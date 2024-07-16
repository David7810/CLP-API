import sys

#deletar isso
sys.path.insert(0, './Lib/site-packages')

import requests
import modbus
import functions
import re
import time

class Mainloop():

    def __init__(self, ip):

        #Endereço Solver.Planning.Domains
        self.enderco_solver = 'https://solver.planning.domains:5001'
        self.package = '/package/lama-first/solve'


        #Instancia o cliente Modbus.
        self.client = modbus.ModbusTcpClient(ip)

        self.finalizado = False

        #Dicionario contendo o estado das entradas e saidas digitais do CLP.
        #Inicialmente todas os registros sao inicializados como falso.
        #Quando em execucao as variaveis associadas as entradas digitais do CLP serao atualizados
        #conforme o estado da memoria
        self.table = {
            'liga_esteira': False,   #OUT
            'anvanca_ap1': False,    #IN
            'anvanca_ap2': False,    #IN
            'anvanca_ap3': False,    #IN
            'retrai_ap3': False,     #IN Logica interna
            'fc_1': False,           #OUT
            'fc_2': False,           #OUT
            'fc_3': False,           #OUT
            'fc_4': False,          #OUT
            'peca_peqnmet': False,   #OUT
            'peca_peqmet': False,    #OUT
            'peca_mednmet': False,   #OUT
            'peca_medmet': False,    #OUT
            'peca_grandnmet': False, #OUT
            'peca_grandmet': False   #OUT
        }

        # Enderco das entradas e saidas
        self.coil_addr = {
            'liga_esteira': 0,
            'anvanca_ap1': 1,
            'anvanca_ap2': 2,
            'anvanca_ap3': 3,
            'retrai_ap3': 4,
            'fc_1': 14,
            'fc_2': 15,
            'fc_3': 16,
            'fc_4': 17,
            'peca_peqnmet': 20,
            'peca_peqmet': 21,
            'peca_mednmet': 22,
            'peca_medmet': 23,
            'peca_grdnmet': 24,
            'peca_grdmet': 25
        }

        #Flags de status de funcionamento
        self.start = False
        self.state = True
        self.running = False
        self.stop = False
        self.precondition_dict = {}
        self.effect_dict = {}

    def setprecondition_dict(self, dicti):
        self.precondition_dict = dicti

    def getprecondition_dict(self):
        return self.precondition_dict

    def seteffect_dict(self, dicti):
        self.effect_dict = dicti

    def geteffect_dict(self):
        return self.effect_dict

    def get_table(self):
        return self.table

    def set_table(self, table):
        self.table = table

    def pause(self):
        self.state = False
        #self.running = False

    def enable(self):
        self.running = True

    def stop1(self):
        self.stop = True


    def getstate(self):
        return self.running

    def reset(self):
        modbus.write_coil_call(self.client, self.coil_addr['liga_esteira'], False)
        modbus.write_coil_call(self.client, self.coil_addr['anvanca_ap1'], False)
        modbus.write_coil_call(self.client, self.coil_addr['anvanca_ap2'], False)
        modbus.write_coil_call(self.client, self.coil_addr['anvanca_ap3'], False)
        modbus.write_coil_call(self.client, self.coil_addr['retrai_ap3'], False)

    def run(self):
        #Cria o cliente modbus com o ip fornecido.
        #print(self.client.connected)
        self.client.connect()
        self.reset()

        #print(self.client.connected)

        F1 = False

        #while not self.running:
        while not self.getstate():
        #while not self.running:
            if self.stop:
                return 0
            time.sleep(1)
        req_body = {'domain': open('./domain.pddl', 'r').read(),
                    'problem': open('./problem.pddl', 'r').read()}

        # Send job request to solve endpoint.
        try:
            solve_request_url=requests.post(self.enderco_solver+self.package, json=req_body).json()
        except Exception as err:
            print('Erro ao obter a solução. Verifique a conexão com a internet')
            raise err

        # Query the result in the job.
        celery_result=requests.post(self.enderco_solver + solve_request_url['result'], json={"adaptor":"planning_editor_adaptor"}  )
        print('Computing...')
        while celery_result.json().get("status","")== 'PENDING':
            # Query the result every 0.5 seconds while the job is executing
            celery_result=requests.post(self.enderco_solver + solve_request_url['result'])
            time.sleep(0.5)
            print('pending')

        #Convertendo a resposta obtida no formato 'requests.models.Response' para formato json armazenado em um dicionario python.
        responseDict = celery_result.json()

        #Agora obtemos a lista de acoes a partir do dicionario da resposta.
        #Cada elemento da lista é um dicionario que possui uma unica chave chamada 'action'. O valor associado a essa chave é uma string contendo a acao a ser
        #tomada, os parametros relativos a essa acao, as condicoes para que essa acao seja tomada e os efeitos esperados depois que a acao é executada.
        try:
            solutionList = responseDict['plans'][0]['result']['plan']
        except Exception as err:
            print('Erro ao obter a solução.')
            raise err
        #Salvando a solucao completa contendo todas as acoes em um arquivo
        with open('./solution', 'w') as f:
            f.write('\n'.join([act['action'] for act in solutionList]))

        #Para cada acao na solucao gerada iremos aguardar as precondicoes necessarias para aquela acao sejam
        #alcancadas para entao executar a acao. Apos excutada a acao iremos aguardar os efeitos esperados daquela acao sejam alcancados.
        #Apos os efeitos esperados terem sido observados iremos processar a proxima acao. Caso todas as acoes do plano tenham sido executadas
        #com sucesso o estado final desejado foi atingido e o programa finaliza
        for index, plan in enumerate(solutionList):
            string = solutionList[index]['action'].splitlines()
            string = [line.lstrip() for line in string]
            string = "\n".join(string)

            string = string.split(':precondition')
            string = string[1].split(':effect')
            precondition = string[0]
            effect = string[1]
            print('\nprecondition r:' + repr(precondition))
            print('\nprecondition:' + precondition)
            print('\neffect r:' + repr(effect))
            print('\neffect:' + effect)

            precondition_met = False
            effect_met = False
            precondition_dict = {}
            effect_dict = {}

            if "(not\n(ligado esteira)\n)" in precondition:
                # precondition_list[0] = 2
                precondition_dict['liga_esteira'] = False
            elif "(ligado esteira)" in precondition:
                # precondition_list[0] = 1
                precondition_dict['liga_esteira'] = True

            if "(not\n(extended atuador_simples1)\n)" in precondition:
                precondition_dict['anvanca_ap1'] = False
            elif "(extended atuador_simples1)" in precondition:
                precondition_dict['anvanca_ap1'] = True

            if "(not\n(extended atuador_simples2)\n)" in precondition:
                precondition_dict['anvanca_ap2'] = False
            elif "(extended atuador_simples2)" in precondition:
                precondition_dict['anvanca_ap2'] = True

            if "(not\n(extended atuador_duplo1)\n)" in precondition:
                precondition_dict['anvanca_ap3'] = False
            elif "(extended atuador_duplo1)" in precondition:
                precondition_dict['anvanca_ap3'] = True

            if "(not\n(s_fimdecurso atuador_simples1)\n)" in precondition:
                precondition_dict['fc_1'] = False
            elif "(s_fimdecurso atuador_simples1)" in precondition:
                precondition_dict['fc_1'] = True

            if "(not\n(s_fimdecurso atuador_simples2)\n)" in precondition:
                precondition_dict['fc_2'] = False
            elif "(s_fimdecurso atuador_simples2)" in precondition:
                precondition_dict['fc_2'] = True

            if "(not\n(s_fimdecurso atuador_duplo1)" in precondition:
                precondition_dict['fc_3'] = False
            elif "(s_fimdecurso atuador_duplo1)" in precondition:
                precondition_dict['fc_3'] = True

            if "(not\n(s_fimdecurso atuador_duplo1)" in precondition:
                precondition_dict['fc_3'] = False
            elif "(s_fimdecurso atuador_duplo1)" in precondition:
                precondition_dict['fc_3'] = True

            if re.search("(type item.? grdmet)", precondition):
                precondition_dict['peca_grdmet'] = True

            if re.search("(type item.? medmet)", precondition):
                precondition_dict['peca_medmet'] = True

            if re.search("(type item.? peqmet)", precondition):
                precondition_dict['peca_peqmet'] = True

            if re.search("(type item.? grdnmet)", precondition):
                precondition_dict['peca_grdnmet'] = True

            if re.search("(type item.? mednmet)", precondition):
                precondition_dict['peca_mednmet'] = True

            if re.search("(type item.? peqnmet)", precondition):
                precondition_dict['peca_peqnmet'] = True

            if "(not\n(ligado esteira)\n)" in effect:
                effect_dict['liga_esteira'] = False
            elif "(ligado esteira)" in effect:
                effect_dict['liga_esteira'] = True

            if "(not\n(extended atuador_simples1)\n)" in effect:
                effect_dict['anvanca_ap1'] = False
            elif "(extended atuador_simples1)" in effect:
                effect_dict['anvanca_ap1'] = True

            if "(not\n(extended atuador_simples2)\n)" in effect:
                effect_dict['anvanca_ap2'] = False
            elif "(extended atuador_simples2)" in effect:
                effect_dict['anvanca_ap2'] = True

            if "(not\n(extended atuador_duplo1)\n)" in effect:
                effect_dict['anvanca_ap3'] = False
            elif "(extended atuador_duplo1)" in effect:
                effect_dict['anvanca_ap3'] = True

            if "(not\n(s_fimdecurso atuador_simples1)\n)" in effect:
                effect_dict['fc_1'] = False
            elif "(s_fimdecurso atuador_simples1)" in effect:
                effect_dict['fc_1'] = True

            if "(not\n(s_fimdecurso atuador_simples2)\n)" in effect:
                effect_dict['fc_2'] = False
            elif "(s_fimdecurso atuador_simples2)" in effect:
                effect_dict['fc_2'] = True

            if "(not\n(s_fimdecurso atuador_duplo1)" in effect:
                effect_dict['fc_3'] = False
            elif "(s_fimdecurso atuador_duplo1)" in effect:
                effect_dict['fc_3'] = True

            if "(not\n(s_fimdecurso atuador_duplo1)" in effect:
                effect_dict['fc_3'] = False
            elif "(s_fimdecurso atuador_duplo1)" in effect:
                effect_dict['fc_3'] = True

            if re.search("(type item.? grdmet)", effect):
                effect_dict['peca_grdmet'] = True

            if re.search("(type item.? medmet)", effect):
                effect_dict['peca_medmet'] = True

            if re.search("(type item.? peqmet)", effect):
                effect_dict['peca_peqmet'] = True

            if re.search("(type item.? grdnmet)", effect):
                effect_dict['peca_grdnmet'] = True

            if re.search("(type item.? mednmet)", effect):
                effect_dict['peca_mednmet'] = True

            if re.search("(type item.? peqnmet)", effect):
                effect_dict['peca_peqnmet'] = True

            print("\nPrecondition dict: ")
            print(precondition_dict)
            self.setprecondition_dict(precondition_dict)
            print("\nEffect dict: ")
            print(effect_dict)
            # print("preconditionlist:\n")
            # print(precondition_list)

            #Verificamos constantemente as precondicoes que esperamos e as comparamos com as precondicoes necessarias.
            #Quando as precondicoes sao atingidas prosseguimos
            while not precondition_met:
                if self.stop:
                #if not self.running:
                    self.reset()
                    return 0


                current_table = {
                    'liga_esteira': modbus.read_coil_call(self.client, self.coil_addr['liga_esteira']),
                    'anvanca_ap1': modbus.read_coil_call(self.client, self.coil_addr['anvanca_ap1']),
                    'anvanca_ap2': modbus.read_coil_call(self.client, self.coil_addr['anvanca_ap2']),
                    'anvanca_ap3': F1,
                    'retrai_ap3': not F1,
                    'fc_1': modbus.read_coil_call(self.client, self.coil_addr['fc_1']),
                    'fc_2': modbus.read_coil_call(self.client, self.coil_addr['fc_2']),
                    'fc_3': modbus.read_coil_call(self.client, self.coil_addr['fc_3']),
                    'fc_4': modbus.read_coil_call(self.client, self.coil_addr['fc_4']),
                    'peca_peqnmet': modbus.read_coil_call(self.client, self.coil_addr['peca_peqnmet']),
                    'peca_peqmet': modbus.read_coil_call(self.client, self.coil_addr['peca_peqmet']),
                    'peca_mednmet': modbus.read_coil_call(self.client, self.coil_addr['peca_mednmet']),
                    'peca_medmet': modbus.read_coil_call(self.client, self.coil_addr['peca_medmet']),
                    'peca_grdnmet': modbus.read_coil_call(self.client, self.coil_addr['peca_grdnmet']),
                    'peca_grdmet': modbus.read_coil_call(self.client, self.coil_addr['peca_grdmet'])
                }

                self.set_table(current_table)

                print('precondition Met?  ')
                print(functions.compare_dicts(precondition_dict, self.get_table()))
                precondition_met = functions.compare_dicts(precondition_dict, self.get_table())

                print('\nCondition we have:')
                print(self.get_table())
                print('\nPrecondition needed: ')
                print(precondition_dict)
                print('-------')

            while not effect_met:
                if self.stop:
                #if not self.running:
                    self.reset()
                    return 0

                if 'liga_esteira' in effect_dict:
                    modbus.write_coil_call(self.client, self.coil_addr['liga_esteira'], effect_dict['liga_esteira'])

                if 'anvanca_ap1' in effect_dict:
                    modbus.write_coil_call(self.client, self.coil_addr['anvanca_ap1'], effect_dict['anvanca_ap1'])

                if 'anvanca_ap2' in effect_dict:
                    modbus.write_coil_call(self.client, self.coil_addr['anvanca_ap2'], effect_dict['anvanca_ap2'])

                if 'anvanca_ap3' in effect_dict:
                    if (not F1 and effect_dict['anvanca_ap3'] == True):
                        print("extend pulse")
                        modbus.write_coil_call(self.client, self.coil_addr['anvanca_ap3'], True)
                        time.sleep(0.1)
                        modbus.write_coil_call(self.client, self.coil_addr['anvanca_ap3'], False)
                        F1 = True
                    elif (F1 and effect_dict['anvanca_ap3'] == False):
                        print("retract pulse")
                        modbus.write_coil_call(self.client, self.coil_addr['retrai_ap3'], True)
                        time.sleep(0.1)
                        modbus.write_coil_call(self.client, self.coil_addr['retrai_ap3'], False)
                        F1 = False

                current_table = {
                    'liga_esteira': modbus.read_coil_call(self.client, self.coil_addr['liga_esteira']),
                    'anvanca_ap1': modbus.read_coil_call(self.client, self.coil_addr['anvanca_ap1']),
                    'anvanca_ap2': modbus.read_coil_call(self.client, self.coil_addr['anvanca_ap2']),
                    'anvanca_ap3': F1,
                    'retrai_ap3': not F1,
                    'fc_1': modbus.read_coil_call(self.client, self.coil_addr['fc_1']),
                    'fc_2': modbus.read_coil_call(self.client, self.coil_addr['fc_2']),
                    'fc_3': modbus.read_coil_call(self.client, self.coil_addr['fc_3']),
                    'fc_4': modbus.read_coil_call(self.client, self.coil_addr['fc_4']),
                    'peca_peqnmet': modbus.read_coil_call(self.client, self.coil_addr['peca_peqnmet']),
                    'peca_peqmet': modbus.read_coil_call(self.client, self.coil_addr['peca_peqmet']),
                    'peca_mednmet': modbus.read_coil_call(self.client, self.coil_addr['peca_mednmet']),
                    'peca_medmet': modbus.read_coil_call(self.client, self.coil_addr['peca_medmet']),
                    'peca_grdnmet': modbus.read_coil_call(self.client, self.coil_addr['peca_grdnmet']),
                    'peca_grdmet': modbus.read_coil_call(self.client, self.coil_addr['peca_grdmet'])
                }

                self.set_table(current_table)

                print('Effect Met?  ')
                print(functions.compare_dicts(effect_dict, self.get_table()))
                effect_met = functions.compare_dicts(effect_dict, self.get_table())
                self.seteffect_dict(effect_dict)

                print('\nCondition we have:')
                print(self.get_table())
                print('\nPrecondition needed: ')
                print(effect_dict)
                print('-------')
            print("\n-------------------------------------")
        self.finalizado = True



if __name__ == "__main__":

    app = Mainloop('127.1.1.1')
    app.running = True
    #app.running = True
    app.run()
