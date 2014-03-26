__author__ = 'Cagdas Emek'
import time
import BaseHTTPServer
import logging
import cgi
from SimpleHTTPServer import SimpleHTTPRequestHandler

CHAP_SECRETS = "./chap-secrets"

HOST_NAME = ""  # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 8000  # Maybe set this to 9000.


class MyHandler(SimpleHTTPRequestHandler):
    user_list = [ ]

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_POST(self):
         if self.path == "/add-user":
            form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })
            username=password=""
            for item in form.list:
                if item.name == 'username':
                    username=item.value
                if item.name == 'password':
                    password=item.value

            newline = "%s\t*\t%s\t*\r\n" % (username,password)

            with open(CHAP_SECRETS, "a") as file:
                file.write(newline)
            self.do_REDIRECT("/users")

    def do_GET(self):
        if self.path == '/':
            self.do_HEAD()
            html = ""
            with open("./web/index.html", 'r') as content_file:
                html += content_file.read()
            self.wfile.write(html)

        elif self.path == "/create":
            self.do_HEAD()
            html = ""
            with open("./web/create.html", 'r') as content_file:
                html += content_file.read()
            self.wfile.write(html)

        elif self.path == "/users":
            self.fetch_users()
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            html=list_str = ""

            with open("./web%s.html" % self.path, 'r') as content_file:
                html += content_file.read()

            for user in self.user_list:
                item = user.split()
                list_str += "<tr><td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td></tr>" % (item[0],item[1],item[2],item[3])
            html = html.replace("%USER_LIST%", list_str)
            self.wfile.write(html)
        else:
            f = open("./web%s" % self.path)
            if f:
                self.copyfile(f, self.wfile)
                f.close()

    def do_REDIRECT(self, path):
        self.send_response(301)
        self.send_header("Location", path)
        self.end_headers()

    def fetch_users(self):
        self.user_list = []
        f = open(CHAP_SECRETS, "r")
        line = f.readline()
        while line:
            if line[0] != '#':
                self.user_list.append(line)
            line = f.readline()


if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)