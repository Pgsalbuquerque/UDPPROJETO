from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread
from time import sleep
import random

class QuisUDP:
    def __init__(self):
        self.pessoas = 0
        self.dic = {}
        self.starting = False
        self.questions = None
        self.acertou = False
        self.timeout = False
        self.questions_array = self.generated_array_questions()
        host = '25.94.168.61'
        port = 3333
        self.udp = socket(AF_INET, SOCK_DGRAM)
        serv = (host, port)
        self.udp.bind(serv)
        print("servidor rodando")
        self.thread_start()
        while True:
            data, client = self.udp.recvfrom(2048)
            Thread(target=self.avaliar, args=(data, client)).start()
        udp.close()

    def generated_array_questions(self):
        Bd = open('Pergunta.csv', 'r')
        questions = Bd.readlines()
        for x in range(0, len(questions)):
            questions[x] = questions[x].replace('\n', '').lower().split(',')
        Bd.close()
        return questions

    def thread_start(self):
        Thread(target=self.check_five).start()

    def check_five(self):
        while True:
            if self.pessoas == 1: #se quiser colocar menos pessoas
                self.start()
                break

    def start(self):
        generation_array = []
        while len(generation_array) < 5:
            r = random.randint(0, 19)
            if r not in generation_array:
                generation_array.append(r)
        for x in range(0, 5):
            self.send_question(x, generation_array[x])
            self.acertou = False
            self.starting = True
            self.timeout = False
            self.questions = generation_array[x]
            Thread(target=self.timercount, args=(generation_array[x],)).start()
            while True:
                if self.acertou == True:
                    break
                if self.timeout == True:
                    break
            self.atualizar_rank()
            self.send_rank()
        self.reset()

    def reset(self):
        self.pessoas = 0
        self.dic = {}
        self.starting = False
        self.questions = None
        self.acertou = False
        self.timeout = False
        self.thread_start()
        
    def atualizar_rank(self):
        for x in self.dic.keys():
            if self.dic[x][1] == False:
                self.dic[x][0] -= 1
            self.dic[x][1] = False

    def send_rank(self):
        st = ''
        for x in self.dic.keys():
            st += f'Player {x} ---> pontuacao: {self.dic[x][0]}\n'
        for x in self.dic.keys():
            self.udp.sendto(f'{st}'.encode(), x)

    def timercount(self, questions_atually):
        sleep(10) #se quiser aumentar o tempo
        if self.questions != questions_atually:
            pass
        else:
            self.timeout = True

    def checkResposta(self, data, client):
        if self.acertou == True:
            return
        x = data
        x = x[25:]
        if x == self.questions_array[self.questions][1]:
            self.dic[client][0] += 25
            self.dic[client][1] = True
            self.acertou = True
        elif x != self.questions_array[self.questions][1]:
            self.dic[client][0] -= 5
            self.dic[client][1] = True

    def send_question(self, number, question_index):
        for x in self.dic.keys():
            self.udp.sendto(f'Questão {number +1}: {self.questions_array[question_index][0]}'.encode(), x)
    
    def avaliar(self, data, client):
        # string valida ----> "QUIZ / 1.0 /\\r\\nreq:p" pedindo pra particiar
        # string valida ----> "QUIZ / 1.0 /\\r\\nreq:a\\r\\n{asdasd}" mandando resposta
        data = data.decode()
        if len(data) < 21:
            self.udp.sendto('Status: 400\r\nBAD REQUEST'.encode(), client)
            print('a')
            return
        if data[0:20] != "QUIZ / 1.0 /\\r\\nreq:":
            self.udp.sendto('Status: 400\r\nBAD REQUEST'.encode(), client)
            print('b')
            return
        if data[20] != 'p' and data[20] != 'a':
            self.udp.sendto('Status: 400\r\nBAD REQUEST'.encode(), client)
            print('c')
            return
        if data[20] == 'a' and len(data) <= 25:
            self.udp.sendto('Status: 400\r\nBAD REQUEST'.encode(), client)
            print('d')
            return
        if data[20] == 'p' and len(data) == 21:
            self.jogar(data,client)
            return
        
        if data[20] == 'a':
            if self.pessoas == 1: #se quiser colocar menos pessoas
                    if client in self.dic:
                        self.checkResposta(data, client)
                    else:
                        self.udp.sendto('Já tem uma rodada em andamento, tente novamente depois'.encode(), client)
            else:
                if client in self.dic:
                    self.udp.sendto('A rodada ainda não começou'.encode(), client)
                else:
                    self.udp.sendto('Você ainda nn foi cadastrado, mande a flag "p" para participar'.encode(), client)
    def jogar(self, data,client):
        if client in self.dic:
            self.udp.sendto('Você já está participando'.encode(), client)
        else:
            if len(self.dic) == 1: #se quiser colocar menos pessoas
                self.udp.sendto('Rodada já está em andamento, tente novamente depois'.encode(), client)
            else:
                self.dic[client] = [0, False]
                self.pessoas += 1
                self.udp.sendto('Você foi cadastrado para essa rodada, aguarde...'.encode(), client)


QuisUDP()
