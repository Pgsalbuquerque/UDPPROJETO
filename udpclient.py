import socket
from threading import Thread
from time import sleep
from tkinter import *


class Client:
    def __init__(self):
        self.root = Tk()
        self.root.title("UDP CLIENT")
        self.root.geometry("1000x600")
        #self.root.iconbitmap("C:\\Users\\pdr\\Documents\\repos\\TCPPROJETO\\favicon.ico")

        self.HOST = '25.94.168.61'
        self.PORT = 3333
        self.Host_Client = '25.94.168.61'
        self.Port_Client = 4444
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp.bind((self.Host_Client, self.Port_Client))
        self.dest = (self.HOST, self.PORT)
        
        L1 = Label(self.root, text="Resposta")
        L1.grid(row=1, column=0, pady=20)
        L1.pack()

        self.E1 = Entry(self.root)
        self.E1.pack()

        button = Button(self.root, text="enviar resposta", command=self.send)
        button.pack()

        button2 = Button(self.root, text="participar", command=self.participar)
        button2.pack()

        Thread(target=self.listen).start()

        self.root.mainloop()
        
    def participar(self):
        self.udp.sendto("QUIZ / 1.0 /\\r\\nreq:p".encode(), self.dest)

    def listen(self):
        while True:
            data, servidor = self.udp.recvfrom(2048)
            l = Label(self.root, text=f'O Servidor {servidor} mandou >>>> {data.decode()}')
            l.pack()
            l.after(10000, l.destroy)
        self.udp.close()
        
    def send(self):
        msg = "QUIZ / 1.0 /\\r\\nreq:a\\r\\n" + self.E1.get()
        self.udp.sendto(msg.encode(), self.dest)

        

Client()
