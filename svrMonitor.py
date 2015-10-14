# -*- coding: utf8 -*-
import sys
import time
from pywebsocketserver.server import SocketServer
from pywebsocketserver.baseio import BaseIO
import subprocess
import paramiko

class MyIO(BaseIO):
   
    def onData(self,uid,text):
        self.sendData(uid,"我收到了你的消息：%s"%(text,))

    def onConnect(self,uid):
        process1 = subprocess.Popen('ssh -t taoh@192.168.200.69 "tail   -f /home/taoh/logs/test0.log" ',
                         shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        while True:
            line = process1.stdout.readline()
            if not line:
                break
            self.sendData(uid,line)
try:
    port = sys.argv[1]
except:
    port = 8082

port = int(port)
myIo = MyIO()
SocketServer(port,myIo).run()    
