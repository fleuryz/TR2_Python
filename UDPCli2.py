from socket import *
from socket import error as socket_error
import time
import random

def separarMensagem (numStr, mensagem):
    retorno = []
    for i in range(0, len(mensagem), numStr):
        retorno.append(str((i/numStr)+1) + separador + mensagem[i:i+numStr])
    
    return retorno, i/numStr

serverName = ''
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(0.1)
separador = '/'
mensNum = 1
mensAck = -1
comecoJanela = 0
tamanhoJanela = 2
tempoRec = 0.1
reduzir = True
i = 0
mensagemTotal = ['Essa mensagem e um teste para verificar a funcionalidade deste codigo.', 'Essa e uma segunda mensagem de teste.']
dado, mensTotal = separarMensagem(random.randint(1,4), mensagemTotal[random.randint(0,1)])
mensTotal += 2
tempoTotal = time.time()
clientSocket.sendto('0/connect', (serverName, serverPort))
while True:
    try:
        mensAck, serverAddress = clientSocket.recvfrom(2048)
        if mensAck == '0':
            print 'Conectado ao Servidor'
            break
    except socket_error as msg:
        print msg
        print 'Sem ACK de conexao'
        clientSocket.sendto('0/connect', (serverName, serverPort))

while int(mensAck) < (int(mensTotal) - 1):
    tempoEnvio = time.time()
    while (mensNum < comecoJanela + tamanhoJanela) and mensNum < mensTotal:
        mensagemEnvio = str(dado[int(mensNum)-1])
        print 'Envio de mensagem: ' + mensagemEnvio
        try:
            clientSocket.sendto(mensagemEnvio, (serverName, serverPort) )
        except socket_error as msg:
            print msg
        mensNum += 1

    tempoEnvio = (time.time() - tempoEnvio)/tamanhoJanela
    tempo = time.time()

    while 1:
        try:
            mensAck, serverAddress = clientSocket.recvfrom(2048)
            tempo = time.time() - tempo
            if int(mensAck) >= comecoJanela:
                print 'Recebido Ack: ' + mensAck
                comecoJanela = int(mensAck) + 1
        except socket_error as msg:
            print msg
            print 'Sem ACK: ' + str(comecoJanela)
            mensNum = comecoJanela
            break
clientSocket.sendto('-1/',(serverName, serverPort))


while True:
    try:
        mensAck, serverAddress = clientSocket.recvfrom(2048)
        if mensAck == '-1/Ack':
            print 'Encerrar conexao'
            break
    except socket_error as msg:
        print msg
        clientSocket.sendto('-1/',(serverName, serverPort))
        print 'Sem ACK de finalizacao'

tempoTotal= time.time() - tempoTotal
clientSocket.close()
vazao = mensTotal/tempoTotal

print 'Vazao total de ' + str(vazao) + ' mensagens por segundo.'
