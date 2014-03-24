import zmq
from api_pb2 import *
import sys


def main():
    zctx = zmq.Context()
    zsck = zctx.socket(zmq.PULL)
    zsck.bind("tcp://*:7272")

    while True:
        zmsg = zsck.recv()
        api_msg = Api()
        api_msg.ParseFromString(zmsg)
        print 'recved', api_msg.desc



if __name__ == '__main__':
    sys.exit(main())
