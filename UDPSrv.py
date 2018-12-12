from socket import *
import time
continua = False
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
proximo = 0
print 'The server is ready to receive'
while 1:
    message, clientAddress = serverSocket.recvfrom(2048)
    print message
    msgNumber, dado = message.split('/')
    resposta = msgNumber
    if int(resposta) == int(15):
        time.sleep(5)
    if (continua or int(resposta) != int(5)) and int(resposta) == proximo:
        serverSocket.sendto(resposta, clientAddress)
        proximo = int(resposta) + 1
    else:
        print 'mensagem perdida'
        continua = True
    time.sleep(1)
