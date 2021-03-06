# coding=utf-8
'''
Created on 20170224

@author: WLX
'''
import logging

from Infrastructure.Communication.MessageRule import MESSAGE, SERVER_PORT, \
    ALL_IP_OF_HOST, CLIENT_PORT
from Infrastructure.Communication.NetUdpBase import NetUdpBase


logging.basicConfig(level=logging.DEBUG)


class Client(NetUdpBase):
    '''
    Client for communication
    '''

    def __init__(self, host, port, name):
        '''
        Constructor
        '''
        super(Client, self).__init__(host, port)
        self._name = name
        self._serverHost = None
        self._socket_recv.bind((ALL_IP_OF_HOST, CLIENT_PORT))
        self._socket_send.bind((ALL_IP_OF_HOST, SERVER_PORT))

    def registerClient(self, serverHost):
        serverAddr = (serverHost, SERVER_PORT)
        try:
            self._sendMessage(MESSAGE["ClientRegister"].format(self._name), serverAddr)
            logging.info("send message {0}".format(MESSAGE["ClientRegister"].format(self._name)))
        except Exception:
            logging.info("send message{0} fail".format(MESSAGE["ClientRegister"].format(self._name)))
            return False
        while True:
            data, addr = self._socket_recv.recvfrom(1024)
            logging.info("waiting for message ---")
            print data, addr
            if addr[0] == serverHost and data == MESSAGE["RegisterSucc"].format(self._name):
                logging.info("Client:{0} Register Success".format(self._name))
                self._serverHost = serverHost
                return True
            else:
                logging.info("Client:{0} Register Failure:{1}".format(self._name, data))
                return False

    def _recvMessage(self, dataQueue, addrQueue):
        while True:
            data, addr = self._socket_recv.recvfrom(1024)
            if self._precheck(addr[0]):
                logging.info("Message:{0}".format(data))
                dataQueue.put(data)
                addrQueue.put(addr[0])

    def _precheck(self, host):
        if host == self._serverHost:
            return True
        else:
            return False

if __name__ == "__main__":
    client1 = Client('10.9.171.151', 8088, 'clent1')
    print "register"
    client1.registerClient('10.9.171.165', 8088)
