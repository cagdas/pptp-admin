from matplotlib.pyplot import switch_backend

__author__ = 'Cagdas Emek'

from classes.http.server.webserver import WebServer

import sys
import os

HOST_NAME = "localhost"  # !!!DON'T FORGET TO CHANGE THIS!!!
PORT_NUMBER = 8000  # Maybe set this to 9000.

workingPath = os.path.dirname(os.path.abspath(__file__))
themePath = workingPath + '/'
CHAP_SECRETS = "/etc/ppp/chap-secrets"

server = WebServer(HOST_NAME, PORT_NUMBER )
#server.setThemePath( themePath )
#server.setWorkingPath( workingPath )
server.setChapSecretFile(CHAP_SECRETS)

if __name__ == '__main__':
    try:
        cmd = sys.argv[1];
    except:
        cmd = ''
        pass

    if cmd == 'start':
        server.start();
    elif cmd == 'stop':
        server.stop()
    elif cmd == 'restart':
        server.stop()
        server.start()
    else:
        print "Usage: python server.py {start|stop|restart}"

