import sys
import zmq
import time
from api_pb2 import *
import msvcrt

zctx = zmq.Context()
zsck = zctx.socket(zmq.PUSH)
zsck.connect("tcp://127.0.0.1:7272")


print 'press 1,2, etc. for actions, see test.py source code for details'
cmd = 0

while cmd != 'q':
    if msvcrt.kbhit():
        cmd = msvcrt.getch()

        api_msg = Api()
        api_msg.title = 'Hello'
        api_msg.body = 'What\'s up?'
        if cmd == '1':
            api_msg.icon = Api.INFO
        elif cmd == '2':
            api_msg.icon = Api.INFO
            api_msg.extended_info = 'hey, there is some cool stuff here man!'
        elif cmd == '3':
            api_msg.icon = Api.CRIT
            api_msg.extended_info = 'kinda critical, you know'
        elif cmd == '0':
            api_msg.die = True

        zsck.send(api_msg.SerializeToString(), zmq.NOBLOCK)
        time.sleep(1)

