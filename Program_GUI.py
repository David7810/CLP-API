import sys
import tkinter as tk
import tkinter.ttk as ttk

from Main_program import Mainloop
import threading

#Extendendo a classe do programa principal
class Main_program_ThreadClient(Mainloop):
    def __init__(self,ip):
        super().__init__(ip)
        self.lock = threading.Lock()

    #Sobrescrevendo os metodos de escrita/leitura com metodos seguros para threads
    def get_table(self):
        with self.lock:
            return self.table

    def set_table(self, table):
        with self.lock:
            self.table = table

    def enable(self):
        with self.lock:
            self.running = True

    def disable(self):
        with self.lock:
            self.running = False

    def stop1(self):
        with self.lock:
            self.stop = True


#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk


#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk


class aUI:
    def __init__(self, master=None):

        #self.thread_client = Main_program_ThreadClient()
        self.thread_client = None
        self.client_instance = None

        # build ui
        tk2 = tk.Tk(master)

        default = []
        for x in range(18):
            default.append(tk.IntVar(tk2, 0))

        tk2.configure(height=720, width=1280)
        self.frame3 = ttk.Frame(tk2)
        self.frame3.configure(height=720, width=1280)
        message3 = tk.Message(self.frame3)
        message3.configure(text='Digite o IP do CLP', width=100)
        message3.pack(anchor="center", pady=20, side="top")
        self.entry = ttk.Entry(self.frame3)
        self.entry.pack(anchor="center", side="top")
        button1 = ttk.Button(self.frame3)
        button1.configure(text='Conectar', command= self.conectar)
        button1.pack(anchor="center", pady=20, side="top")
        self.frame3.grid(column=0, row=0)
        self.frame3.pack_propagate(0)
        self.frame6 = ttk.Frame(tk2)
        self.frame6.configure(height=720, width=1280)
        canvas1 = tk.Canvas(self.frame6)
        canvas1.configure(height=450, state="normal", width=1152)
        canvas1.pack(padx=20, pady=20, side="top")
        frame5 = ttk.Frame(self.frame6)
        frame5.configure(height=200, width=200)
        labelframe2 = ttk.Labelframe(frame5)
        labelframe2.configure(height=200, text='Selecão de itens', width=200)
        label1 = tk.Label(labelframe2)
        label1.configure(text='Metalica Pequena')
        label1.grid(column=0, padx=20, pady=6, row=1)
        label2 = tk.Label(labelframe2)
        label2.configure(text='Metalica Media')
        label2.grid(column=0, row=2)
        label3 = tk.Label(labelframe2)
        label3.configure(text='Metalica Grande')
        label3.grid(column=0, pady=6, row=3)
        label4 = tk.Label(labelframe2)
        label4.configure(text='Nao metalica pequena')
        label4.grid(column=0, row=4)
        label5 = tk.Label(labelframe2)
        label5.configure(
            cursor="arrow",
            font="TkDefaultFont",
            text='Nao metalica media')
        label5.grid(column=0, pady=6, row=5)
        label6 = tk.Label(labelframe2)
        label6.configure(text='Nao metalica grande')
        label6.grid(column=0, row=6)
        label7 = tk.Label(labelframe2)
        label7.configure(text='Caixa de descarte 1')
        label7.grid(column=1, row=0)
        self.spinbox2 = tk.Spinbox(labelframe2)
        self.spinbox2.configure(from_=0, to=99, textvariable=default[0],width=6)
        self.spinbox2.grid(column=1, row=1)
        self.spinbox3 = tk.Spinbox(labelframe2)
        self.spinbox3.configure(from_=0, to=99, textvariable=default[1],width=6)
        self.spinbox3.grid(column=1, row=2)
        self.spinbox4 = tk.Spinbox(labelframe2)
        self.spinbox4.configure(from_=0, to=99, textvariable=default[2],width=6)
        self.spinbox4.grid(column=1, row=3)
        self.spinbox5 = tk.Spinbox(labelframe2)
        self.spinbox5.configure(from_=0, to=99, textvariable=default[3],width=6)
        self.spinbox5.grid(column=1, row=4)
        self.spinbox6 = tk.Spinbox(labelframe2)
        self.spinbox6.configure(from_=0, to=99, textvariable=default[4],width=6)
        self.spinbox6.grid(column=1, row=5)
        self.spinbox7 = tk.Spinbox(labelframe2)
        self.spinbox7.configure(from_=0, to=99, textvariable=default[5],width=6)
        self.spinbox7.grid(column=1, row=6)
        label8 = tk.Label(labelframe2)
        label8.configure(text='Caixa de descarte 2')
        label8.grid(column=2, padx=17, row=0)
        self.spinbox8 = tk.Spinbox(labelframe2)
        self.spinbox8.configure(from_=0, to=99, textvariable=default[6],width=6)
        self.spinbox8.grid(column=2, row=1)
        self.spinbox9 = tk.Spinbox(labelframe2)
        self.spinbox9.configure(from_=0, to=99, textvariable=default[7],width=6)
        self.spinbox9.grid(column=2, row=2)
        self.spinbox10 = tk.Spinbox(labelframe2)
        self.spinbox10.configure(from_=0, to=99, textvariable=default[8],width=6)
        self.spinbox10.grid(column=2, row=3)
        self.spinbox11 = tk.Spinbox(labelframe2)
        self.spinbox11.configure(from_=0, to=99, textvariable=default[9],width=6)
        self.spinbox11.grid(column=2, row=4)
        self.spinbox12 = tk.Spinbox(labelframe2)
        self.spinbox12.configure(from_=0, to=99, textvariable=default[10],width=6)
        self.spinbox12.grid(column=2, row=5)
        self.spinbox13 = tk.Spinbox(labelframe2)
        self.spinbox13.configure(from_=0, to=99, textvariable=default[11],width=6)
        self.spinbox13.grid(column=2, row=6)
        label9 = tk.Label(labelframe2)
        label9.configure(text='Caixa de descarte 3')
        label9.grid(column=3, row=0)
        self.spinbox14 = tk.Spinbox(labelframe2)
        self.spinbox14.configure(from_=0, to=99, textvariable=default[12],width=6)
        self.spinbox14.grid(column=3, row=1)
        self.spinbox15 = tk.Spinbox(labelframe2)
        self.spinbox15.configure(from_=0, to=99, textvariable=default[13],width=6)
        self.spinbox15.grid(column=3, row=2)
        self.spinbox16 = tk.Spinbox(labelframe2)
        self.spinbox16.configure(from_=0, to=99, textvariable=default[14],width=6)
        self.spinbox16.grid(column=3, row=3)
        self.spinbox17 = tk.Spinbox(labelframe2)
        self.spinbox17.configure(from_=0, to=99, textvariable=default[15],width=6)
        self.spinbox17.grid(column=3, row=4)
        self.spinbox18 = tk.Spinbox(labelframe2)
        self.spinbox18.configure(from_=0, to=99, textvariable=default[16],width=6)
        self.spinbox18.grid(column=3, row=5)
        self.spinbox19 = tk.Spinbox(labelframe2)
        self.spinbox19.configure(from_=0, to=99, textvariable=default[17],width=6)
        self.spinbox19.grid(column=3, row=6)
        labelframe2.grid(column=0, row=0)
        labelframe4 = ttk.Labelframe(frame5)
        labelframe4.configure(height=200, text='Execução', width=200)
        label10 = ttk.Label(labelframe4)
        label10.configure(text='Estado:  ')
        label10.pack(expand=True, side="top")
        button2 = ttk.Button(labelframe4)
        button2.configure(text='Iniciar', command=self.iniciar)
        button2.pack(expand=True, side="top")
        self.button3 = ttk.Button(labelframe4)
        self.button3.configure(text='Parar/Reprogamar', command=self.parar)
        self.button3.pack(expand=True, side="top")
        button4 = ttk.Button(labelframe4)
        button4.configure(text='Desconectar e Resetar', command=self.desconectar)
        button4.pack(expand=True, side="top")
        labelframe4.grid(column=2, padx=25, row=0)
        labelframe4.pack_propagate(0)
        labelframe3 = ttk.Labelframe(frame5)
        labelframe3.configure(
            height=200,
            text='Registro de eventos\n',
            width=200)
        text1 = tk.Text(labelframe3)
        text1.configure(height=10, state="disabled", width=50)
        text1.pack(padx=0, pady=0, side="top")
        labelframe3.grid(column=3, row=0)
        frame5.pack(side="top")
        self.frame6.grid(column=0, row=0)
        self.frame6.pack_propagate(0)

        # Main widget
        self.mainwindow = tk2

    def run(self):
        self.update()
        self.mainwindow.mainloop()

    #Atualiza a interface
    def update(self):

        if self.client_instance is not None and self.client_instance.getstate():
            self.spinbox2.configure(state=tk.DISABLED)
            self.spinbox3.configure(state=tk.DISABLED)
            self.spinbox4.configure(state=tk.DISABLED)
            self.spinbox5.configure(state=tk.DISABLED)
            self.spinbox6.configure(state=tk.DISABLED)
            self.spinbox7.configure(state=tk.DISABLED)
            self.spinbox8.configure(state=tk.DISABLED)
            self.spinbox9.configure(state=tk.DISABLED)
            self.spinbox10.configure(state=tk.DISABLED)
            self.spinbox11.configure(state=tk.DISABLED)
            self.spinbox12.configure(state=tk.DISABLED)
            self.spinbox13.configure(state=tk.DISABLED)
            self.spinbox14.configure(state=tk.DISABLED)
            self.spinbox15.configure(state=tk.DISABLED)
            self.spinbox16.configure(state=tk.DISABLED)
            self.spinbox17.configure(state=tk.DISABLED)
            self.spinbox18.configure(state=tk.DISABLED)
            self.spinbox19.configure(state=tk.DISABLED)
        else:
            self.spinbox2.configure(state=tk.NORMAL)
            self.spinbox3.configure(state=tk.NORMAL)
            self.spinbox4.configure(state=tk.NORMAL)
            self.spinbox5.configure(state=tk.NORMAL)
            self.spinbox6.configure(state=tk.NORMAL)
            self.spinbox7.configure(state=tk.NORMAL)
            self.spinbox8.configure(state=tk.NORMAL)
            self.spinbox9.configure(state=tk.NORMAL)
            self.spinbox10.configure(state=tk.NORMAL)
            self.spinbox11.configure(state=tk.NORMAL)
            self.spinbox12.configure(state=tk.NORMAL)
            self.spinbox13.configure(state=tk.NORMAL)
            self.spinbox14.configure(state=tk.NORMAL)
            self.spinbox15.configure(state=tk.NORMAL)
            self.spinbox16.configure(state=tk.NORMAL)
            self.spinbox17.configure(state=tk.NORMAL)
            self.spinbox18.configure(state=tk.NORMAL)
            self.spinbox19.configure(state=tk.NORMAL)


        if self.thread_client is not None:
            if self.thread_client.is_alive() and self.client_instance.client.connected:
                self.frame6.tkraise()
            else:
                self.frame3.tkraise()
        else :
            self.frame3.tkraise()
        #if self.f1:
        #    self.frame3.tkraise()
        #else:
        #    self.frame6.tkraise()

        #self.f1 = not self.f1
        #print(threading.enumerate(),'\n')


        self.mainwindow.after(50, self.update)

    def conectar(self):
        entered_value = self.entry.get()
        print('entered value:', entered_value)
        if entered_value != "":
            self.client_instance = Main_program_ThreadClient(entered_value)
            self.thread_client = threading.Thread(target=lambda a: a.run(), args=([self.client_instance]))
            self.thread_client.start()
        #self.client_instance.enable()
        #self.thread_client.start()
        #self.thread_client()
        #self.table = self.instance.prog.table

    def iniciar(self):
        self.generate_problem()
        self.client_instance.enable()

    def parar(self):
        self.client_instance.stop1()
        self.conectar()

    def desconectar(self):
        self.client_instance.stop1()


    def generate_problem(self):
        # Armazena as informacoes sobre o problema desejado
        items = {
            'cx1_peq_metal': self.spinbox2.get(),
            'cx1_med_metal': self.spinbox3.get(),
            'cx1_grd_metal': self.spinbox4.get(),
            'cx1_peq': self.spinbox5.get(),
            'cx1_med': self.spinbox6.get(),
            'cx1_grd': self.spinbox7.get(),

            'cx2_peq_metal': self.spinbox8.get(),
            'cx2_med_metal': self.spinbox9.get(),
            'cx2_grd_metal': self.spinbox10.get(),
            'cx2_peq': self.spinbox11.get(),
            'cx2_med': self.spinbox12.get(),
            'cx2_grd': self.spinbox13.get(),

            'cx3_peq_metal': self.spinbox14.get(),
            'cx3_med_metal': self.spinbox15.get(),
            'cx3_grd_metal': self.spinbox16.get(),
            'cx3_peq': self.spinbox17.get(),
            'cx3_med': self.spinbox18.get(),
            'cx3_grd': self.spinbox19.get()
        }

        # Gerando o problema a partir das informacoes inseridas
        lines = []
        for keys in items:
            items[keys] = int(items[keys])

        n_box1 = items['cx1_peq_metal'] + items['cx1_med_metal'] + items['cx1_grd_metal'] + items['cx1_peq'] + items[
            'cx1_med'] + items['cx1_grd']
        n_box2 = items['cx2_peq_metal'] + items['cx2_med_metal'] + items['cx2_grd_metal'] + items['cx2_peq'] + items[
            'cx2_med'] + items['cx2_grd']
        n_box3 = items['cx3_peq_metal'] + items['cx3_med_metal'] + items['cx3_grd_metal'] + items['cx3_peq'] + items[
            'cx3_med'] + items['cx3_grd']

        n_peq_metal = items['cx1_peq_metal'] + items['cx2_peq_metal'] + items['cx3_peq_metal']
        n_med_metal = items['cx1_med_metal'] + items['cx2_med_metal'] + items['cx3_med_metal']
        n_grd_metal = items['cx1_grd_metal'] + items['cx2_grd_metal'] + items['cx3_grd_metal']

        n_peq = items['cx1_peq'] + items['cx2_peq'] + items['cx3_peq']
        n_med = items['cx1_med'] + items['cx2_med'] + items['cx3_med']
        n_grd = items['cx1_grd'] + items['cx2_grd'] + items['cx3_grd']

        n_items = sum(items.values())

        with open('problem-template.pddl', 'r') as f:
            for line in f:
                if line.startswith('	##definir_itens'):
                    line = '        '
                    num = 0
                    tipo_items = {}
                    for x in range(n_peq_metal):
                        line = line + 'item' + str(num) + ' - peqmet\n        '
                        tipo_items['item' + str(num)] = 'peqmet'
                        num += 1

                    for x in range(n_med_metal):
                        line = line + 'item' + str(num) + ' - medmet\n        '
                        tipo_items['item' + str(num)] = 'medmet'
                        num += 1

                    for x in range(n_grd_metal):
                        line = line + 'item' + str(num) + ' - grdmet\n        '
                        tipo_items['item' + str(num)] = 'grdmet'
                        num += 1

                    for x in range(n_peq):
                        line = line + 'item' + str(num) + ' - peqnmet\n        '
                        tipo_items['item' + str(num)] = 'peqnmet'
                        num += 1

                    for x in range(n_med):
                        line = line + 'item' + str(num) + ' - mednmet\n        '
                        tipo_items['item' + str(num)] = 'mednmet'
                        num += 1

                    for x in range(n_grd):
                        line = line + 'item' + str(num) + ' - grdnmet\n        '
                        tipo_items['item' + str(num)] = 'grdnmet'
                        num += 1

                if line.startswith('	##definir_tipos'):
                    line = '        '
                    num = 0
                    tipo_items = {}
                    for x in range(n_peq_metal):
                        line = line + '(type item' + str(num) + ' ' + 'peqmet1)\n        '
                        tipo_items['item' + str(num)] = 'peqmet'
                        num += 1

                    for x in range(n_med_metal):
                        line = line + '(type item' + str(num) + ' ' + 'medmet1)\n        '
                        tipo_items['item' + str(num)] = 'medmet'
                        num += 1

                    for x in range(n_grd_metal):
                        line = line + '(type item' + str(num) + ' ' + 'grdmet1)\n        '
                        tipo_items['item' + str(num)] = 'grdmet'
                        num += 1

                    for x in range(n_peq):
                        line = line + '(type item' + str(num) + ' ' + 'peqnmet1)\n        '
                        tipo_items['item' + str(num)] = 'peqnmet'
                        num += 1

                    for x in range(n_med):
                        line = line + '(type item' + str(num) + ' ' + 'mednmet1)\n        '
                        tipo_items['item' + str(num)] = 'mednmet'
                        num += 1

                    for x in range(n_grd):
                        line = line + '(type item' + str(num) + ' ' + 'grdnmet1)\n        '
                        tipo_items['item' + str(num)] = 'grdnmet'
                        num += 1



                if line.startswith('	##definir_inicio'):
                    line = '        '
                    for x in range(n_items):
                        line = line + '(at item' + str(x) + ' inicio' + ')\n        '

                if line.startswith('        ##definir_destino'):
                    line = '        '

                    key_list = list(tipo_items.keys())

                    for keys in items:
                        match keys:
                            case 'cx1_peq_metal':
                                for x in range(items['cx1_peq_metal']):
                                    val_list = list(tipo_items.values())
                                    position = val_list.index('peqmet')
                                    tipo_items[key_list[position]] = 'box1'

                            case 'cx1_med_metal':
                                for x in range(items['cx1_med_metal']):
                                    val_list = list(tipo_items.values())
                                    position = val_list.index('medmet')
                                    tipo_items[key_list[position]] = 'box1'

                            case 'cx1_grd_metal':
                                for x in range(items['cx1_grd_metal']):
                                    val_list = list(tipo_items.values())
                                    position = val_list.index('grdmet')
                                    tipo_items[key_list[position]] = 'box1'

                            case 'cx1_peq':
                                for x in range(items['cx1_peq']):
                                    val_list = list(tipo_items.values())
                                    position = val_list.index('peqnmet')
                                    tipo_items[key_list[position]] = 'box1'

                            case 'cx1_med':
                                for x in range(items['cx1_med']):
                                    val_list = list(tipo_items.values())
                                    position = val_list.index('mednmet')
                                    tipo_items[key_list[position]] = 'box1'

                            case 'cx1_grd':
                                for x in range(items['cx1_grd']):
                                    val_list = list(tipo_items.values())
                                    position = val_list.index('grdnmet')
                                    tipo_items[key_list[position]] = 'box1'

                            case 'cx2_peq_metal':
                                for x in range(items['cx2_peq_metal']):
                                    val_list = list(tipo_items.values())
                                    position = val_list.index('peqmet')
                                    tipo_items[key_list[position]] = 'box2'

                            case 'cx2_med_metal':
                                for x in range(items['cx2_med_metal']):
                                    val_list = list(tipo_items.values())
                                    position = val_list.index('medmet')
                                    tipo_items[key_list[position]] = 'box2'

                            case 'cx2_grd_metal':
                                for x in range(items['cx2_grd_metal']):
                                    val_list = list(tipo_items.values())
                                    position = val_list.index('grdmet')
                                    tipo_items[key_list[position]] = 'box2'

                            case 'cx2_peq':
                                for x in range(items['cx2_peq']):
                                    val_list = list(tipo_items.values())
                                    position = val_list.index('peqnmet')
                                    tipo_items[key_list[position]] = 'box2'

                            case 'cx2_med':
                                for x in range(items['cx2_med']):
                                    val_list = list(tipo_items.values())
                                    position = val_list.index('mednmet')
                                    tipo_items[key_list[position]] = 'box2'

                            case 'cx2_grd':
                                for x in range(items['cx2_grd']):
                                    val_list = list(tipo_items.values())
                                    position = val_list.index('grdnmet')
                                    tipo_items[key_list[position]] = 'box2'

                            case 'cx3_peq_metal':
                                for x in range(items['cx3_peq_metal']):
                                    val_list = list(tipo_items.values())
                                    position = val_list.index('peqmet')
                                    tipo_items[key_list[position]] = 'box3'

                            case 'cx3_med_metal':
                                for x in range(items['cx3_med_metal']):
                                    val_list = list(tipo_items.values())
                                    position = val_list.index('medmet')
                                    tipo_items[key_list[position]] = 'box3'

                            case 'cx3_grd_metal':
                                for x in range(items['cx3_grd_metal']):
                                    val_list = list(tipo_items.values())
                                    position = val_list.index('grdmet')
                                    tipo_items[key_list[position]] = 'box3'

                            case 'cx3_peq':
                                for x in range(items['cx3_peq']):
                                    val_list = list(tipo_items.values())
                                    position = val_list.index('peqnmet')
                                    tipo_items[key_list[position]] = 'box3'

                            case 'cx3_med':
                                for x in range(items['cx3_med']):
                                    val_list = list(tipo_items.values())
                                    position = val_list.index('mednmet')
                                    tipo_items[key_list[position]] = 'box3'

                            case 'cx3_grd':
                                for x in range(items['cx3_grd']):
                                    val_list = list(tipo_items.values())
                                    position = val_list.index('grdnmet')
                                    tipo_items[key_list[position]] = 'box3'

                    # for x in range(n_box1):
                    #   line += '(at box1 ' +
                    for key, value in tipo_items.items():
                        line += '(at ' + key + ' ' + value + ')' + '\n        '

                lines.append(line)

        # Escrevendo o problema no arquivo
        with open('problem.pddl', 'w') as f:
            f.writelines(lines)

if __name__ == "__main__":
    app = aUI()
    app.run()