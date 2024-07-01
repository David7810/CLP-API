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

        #Instancia o cliente Modbus.
        self.client = modbus.ModbusTcpClient(ip)

        #Dicionario contendo o estado das entradas e saidas digitais do CLP.
        #Inicialmente todas os registros sao inicializados como falso.
        #Quando em execucao as variaveis associadas as entradas digitais do CLP serao atualizados
        #conforme o estado da memoria
        self.table = {
            'liga_esteira': False,   #OUT
            'anvanca_ap1': False,    #IN
            'anvanca_ap2': False,    #IN
            'anvanca_ap3': False,    #IN
            'retrai_ap3': False,     #IN
            'fc_1': False,           #OUT
            'fc_2': False,           #OUT
            'fc_3': False,           #OUT
            'fc_4': False,           #OUT
            'peca_peqnmet': False,   #OUT
            'peca_peqmet': False,    #OUT
            'peca_mednmet': False,   #OUT
            'peca_medmet': False,    #OUT
            'peca_grandnmet': False, #OUT
            'peca_grandmet': False   #OUT
        }


        #Flags de status de funcionamento
        self.start = False
        self.state = True
        self.running = False
        self.stop = False

    def get_table(self):
        return self.table

    def set_table(self, table):
        self.table = table

    def pause(self):
        self.state = False
        #self.running = False

    def enable(self):
        self.running = True

    def disable(self):
        self.running = False

    def stop(self):
        self.stop = True

    def getstate(self):
        return self.running

    def run(self):

        #Cria o cliente modbus com o ip fornecido.
        #print(self.client.connected)
        self.client.connect()

        #print(self.client.connected)



        #Define o estado inicial
        try:
            liga_esteira = modbus.write_coil_call(self.client, 0, False)
            anvanca_ap1 = modbus.write_coil_call(self.client, 2, False)
            anvanca_ap2 = modbus.write_coil_call(self.client, 3, False)
            #fc_1 = modbus.write_coil_call(self.client, 14, False)
            #fc_2 = modbus.write_coil_call(self.client, 15, False)
            #fc_3 = modbus.write_coil_call(self.client, 16, False)
            #fc_4 = modbus.write_coil_call(self.client, 17, False)
            peca_peqnmet = modbus.write_coil_call(self.client, 20, False)
            peca_peqmet = modbus.write_coil_call(self.client, 21, False)
            peca_mednmet = modbus.write_coil_call(self.client, 22, False)
            peca_medmet = modbus.write_coil_call(self.client, 23, False)
            peca_grdnmet = modbus.write_coil_call(self.client, 24, False)
            peca_grdmet = modbus.write_coil_call(self.client, 25, False)
        except:
            print('erro ao conectar')
            #sys.exit(1)
            return 0
        #print()

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
        solve_request_url=requests.post("https://solver.planning.domains:5001/package/lama-first/solve", json=req_body).json()

        # Query the result in the job.
        celery_result=requests.post('https://solver.planning.domains:5001' + solve_request_url['result'], json={"adaptor":"planning_editor_adaptor"}  )
        print('Computing...')
        while celery_result.json().get("status","")== 'PENDING':

            # Query the result every 0.5 seconds while the job is executing
            celery_result=requests.post('https://solver.planning.domains:5001' + solve_request_url['result'])
            time.sleep(0.5)
            print('pending')

        #Convertendo a resposta obtida no formato 'requests.models.Response' para formato json armazenado em um dicionario python.
        responseDict = celery_result.json()

        #Agora obtemos a lista de acoes a partir do dicionario da resposta.
        #Cada elemento da lista é um dicionario que possui uma unica chave chamada 'action'. O valor associado a essa chave é uma string contendo a acao a ser
        #tomada, os parametros relativos a essa acao, as condicoes para que essa acao seja tomada e os efeitos esperados depois que a acao é executada.
        try:
            solutionList = responseDict['plans'][0]['result']['plan']
        except:
            print('Nao foi possivel obter a solucao. Verifique a conexão com a internet e tente novamente')

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
                precondition_dict['peca_grdmet'] = True

            if re.search("(type item.? mednmet)", precondition):
                precondition_dict['peca_medmet'] = True

            if re.search("(type item.? peqnmet)", precondition):
                precondition_dict['peca_peqmet'] = True

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
                effect_dict['peca_grdmet'] = True

            if re.search("(type item.? mednmet)", effect):
                effect_dict['peca_medmet'] = True

            if re.search("(type item.? peqnmet)", effect):
                effect_dict['peca_peqmet'] = True

            print("\nPrecondition dict: ")
            print(precondition_dict)
            print("\nEffect dict: ")
            print(effect_dict)
            # print("preconditionlist:\n")
            # print(precondition_list)

            #Verificamos constantemente as precondicoes que esperamos e as comparamos com as precondicoes necessarias.
            #Quando as precondicoes sao atingidas prosseguimos
            while not precondition_met:
                if self.stop:
                #if not self.running:
                    return 0

                self.table['liga_esteira'] = modbus.read_coil_call(self.client, 0)
                self.table['anvanca_ap1'] = modbus.read_coil_call(self.client, 1)
                self.table['anvanca_ap2'] = modbus.read_coil_call(self.client, 2)

                self.table['anvanca_ap3'] = F1
                self.table['retrai_ap3'] = not F1

                self.table['fc_1'] = modbus.read_coil_call(self.client, 14)
                self.table['fc_2'] = modbus.read_coil_call(self.client, 15)
                self.table['fc_3'] = modbus.read_coil_call(self.client, 16)
                self.table['fc_4'] = modbus.read_coil_call(self.client, 17)
                self.table['peca_peqnmet'] = modbus.read_coil_call(self.client, 20)
                self.table['peca_peqmet'] = modbus.read_coil_call(self.client, 21)
                self.table['peca_mednmet'] = modbus.read_coil_call(self.client, 22)
                self.table['peca_medmet'] = modbus.read_coil_call(self.client, 23)
                self.table['peca_grdnmet'] = modbus.read_coil_call(self.client, 24)
                self.table['peca_grdmet'] = modbus.read_coil_call(self.client, 25)

                print('precondition Met?  ')
                print(functions.compare_dicts(precondition_dict, self.table))
                precondition_met = functions.compare_dicts(precondition_dict, self.table)

                print('\nprecondition we have:')
                print(self.table)
                print('\nPrecondition needed: ')
                print(precondition_dict)
                print('-------')

            while not effect_met:
                if self.stop:
                #if not self.running:
                    return 0

                if 'liga_esteira' in effect_dict:
                    modbus.write_coil_call(self.client, 0, effect_dict['liga_esteira'])

                if 'anvanca_ap1' in effect_dict:
                    modbus.write_coil_call(self.client, 1, effect_dict['anvanca_ap1'])

                if 'anvanca_ap2' in effect_dict:
                    modbus.write_coil_call(self.client, 2, effect_dict['anvanca_ap2'])

                if 'anvanca_ap3' in effect_dict:
                    if (not F1 and effect_dict['anvanca_ap3'] == True):
                        print("extend pulse")
                        modbus.write_coil_call(self.client, 3, True)
                        time.sleep(0.1)
                        modbus.write_coil_call(self.client, 3, False)
                        F1 = True
                    elif (F1 and effect_dict['anvanca_ap3'] == False):
                        print("retract pulse")
                        modbus.write_coil_call(self.client, 3, True)
                        time.sleep(0.1)
                        modbus.write_coil_call(self.client, 3, False)
                        F1 = False

                self.table['liga_esteira'] = modbus.read_coil_call(self.client, 0)
                self.table['anvanca_ap1'] = modbus.read_coil_call(self.client, 1)
                self.table['anvanca_ap2'] = modbus.read_coil_call(self.client, 2)
                self.table['anvanca_ap3'] = F1
                self.table['retrai_ap3'] = not F1

                self.table['fc_1'] = modbus.read_coil_call(self.client, 14)
                self.table['fc_2'] = modbus.read_coil_call(self.client, 15)
                self.table['fc_3'] = modbus.read_coil_call(self.client, 16)
                self.table['fc_4'] = modbus.read_coil_call(self.client, 17)
                self.table['peca_peqnmet'] = modbus.read_coil_call(self.client, 20)
                self.table['peca_peqmet'] = modbus.read_coil_call(self.client, 21)
                self.table['peca_mednmet'] = modbus.read_coil_call(self.client, 22)
                self.table['peca_medmet'] = modbus.read_coil_call(self.client, 23)
                self.table['peca_grdnmet'] = modbus.read_coil_call(self.client, 24)
                self.table['peca_grdmet'] = modbus.read_coil_call(self.client, 25)

                print('Effect Met?  ')
                print(functions.compare_dicts(effect_dict, self.table))
                effect_met = functions.compare_dicts(effect_dict, self.table)

                print('\nprecondition we have:')
                print(self.table)
                print('\nPrecondition needed: ')
                print(effect_dict)
                print('-------')

            print("\n-------------------------------------")



if __name__ == "__main__":
    app = Mainloop('127.1.1.1')
    app.running = True
    #app.running = True
    app.run()
