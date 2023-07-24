import sys
sys.path.insert(0, './Lib/site-packages')

import requests
import modbus
import functions
import re
import time

class program():

    def __init__(self, ip):
        self.table = {
            'liga_esteira': False,
            'anvanca_ap1': False,
            'anvanca_ap2': False,
            'anvanca_ap3': False,
            'retrai_ap3': False,
            'fc_1': False,
            'fc_2': False,
            'fc_3': False,
            'fc_4': False,
            'peca_peqnmet': False,
            'peca_peqmet': False,
            'peca_mednmet': False,
            'peca_medmet': False,
            'peca_grandnmet': False,
            'peca_grandmet': False
        }
        self.start = False
        self.ip = ip
        self.state = True

    def run(self):
        self.client = modbus.ModbusTcpClient(self.ip)

        self.client.connect()
        #print(self.client.connected)

        F1 = False

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

        while not self.start:
            if not self.state:
                return 0
            time.sleep(1)

        data = {'domain': open('./domain.pddl', 'r').read(),
                'problem': open('./problem.pddl', 'r').read()}

        resp = requests.post('http://solver.planning.domains/solve', verify=False, json=data).json()

        with open('./solution', 'w') as f:
            f.write('\n'.join([act['action'] for act in resp['result']['plan']]))

        for index, plan in enumerate(resp['result']['plan']):
            string = functions.remove_space(resp['result']['plan'][index]['action'])
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


            while not precondition_met:
                if not self.state:
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
                if not self.state:
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
    app = program("127.0.0.1")
    app.start = True
    app.run()
