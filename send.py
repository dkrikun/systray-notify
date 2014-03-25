import sys
import zmq
import time
from api_pb2 import *
import msvcrt

zctx = zmq.Context()
zsck = zctx.socket(zmq.PUSH)
zsck.connect("tcp://127.0.0.1:7272")


print 'hello'
cmd = 0
while cmd != 'q':
    if msvcrt.kbhit():
        cmd = msvcrt.getch()

        api_msg = Api()
        api_msg.title = 'a title'
        api_msg.body = 'a message'

        zsck.send(api_msg.SerializeToString(), zmq.NOBLOCK)
        time.sleep(1)

