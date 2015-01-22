import BaseHTTPServer
import time
import os
from classes.http.request.handler import Handler

__author__ = 'cagdas'

class WebServer():

    __working_dir = ''
    __chap_secret_file = "/etc/ppp/chap-secrets"
    __themePath = '../../../web'

    def start(self):
        try:
            print time.asctime(), "Server Started - %s:%s" % (self.__hostname, self.__port)
            self.__daemon.serve_forever()
        except:
            pass

    def stop(self):
        try:
            self.__daemon.server_close()
            print time.asctime(), "Server Stopped - %s:%s" % (self.__hostname, self.__port)
        except:
            pass

    def __init__(self, hostname, port, chap_secret_file):
        Handler.themePath = os.path.dirname(os.path.abspath(__file__)) + "/../../../";
        Handler.chap_secret_file = chap_secret_file
        
        self.__hostname = hostname
        self.__port = port
        self.__httpserver = BaseHTTPServer.HTTPServer
        self.__daemon = self.__httpserver(( self.__hostname, self.__port), Handler )

    def setWorkingPath(self, path):
        self.__working_dir = path

    def setThemePath(self, path):
        self.__themePath = path
        Handler.themePath = self.__themePath
 