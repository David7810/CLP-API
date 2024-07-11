import sys
import tkinter as tk
import tkinter.ttk as ttk

from Main_program import Mainloop
from Main_program import modbus
import threading
from queue import Queue

#Extendendo a classe do programa principal
class Main_program_ThreadClient(Mainloop):
    def __init__(self,ip):
        super().__init__(ip)
        self.finalizado = False
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

    def stop1(self):
        with self.lock:
            self.stop = True

    def getstate(self):
        with self.lock:
            return self.running

    def setprecondition_dict(self, dict):
        with self.lock:
            self.precondition_dict = dict

    def getprecondition_dict(self):
        with self.lock:
            return self.precondition_dict

    def run(self):
        self.finalizado = False
        try:
            Mainloop.run(self)
        except Exception as err:
            #self.stop1()
            raise err
            #sys.exit()
        else:
            if self.finalizado:
                return 2


#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk


#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk


class aUI:
    def __init__(self, master=None):

        #self.thread_client = Main_program_ThreadClient()
        self.ip = None
        self.thread_client = None
        self.client_instance = None
        self.end_que = Queue()
        self.pecas_que = Queue()
        self.descartando_pecaincorreta = False

        #Armazena a quantidade de peças em cada caixa
        self.caixa_descarte1 = {
            'peca_peqnmet': 0,
            'peca_peqmet': 0,
            'peca_mednmet': 0,
            'peca_medmet': 0,
            'peca_grdnmet': 0,
            'peca_grdmet': 0
        }
        self.caixa_descarte2 = {
            'peca_peqnmet': 0,
            'peca_peqmet': 0,
            'peca_mednmet': 0,
            'peca_medmet': 0,
            'peca_grdnmet': 0,
            'peca_grdmet': 0
        }
        self.caixa_descarte3 = {
            'peca_peqnmet': 0,
            'peca_peqmet': 0,
            'peca_mednmet': 0,
            'peca_medmet': 0,
            'peca_grdnmet': 0,
            'peca_grdmet': 0
        }
        self.caixa_descarte4 = {
            'peca_peqnmet': 0,
            'peca_peqmet': 0,
            'peca_mednmet': 0,
            'peca_medmet': 0,
            'peca_grdnmet': 0,
            'peca_grdmet': 0
        }

        self.precondition_dict = {}
        self.table = {}

        # build ui
        tk2 = tk.Tk(master)

        self.default = []
        for x in range(18):
            self.default.append(tk.IntVar(tk2, 0))

        tk2.configure(height=720, width=1280)
        self.frame3 = ttk.Frame(tk2)
        self.frame3.configure(height=720, width=1280)
        message3 = tk.Message(self.frame3)
        message3.configure(text='Digite o IP do CLP', width=100)
        message3.pack(anchor="center", pady=20, side="top")
        self.entry = ttk.Entry(self.frame3)
        self.entry.pack(anchor="center", side="top")
        button1 = ttk.Button(self.frame3)
        button1.configure(text='Definir Endereço', command= self.conectar)
        button1.pack(anchor="center", pady=20, side="top")
        self.frame3.grid(column=0, row=0)
        self.frame3.pack_propagate(0)
        self.frame6 = ttk.Frame(tk2)
        self.frame6.configure(height=720, width=1280)
        self.canvas1 = tk.Canvas(self.frame6)
        self.canvas1.configure(height=450, state="normal", width=1152)
        self.canvas1.pack(padx=20, pady=20, side="top")
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
        self.spinbox2.configure(from_=0, to=99, textvariable=self.default[0],width=6)
        self.spinbox2.grid(column=1, row=1)
        self.spinbox3 = tk.Spinbox(labelframe2)
        self.spinbox3.configure(from_=0, to=99, textvariable=self.default[1],width=6)
        self.spinbox3.grid(column=1, row=2)
        self.spinbox4 = tk.Spinbox(labelframe2)
        self.spinbox4.configure(from_=0, to=99, textvariable=self.default[2],width=6)
        self.spinbox4.grid(column=1, row=3)
        self.spinbox5 = tk.Spinbox(labelframe2)
        self.spinbox5.configure(from_=0, to=99, textvariable=self.default[3],width=6)
        self.spinbox5.grid(column=1, row=4)
        self.spinbox6 = tk.Spinbox(labelframe2)
        self.spinbox6.configure(from_=0, to=99, textvariable=self.default[4],width=6)
        self.spinbox6.grid(column=1, row=5)
        self.spinbox7 = tk.Spinbox(labelframe2)
        self.spinbox7.configure(from_=0, to=99, textvariable=self.default[5],width=6)
        self.spinbox7.grid(column=1, row=6)
        label8 = tk.Label(labelframe2)
        label8.configure(text='Caixa de descarte 2')
        label8.grid(column=2, padx=17, row=0)
        self.spinbox8 = tk.Spinbox(labelframe2)
        self.spinbox8.configure(from_=0, to=99, textvariable=self.default[6],width=6)
        self.spinbox8.grid(column=2, row=1)
        self.spinbox9 = tk.Spinbox(labelframe2)
        self.spinbox9.configure(from_=0, to=99, textvariable=self.default[7],width=6)
        self.spinbox9.grid(column=2, row=2)
        self.spinbox10 = tk.Spinbox(labelframe2)
        self.spinbox10.configure(from_=0, to=99, textvariable=self.default[8],width=6)
        self.spinbox10.grid(column=2, row=3)
        self.spinbox11 = tk.Spinbox(labelframe2)
        self.spinbox11.configure(from_=0, to=99, textvariable=self.default[9],width=6)
        self.spinbox11.grid(column=2, row=4)
        self.spinbox12 = tk.Spinbox(labelframe2)
        self.spinbox12.configure(from_=0, to=99, textvariable=self.default[10],width=6)
        self.spinbox12.grid(column=2, row=5)
        self.spinbox13 = tk.Spinbox(labelframe2)
        self.spinbox13.configure(from_=0, to=99, textvariable=self.default[11],width=6)
        self.spinbox13.grid(column=2, row=6)
        label9 = tk.Label(labelframe2)
        label9.configure(text='Caixa de descarte 3')
        label9.grid(column=3, row=0)
        self.spinbox14 = tk.Spinbox(labelframe2)
        self.spinbox14.configure(from_=0, to=99, textvariable=self.default[12],width=6)
        self.spinbox14.grid(column=3, row=1)
        self.spinbox15 = tk.Spinbox(labelframe2)
        self.spinbox15.configure(from_=0, to=99, textvariable=self.default[13],width=6)
        self.spinbox15.grid(column=3, row=2)
        self.spinbox16 = tk.Spinbox(labelframe2)
        self.spinbox16.configure(from_=0, to=99, textvariable=self.default[14],width=6)
        self.spinbox16.grid(column=3, row=3)
        self.spinbox17 = tk.Spinbox(labelframe2)
        self.spinbox17.configure(from_=0, to=99, textvariable=self.default[15],width=6)
        self.spinbox17.grid(column=3, row=4)
        self.spinbox18 = tk.Spinbox(labelframe2)
        self.spinbox18.configure(from_=0, to=99, textvariable=self.default[16],width=6)
        self.spinbox18.grid(column=3, row=5)
        self.spinbox19 = tk.Spinbox(labelframe2)
        self.spinbox19.configure(from_=0, to=99, textvariable=self.default[17],width=6)
        self.spinbox19.grid(column=3, row=6)
        labelframe2.grid(column=0, row=0)
        labelframe4 = ttk.Labelframe(frame5)
        labelframe4.configure(height=200, text='Execução', width=200)
        label10 = ttk.Label(labelframe4)
        label10.configure(text='Estado:  ')
        #label10.pack(expand=True, side="top")
        self.button2 = ttk.Button(labelframe4)
        self.button2.configure(text='Iniciar', command=self.iniciar)
        self.button2.pack(expand=True, side="top")
        self.button3 = ttk.Button(labelframe4)
        self.button3.configure(text='Parar/Reprogamar', command=self.parar)
        self.button3.pack(expand=True, side="top")
        button4 = ttk.Button(labelframe4)
        button4.configure(text='Voltar', command=self.desconectar)
        button4.pack(expand=True, side="top")
        labelframe4.grid(column=2, padx=25, row=0)
        labelframe4.pack_propagate(0)
        labelframe3 = ttk.Labelframe(frame5)
        labelframe3.configure(
            height=200,
            text='',
            width=200)
        self.text1 = tk.Text(labelframe3)
        self.text1.configure(height=10, state="disabled", width=50)
        self.text1.pack(padx=0, pady=0, side="top")
        labelframe3.grid(column=3, row=0)
        frame5.pack(side="top")
        self.frame6.grid(column=0, row=0)
        self.frame6.pack_propagate(0)

        #Carrega a ilustracao

        self.expiston = tk.PhotoImage(file='./assets/expiston.gif')
        self.piston = tk.PhotoImage(file='./assets/piston.gif')
        self.gndmet = tk.PhotoImage(file='./assets/gndmet.gif')
        self.medmet = tk.PhotoImage(file='./assets/medmet.gif')
        self.peqmet = tk.PhotoImage(file='./assets/peqnmet.gif')
        self.gndnmet = tk.PhotoImage(file='./assets/gndnmet.gif')
        self.mednmet = tk.PhotoImage(file='./assets/mednmet.gif')
        self.peqnmet = tk.PhotoImage(file='./assets/peqnmet.gif')
        self.peqmet_id = self.canvas1.create_image(0, 0, anchor=tk.NW, image=self.peqmet)
        self.medmet_id = self.canvas1.create_image(0, 0, anchor=tk.NW, image=self.medmet)
        self.gndmet_id = self.canvas1.create_image(0, 0, anchor=tk.NW, image=self.gndmet)
        self.gndnmet_id = self.canvas1.create_image(0, 0, anchor=tk.NW, image=self.gndnmet)
        self.mednmet_id = self.canvas1.create_image(0, 0, anchor=tk.NW, image=self.mednmet)
        self.peqnmet_id = self.canvas1.create_image(0, 0, anchor=tk.NW, image=self.peqnmet)
        self.piston1_id = self.canvas1.create_image(345, 15, anchor=tk.NW, image=self.piston)
        self.piston2_id = self.canvas1.create_image(575, 15, anchor=tk.NW, image=self.piston)
        self.piston3_id = self.canvas1.create_image(785, 15, anchor=tk.NW, image=self.piston)
        self.expiston1_id = self.canvas1.create_image(345, 15, anchor=tk.NW, image=self.expiston)
        self.expiston2_id = self.canvas1.create_image(575, 15, anchor=tk.NW, image=self.expiston)
        self.expiston3_id = self.canvas1.create_image(785, 15, anchor=tk.NW, image=self.expiston)


        self.belt = tk.PhotoImage(file='./assets/belt.gif')
        self.belt_moving_frames = self.load_gif_frames('./assets/belt_moving.gif')
        self.belt_id = self.canvas1.create_image(0, 0, anchor=tk.NW, image=self.belt)
        self.belt_moving_id = self.canvas1.create_image(0, 0, anchor=tk.NW, image=self.belt_moving_frames[0])
        self.frame_index = 0
        self.canvas1.tag_raise(self.piston1_id)
        self.canvas1.tag_raise(self.piston2_id)
        self.canvas1.tag_raise(self.piston3_id)
        self.canvas1.tag_raise(self.expiston1_id)
        self.canvas1.tag_raise(self.expiston2_id)
        self.canvas1.tag_raise(self.expiston3_id)
        self.canvas1.itemconfigure(self.expiston1_id, state=tk.HIDDEN)
        self.canvas1.itemconfigure(self.expiston2_id, state=tk.HIDDEN)
        self.canvas1.itemconfigure(self.expiston3_id, state=tk.HIDDEN)

        self.frame3.tkraise()

        # Main widget
        self.mainwindow = tk2

    def new_window(self, message):
        # Create a new window
        window = tk.Toplevel()
        window.title("Mensagem")

        # Set the size of the new window
        window.geometry("300x100")

        # Create a label to display the message
        label = tk.Label(window, text=message)
        label.pack(pady=15)

        # Create a button to close the new window
        close_button = tk.Button(window, text="Fechar", command=window.destroy)
        close_button.pack(pady=10)

    def load_gif_frames(self, file_path):
        frames = []
        image = tk.PhotoImage(file=file_path)
        try:
            i = 0
            while True:
                frames.append(image.subsample(1, 1).copy())
                i += 1
                image = tk.PhotoImage(file=file_path, format=f"gif -index {i}")
        except:
            pass
        return frames




    def run(self):
        self.update()
        self.mainwindow.mainloop()

    #Atualiza a interface
    def update(self):
        #if self.client_instance is not None:
        #    print(self.client_instance.finalizado)


        if not self.end_que.empty():
            if self.end_que.get() == 2:
                self.text1.configure(state="normal")
                self.text1.insert(tk.END, "Plano finalizado com sucesso\n")
                self.text1.see(tk.END)
                self.text1.configure(state="disabled")
                for value in range(18):
                    self.default[value].set(0)

        if self.thread_client is not None and self.thread_client.is_alive():
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
            self.button2.configure(state=tk.DISABLED)
            self.button3.configure(state=tk.NORMAL)
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
            self.button2.configure(state=tk.NORMAL)
            self.button3.configure(state=tk.DISABLED)

        # Informaçao sobre proxima peça a ser inserida e peça chegando
        if self.client_instance is not None:
            new_precondition_dict = self.client_instance.getprecondition_dict()
            new_table = self.client_instance.get_table()
            pecas = ['peca_peqnmet', 'peca_peqmet', 'peca_mednmet', 'peca_medmet', 'peca_grdnmet', 'peca_grdmet']
            for key in pecas:
                if key not in self.precondition_dict and key in new_precondition_dict:
                    self.text1.configure(state="normal")
                    self.text1.insert(tk.END, "Insira a próxima peça: ")
                    match key:
                        case 'peca_peqnmet':
                            self.text1.insert(tk.END, "Pequena não Metálica\n")
                        case 'peca_peqmet':
                            self.text1.insert(tk.END, "Pequena Metálica\n")
                        case 'peca_mednmet':
                            self.text1.insert(tk.END, "Média não Metálica\n")
                        case 'peca_medmet':
                            self.text1.insert(tk.END, "Média Metálica\n")
                        case 'peca_grdnmet':
                            self.text1.insert(tk.END, "Grande não Metálica\n")
                        case 'peca_grdmet':
                            self.text1.insert(tk.END, "Grande Metálica\n")
                    self.text1.see(tk.END)
                    self.text1.configure(state="disabled")

                #Identifica nova peça detectada
                if key in self.table and key in new_table:
                    if self.table[key] is False and new_table[key] is True:
                        self.pecas_que.put(key)
                        self.text1.configure(state="normal")
                        match key:
                            case 'peca_peqnmet':
                                self.text1.insert(tk.END, "Peça detectada: Pequena não Metálica\n")
                            case 'peca_peqmet':
                                self.text1.insert(tk.END, "Peça detectada: Pequena Metálica\n")
                            case 'peca_mednmet':
                                self.text1.insert(tk.END, "Peça detectada: Média não Metálica\n")
                            case 'peca_medmet':
                                self.text1.insert(tk.END, "Peça detectada: Média Metálica\n")
                            case 'peca_grdnmet':
                                self.text1.insert(tk.END, "Peça detectada: Grande não Metálica\n")
                            case 'peca_grdmet':
                                self.text1.insert(tk.END, "Peça detectada: Grande Metálica\n")
                        self.text1.configure(state="disabled")

            #Detecta peça chegando na caixa de descarte
            fc = ['fc_1', 'fc_2', 'fc_3', 'fc_4']
            for key in fc:
                if key in self.table and key in new_table:
                    if self.table[key] is False and new_table[key] is True and not self.pecas_que.empty():
                        self.text1.configure(state="normal")
                        self.text1.insert(tk.END, "Peça recebida na caixa ")
                        peca = self.pecas_que.get()
                        match key:
                            case 'fc_1':
                                self.text1.insert(tk.END, "1\n")
                                self.caixa_descarte1[peca] = self.caixa_descarte1[peca] + 1
                                #s =('peça '+ peca + 'chegou na caixa1\n')
                                #self.text1.insert(tk.END, s)
                                #s = ('quantidade de pecas do tipo ' + peca + ' na caixa 1:' + str(self.caixa_descarte1[peca])+'\n')
                                #self.text1.insert(tk.END, s)
                            case 'fc_2':
                                self.text1.insert(tk.END, "2\n")
                                self.caixa_descarte2[peca] = self.caixa_descarte2[peca] + 1
                                #s =('peça ' + peca + 'chegou na caixa2')
                                #self.text1.insert(tk.END, s)
                                #s = ('quantidade de pecas do tipo ' + peca + ' na caixa 2:' + str(self.caixa_descarte2[peca])+'\n')
                                #self.text1.insert(tk.END, s)
                            case 'fc_3':
                                self.text1.insert(tk.END, "3\n")
                                self.caixa_descarte3[peca] = self.caixa_descarte3[peca] + 1
                                #s = ('peça ' + peca + 'chegou na caixa3')
                                #self.text1.insert(tk.END, s)
                                #s = ('quantidade de pecas do tipo ' + peca + ' na caixa 3:' + str(self.caixa_descarte3[peca])+'\n')
                                self.text1.insert(tk.END, s)
                            case 'fc_4':
                                self.text1.insert(tk.END, "4\n")
                                self.caixa_descarte4[peca] = self.caixa_descarte4[peca] + 1
                                #s = ('peça ' + peca + 'chegou na caixa4')
                                #self.text1.insert(tk.END, s)
                                #s = ('quantidade de pecas do tipo ' + peca + ' na caixa 4:' + str(self.caixa_descarte4[peca])+'\n')
                                #self.text1.insert(tk.END, s)
                                self.descartando_pecaincorreta = False
                        self.text1.configure(state="disabled")

            '''
            #Detecta peça incorreta inserida
            if not self.pecas_que.empty():
                if self.pecas_que.queue[0] in self.table and not self.descartando_pecaincorreta:
                    #if self.table[self.pecas_que.queue[0]] is True:
                    pecas = ['peca_peqnmet', 'peca_peqmet', 'peca_mednmet', 'peca_medmet', 'peca_grdnmet', 'peca_grdmet']
                    pecas_err = [item for item in pecas if item != self.pecas_que.queue[0]]
                    for key3 in pecas_err:
                        if self.table[key3] is True:
                            self.text1.configure(state="normal")
                            self.text1.insert(tk.END, "Peça incorreta. Descartando.\n")
                            self.text1.configure(state="disabled")
                            self.descartando_pecaincorreta = True
            '''
            # Detecta peça incorreta inserida
            pecas = ['peca_peqnmet', 'peca_peqmet', 'peca_mednmet', 'peca_medmet', 'peca_grdnmet', 'peca_grdmet']
            for key3 in pecas:
                if key3 in self.precondition_dict:
                    pecas_err = [item for item in pecas if item != key3]
                    for key4 in pecas_err:
                        if self.table[key4] is True and not self.descartando_pecaincorreta:
                            self.text1.configure(state="normal")
                            self.text1.insert(tk.END, "Peça incorreta. Descartando.\n")
                            self.text1.see(tk.END)
                            self.text1.configure(state="disabled")
                            self.descartando_pecaincorreta = True

            self.table = new_table
            self.precondition_dict = new_precondition_dict

        self.UpdateCanvas()



        '''
        if self.thread_client is not None:
            if self.thread_client.is_alive() and self.client_instance.client.connected:
                self.frame6.tkraise()
            else:
                self.frame3.tkraise()
        else :
            self.frame3.tkraise()
        '''
        #if self.f1:
        #    self.frame3.tkraise()
        #else:
        #    self.frame6.tkraise()

        #self.f1 = not self.f1
        #print(threading.enumerate(),'\n')



        self.mainwindow.after(50, self.update)



    def conectar(self):
        entered_value = self.entry.get()
        #print('entered value:', entered_value)
        if entered_value != "":
            self.ip = entered_value
            self.frame6.tkraise()
        else:
            self.new_window('Endereço invalido')
        #self.client_instance.enable()
        #self.thread_client.start()
        #self.thread_client()
        #self.table = self.instance.prog.table

    def iniciar(self):
        try:
            self.client_instance = Main_program_ThreadClient(self.ip)
        except Exception as err:
            print('Erro: Não foi possível conectar ao enderço do controlador.')
            self.new_window('Erro: Não foi possível conectar ao enderço do controlador.')
            raise err
        self.generate_problem()
        self.client_instance.enable()
        self.text1.configure(state="normal")
        self.text1.insert(tk.END, "Iniciando\n")
        self.text1.see(tk.END)
        self.text1.configure(state="disabled")
        #self.thread_client = threading.Thread(target=lambda a: a.run(), args=([self.client_instance]))
        self.thread_client = threading.Thread(target=lambda q, a: q.put(a.run()), args=(self.end_que, self.client_instance))
        self.thread_client.start()

    def parar(self):
        self.client_instance.stop1()
        #self.conectar()
        self.text1.configure(state="normal")
        self.text1.insert(tk.END, "Parando\n")
        self.text1.see(tk.END)
        self.text1.configure(state="disabled")
        while not self.pecas_que.empty():
            self.pecas_que.get()
    def desconectar(self):
        if self.client_instance is not None:
            self.client_instance.stop1()
        self.frame3.tkraise()

    def generate_problem(self):
        # Armazena as informacoes sobre o problema desejado
        items = {
            'cx1_peq_metal': int(self.spinbox2.get()) - self.caixa_descarte1['peca_peqmet'],
            'cx1_med_metal': int(self.spinbox3.get()) - self.caixa_descarte1['peca_medmet'],
            'cx1_grd_metal': int(self.spinbox4.get()) - self.caixa_descarte1['peca_grdmet'],
            'cx1_peq': int(self.spinbox5.get()) - self.caixa_descarte1['peca_peqnmet'],
            'cx1_med': int(self.spinbox6.get()) - self.caixa_descarte1['peca_mednmet'],
            'cx1_grd': int(self.spinbox7.get()) - self.caixa_descarte1['peca_grdnmet'],

            'cx2_peq_metal': int(self.spinbox8.get()) - self.caixa_descarte2['peca_peqmet'],
            'cx2_med_metal': int(self.spinbox9.get()) - self.caixa_descarte2['peca_medmet'],
            'cx2_grd_metal': int(self.spinbox10.get()) - self.caixa_descarte2['peca_grdmet'],
            'cx2_peq': int(self.spinbox11.get()) - self.caixa_descarte2['peca_peqnmet'],
            'cx2_med': int(self.spinbox12.get()) - self.caixa_descarte2['peca_mednmet'],
            'cx2_grd': int(self.spinbox13.get()) - self.caixa_descarte2['peca_grdnmet'],

            'cx3_peq_metal': int(self.spinbox14.get()) - self.caixa_descarte3['peca_peqmet'],
            'cx3_med_metal': int(self.spinbox15.get()) - self.caixa_descarte3['peca_medmet'],
            'cx3_grd_metal': int(self.spinbox16.get()) - self.caixa_descarte3['peca_grdmet'],
            'cx3_peq': int(self.spinbox17.get()) - self.caixa_descarte3['peca_peqnmet'],
            'cx3_med': int(self.spinbox18.get()) - self.caixa_descarte3['peca_mednmet'],
            'cx3_grd': int(self.spinbox19.get()) - self.caixa_descarte3['peca_grdnmet']
        }
        for key in items:
            if items[key] < 0:
                items[key]=0

        # Gerando o problema a partir das informacoes inseridas
        lines = []
        #for keys in items:
            #items[keys] = int(items[keys])

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

    def UpdateCanvas(self):
        if self.client_instance is not None:
            table = self.client_instance.get_table()
            if table['liga_esteira'] and self.thread_client.is_alive():
                self.canvas1.itemconfigure(self.belt_id, state=tk.HIDDEN)
                self.canvas1.itemconfig(self.belt_moving_id, image=self.belt_moving_frames[self.frame_index])
                self.frame_index = (self.frame_index + 1) % len(self.belt_moving_frames)
                self.canvas1.itemconfigure(self.belt_moving_id, state=tk.NORMAL)
            else:
                self.canvas1.itemconfigure(self.belt_moving_id, state=tk.HIDDEN)
                self.canvas1.itemconfigure(self.belt_id, state=tk.NORMAL)

            if table['anvanca_ap1']:
                self.canvas1.itemconfigure(self.expiston1_id, state=tk.NORMAL)
                self.canvas1.itemconfigure(self.piston1_id, state=tk.HIDDEN)
            else:
                self.canvas1.itemconfigure(self.expiston1_id, state=tk.HIDDEN)
                self.canvas1.itemconfigure(self.piston1_id, state=tk.NORMAL)

            if table['anvanca_ap2']:
                self.canvas1.itemconfigure(self.expiston2_id, state=tk.NORMAL)
                self.canvas1.itemconfigure(self.piston2_id, state=tk.HIDDEN)
            else:
                self.canvas1.itemconfigure(self.expiston2_id, state=tk.HIDDEN)
                self.canvas1.itemconfigure(self.piston2_id, state=tk.NORMAL)

            if table['anvanca_ap3']:
                self.canvas1.itemconfigure(self.expiston3_id, state=tk.NORMAL)
                self.canvas1.itemconfigure(self.piston3_id, state=tk.HIDDEN)
            else:
                self.canvas1.itemconfigure(self.expiston3_id, state=tk.HIDDEN)
                self.canvas1.itemconfigure(self.piston3_id, state=tk.NORMAL)


if __name__ == "__main__":
    app = aUI()
    app.run()
