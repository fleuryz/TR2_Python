from socket import *
import time
import threading
import random

class Conexao(threading.Thread):
    def __init__(self, clientAddress, serverSocket, mensagem, timeout):
        threading.Thread.__init__(self)
        self.endereco = clientAddress
        self.proxima = 1
        self.serverConexao = serverSocket
        self.continuar = 1
        self.mensagemFinal = ''
        #self.serverConexao.sendto('0', self.endereco)
        self.tempo = time.time()
        self.tempo2 = time.time()
        self.timeout = timeout
        self.encerrar = 10
        self.resposta = '0'
        self.trata = False
        print 'Cliente conectado: ' + str(self.endereco)
    
    def run(self):
        self.serverConexao.sendto(self.resposta, self.endereco)
        while self.continuar:
            if time.time() - self.tempo >= self.timeout:
                self.tempo = time.time()
                print 'Reenvio de Ack(' + str(self.endereco) + '): ' + self.resposta
                try:
                    self.serverConexao.sendto(self.resposta, self.endereco)
                except socket_error as msg:
                    print msg
                time.sleep(0.1)
            self.continuar =  (time.time() - self.tempo2 <= self.encerrar) and self.continuar
        print 'Encerrando por timeout de encerrar: ' + str(self.endereco)

    def tratar(self, mensagem):
        self.trata = False
        self.tempo2 = time.time()
        print 'Mensagem recebida: ' + mensagem
        numMsg, dado = mensagem.split('/')
        self.resposta = numMsg
        if self.proxima == int(numMsg):
            if random.randint(0,9) == 0:
                print 'Perdeu uma mensagem do servidor ao cliente'
            else:
                self.serverConexao.sendto(self.resposta, self.endereco)
            print 'Envio de Ack: ' + self.resposta
            self.proxima += 1
            self.mensagemFinal += dado
            self.tempo = time.time()
            return False
        elif int(numMsg) == -1:
            self.serverConexao.sendto('-1/Ack', self.endereco)
            self.continuar = False
            print 'Fechando conexao.'
            print 'Mensagem recebida: ' + self.mensagemFinal
            return True
        else:
            self.serverConexao.sendto(str(self.proxima-1),self.endereco)
            print 'Reenviando Ack ja enviado: ' + self.resposta


continua = False
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
proximo = 0
conexoes = []
novo = 1
timeout = 0.1

print 'Servidor pronto.'
while 1:
    message, clientAddress = serverSocket.recvfrom(2048)
    if message == 'encerrar':
        break
    if message == '0/connect':
        conexao = Conexao(clientAddress, serverSocket, message, timeout)
        conexoes += [conexao]
        conexao.start()
    elif random.randint(0,9) != 0:
        for i in conexoes:
            if i.endereco == clientAddress:
                fechar = i.tratar(message)
                if fechar:
                    conexoes.remove(i)
    else:
        print 'Perdeu uma mensagem do cliente para o servidor'
for i in conexoes:
    i.join()

print 'Fechando servidor'
