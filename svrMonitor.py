# -*- coding: utf8 -*-
import sys
import time
from pywebsocketserver.server import SocketServer
from pywebsocketserver.baseio import BaseIO
import subprocess
import paramiko

class MyIO(BaseIO):
    def oldssh():
        output=''
        while True:     
            p = subprocess.Popen('ssh -t taoh@192.168.200.69 "tail  /home/taoh/logs/test0.log" ',
                         shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            thistime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

            for line in p.stdout.readlines():
                output+= line

            
            self.sendData(uid,output+thistime)
            time.sleep(3)

    def newssh():
        while True:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect('192.168.200.69',username = 'taoh',password='')
            cmd = 'tail logs/test0.log'  #管道，ls命名的输出到文件test里面
            stdin,stdout,stderr = ssh.exec_command(cmd)
            loginfo =stdout.readlines()
            
            self.sendData(uid,loginfo)
            time.sleep(3)
    
        


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
