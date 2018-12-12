from socket import *
from socket import error as socket_error
import time
serverName = '' 
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)

clientSocket.sendto('encerrar',(serverName, serverPort))

clientSocket.close()
