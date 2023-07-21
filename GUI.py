#!/usr/bin/python3

import sys
sys.path.insert(0, './Lib/site-packages')

import tkinter as tk
import tkinter.ttk as ttk
from program import program
import threading

class ThreadClient(threading.Thread):
    def __init__(self,ip):
        threading.Thread.__init__(self)
        self.prog = program(ip)
    def run(self):
        self.prog.run()


class GUI:


    def __init__(self, master=None):

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

        # build ui

        toplevel1 = tk.Tk() if master is None else tk.Toplevel(master)
        default = []
        for x in range(18):
            default.append(tk.IntVar(toplevel1, 0))


        toplevel1.configure(width=200)
        toplevel1.geometry("1024x600")
        #default = tk.IntVar(toplevel1, 0)
        self.frame1 = tk.Frame(toplevel1)
        self.frame1.configure(height=600, width=1024)
        self.frame55 = tk.Frame(self.frame1)
        self.entry3 = tk.Entry(self.frame55)
        self.entry3.grid(column=0, row=1)
        button2 = tk.Button(self.frame55, command=self.conectar)
        button2.configure(text='Conectar')
        button2.grid(column=0, row=2)
        label3 = tk.Label(self.frame55)
        label3.configure(text='Insira o endereço de IP')
        label3.grid(column=0, row=0)
        self.frame55.grid(column=0, ipadx=40, ipady=10, row=0)
        self.frame55.grid_anchor("center")
        self.frame1.grid(column=0, row=0)
        self.frame1.grid_propagate(0)
        self.frame1.grid_anchor("center")
        self.frame2 = tk.Frame(toplevel1)
        self.frame2.configure(height=600, width=1024)
        self.frame22 = tk.Frame(self.frame2)
        self.frame22.configure(height=350, width=700)
        canvas1 = tk.Canvas(self.frame22)
        canvas1.configure(height=350, width=700)
        canvas1.pack(side="top")
        self.frame22.grid(column=0, padx=10, pady=10, row=0)
        self.frame23 = tk.Frame(self.frame2)
        self.frame23.configure(height=175, width=700)
        frame3 = tk.Frame(self.frame23)
        frame3.configure(height=200, width=200)
        label1 = tk.Label(frame3)
        label1.configure(text='Met Peq')
        label1.grid(column=0, row=0)
        spinbox8 = tk.Spinbox(frame3)
        spinbox8.configure(from_=0, to=99, textvariable=default[0],width=6)
        spinbox8.grid(column=1, pady=2, row=0)
        label2 = tk.Label(frame3)
        label2.configure(text='Met Med')
        label2.grid(column=0, row=2)
        spinbox9 = tk.Spinbox(frame3)
        spinbox9.configure(from_=0, to=99, textvariable=default[1],width=6)
        spinbox9.grid(column=1, row=2)
        label4 = tk.Label(frame3)
        label4.configure(text='Met Grd')
        label4.grid(column=0, row=4)
        spinbox10 = tk.Spinbox(frame3)
        spinbox10.configure(from_=0, to=99, textvariable=default[2],width=6)
        spinbox10.grid(column=1, pady=2, row=4)
        label5 = tk.Label(frame3)
        label5.configure(text='Nao Met P')
        label5.grid(column=0, row=6)
        spinbox12 = tk.Spinbox(frame3)
        spinbox12.configure(from_=0, to=99, textvariable=default[3],width=6)
        spinbox12.grid(column=1, row=6)
        label6 = tk.Label(frame3)
        label6.configure(text='Nao Met M')
        label6.grid(column=0, row=8)
        spinbox13 = tk.Spinbox(frame3)
        spinbox13.configure(from_=0, to=99, textvariable=default[4],width=6)
        spinbox13.grid(column=1, pady=2, row=8)
        label7 = tk.Label(frame3)
        label7.configure(text='Nao Met G')
        label7.grid(column=0, row=10)
        spinbox15 = tk.Spinbox(frame3)
        spinbox15.configure(from_=0, to=99, textvariable=default[5],width=6)
        spinbox15.grid(column=1, row=10)
        frame3.grid(column=0, ipadx=5, row=1)
        frame4 = tk.Frame(self.frame23)
        frame4.configure(height=200, width=200)
        label8 = tk.Label(frame4)
        label8.configure(text='Met Peq')
        label8.grid(column=0, row=0)
        spinbox1 = tk.Spinbox(frame4)
        spinbox1.configure(from_=0, to=99, textvariable=default[6],width=6)
        spinbox1.grid(column=1, pady=2, row=0)
        label9 = tk.Label(frame4)
        label9.configure(text='Met Med')
        label9.grid(column=0, row=2)
        spinbox2 = tk.Spinbox(frame4)
        spinbox2.configure(from_=0, to=99, textvariable=default[7],width=6)
        spinbox2.grid(column=1, row=2)
        label10 = tk.Label(frame4)
        label10.configure(text='Met Grd')
        label10.grid(column=0, row=4)
        spinbox3 = tk.Spinbox(frame4)
        spinbox3.configure(from_=0, to=99, textvariable=default[8],width=6)
        spinbox3.grid(column=1, pady=2, row=4)
        label11 = tk.Label(frame4)
        label11.configure(text='Nao Met P')
        label11.grid(column=0, row=6)
        spinbox4 = tk.Spinbox(frame4)
        spinbox4.configure(from_=0, to=99, textvariable=default[9],width=6)
        spinbox4.grid(column=1, row=6)
        label12 = tk.Label(frame4)
        label12.configure(text='Nao Met M')
        label12.grid(column=0, row=8)
        spinbox5 = tk.Spinbox(frame4)
        spinbox5.configure(from_=0, to=99, textvariable=default[10],width=6)
        spinbox5.grid(column=1, pady=2, row=8)
        label13 = tk.Label(frame4)
        label13.configure(text='Nao Met G')
        label13.grid(column=0, row=10)
        spinbox6 = tk.Spinbox(frame4)
        spinbox6.configure(from_=0, to=99, textvariable=default[11],width=6)
        spinbox6.grid(column=1, row=10)
        frame4.grid(column=1, ipadx=5, row=1)
        frame5 = tk.Frame(self.frame23)
        frame5.configure(height=200, width=200)
        label14 = tk.Label(frame5)
        label14.configure(text='Met Peq')
        label14.grid(column=0, row=0)
        spinbox7 = tk.Spinbox(frame5)
        spinbox7.configure(from_=0, to=99, textvariable=default[12],width=6)
        spinbox7.grid(column=1, pady=2, row=0)
        label15 = tk.Label(frame5)
        label15.configure(text='Met Med')
        label15.grid(column=0, row=2)
        spinbox11 = tk.Spinbox(frame5)
        spinbox11.configure(from_=0, to=99, textvariable=default[13],width=6)
        spinbox11.grid(column=1, row=2)
        label16 = tk.Label(frame5)
        label16.configure(text='Met Grd')
        label16.grid(column=0, row=4)
        spinbox14 = tk.Spinbox(frame5)
        spinbox14.configure(from_=0, to=99, textvariable=default[14],width=6)
        spinbox14.grid(column=1, pady=2, row=4)
        label17 = tk.Label(frame5)
        label17.configure(text='Nao Met P')
        label17.grid(column=0, row=6)
        spinbox16 = tk.Spinbox(frame5)
        spinbox16.configure(from_=0, to=99, textvariable=default[15],width=6)
        spinbox16.grid(column=1, row=6)
        label18 = tk.Label(frame5)
        label18.configure(text='Nao Met M')
        label18.grid(column=0, row=8)
        spinbox17 = tk.Spinbox(frame5)
        spinbox17.configure(from_=0, to=99, textvariable=default[16],width=6)
        spinbox17.grid(column=1, pady=2, row=8)
        label19 = tk.Label(frame5)
        label19.configure(text='Nao Met G')
        label19.grid(column=0, row=10)
        spinbox18 = tk.Spinbox(frame5)
        spinbox18.configure(from_=0, to=99, textvariable=default[17], width=6)
        spinbox18.grid(column=1, row=10)
        frame5.grid(column=2, ipadx=5, row=1)
        frame8 = tk.Frame(self.frame23)
        frame8.configure(height=200, width=200)
        button5 = tk.Button(frame8)
        button5.configure(text='Iniciar',command=self.iniciar)
        button5.pack(side="top")
        button6 = tk.Button(frame8)
        button6.configure(text='Parar/Reprogramar')
        button6.pack(side="top")
        button7 = tk.Button(frame8)
        button7.configure(text='Desconectar')
        button7.pack(side="top")
        frame8.grid(column=3, padx=40, row=1)
        label24 = tk.Label(self.frame23)
        label24.configure(text='Caixa de descarte 1')
        label24.grid(column=0, row=0)
        label25 = tk.Label(self.frame23)
        label25.configure(text='Caixa de descarte 2')
        label25.grid(column=1, row=0)
        label26 = tk.Label(self.frame23)
        label26.configure(text='Caixa de descarte 3')
        label26.grid(column=2, row=0)
        self.frame23.grid(column=0, padx=1, pady=1, row=1)
        self.frame23.grid_propagate(0)
        self.frame24 = tk.Frame(self.frame2)
        self.frame24.configure(height=350, width=250)
        canvas2 = tk.Canvas(self.frame24)
        canvas2.configure(height=350, width=250)
        canvas2.pack(side="top")
        self.frame24.grid(column=1, padx=10, pady=10, row=0)
        self.frame25 = tk.Frame(self.frame2)
        self.frame25.configure(height=125, width=250)
        label27 = tk.Label(self.frame25)
        label27.configure(text='label27')
        label27.pack(side="top")
        label28 = tk.Label(self.frame25)
        label28.configure(text='label28')
        label28.pack(side="top")
        label29 = tk.Label(self.frame25)
        label29.configure(text='label29')
        label29.pack(side="top")
        self.frame25.grid(column=1, row=1)
        self.frame25.pack_propagate(0)
        self.frame2.grid(column=0, row=0)
        self.frame2.grid_propagate(0)
        self.frame2.grid_anchor("center")
        toplevel1.grid_anchor("center")

        # Main widget
        self.frame1.tkraise()
        self.mainwindow = toplevel1

    def run(self):
        self.mainwindow.after(0, self.update)
        self.mainwindow.mainloop()

    def conectar(self):
        entered_value = self.entry3.get()
        print(entered_value)
        self.instance = ThreadClient(entered_value)
        self.instance.start()
        self.table = self.instance.prog.table

    def iniciar(self):
        self.instance.prog.start = True


    def update(self):
        print("teste")

        #time.sleep(rand.random() * 1.5)


        if hasattr(self, 'instance'):
            if(self.instance.is_alive()):
                self.frame2.tkraise()
            else:
                self.frame1.tkraise()
        else:
            self.frame1.tkraise()

        #match(self.table['anvanca_ap1']):
            #case True: self.label32.configure(background='green')
            #case False: self.label32.configure(background='red')

        self.mainwindow.after(200, self.update)





if __name__ == "__main__":
    app = GUI()
    app.run()
