import sys
import zmq
import time
from api_pb2 import *

zctx = zmq.Context()
zsck = zctx.socket(zmq.PUSH)
zsck.connect("tcp://127.0.0.1:7272")


j = 1
while True:
    api_msg = Api()
    api_msg.desc = 'a message'

    zsck.send(api_msg.SerializeToString())
    time.sleep(1)

