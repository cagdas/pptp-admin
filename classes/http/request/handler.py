__author__ = 'cagdas'

import cgi
from SimpleHTTPServer import SimpleHTTPRequestHandler
from classes.acl.users import Users

class Handler(SimpleHTTPRequestHandler):

    themePath = ''
    chap_secret_file = ''
    user_list = []
    user_manager = Users(self.chap_secret_file)

    def __init__(self, request, client_address, server):
        self.user_manager = Users(self.chap_secret_file)
        SimpleHTTPRequestHandler.__init__(self, request, client_address, server)

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

            with open(self.chap_secret_file, "a") as file:
                file.write(newline)
            self.do_REDIRECT("/users")

    def do_GET(self):
        if self.path == '/':
            self.do_HEAD()
            html = ""
            with open( self.themePath + "web/index.html" , 'r') as content_file:
                html += content_file.read()
            self.wfile.write(html)

        elif self.path == "/create":
            self.do_HEAD()
            html = ""
            with open(self.themePath +"web/create.html", 'r') as content_file:
                html += content_file.read()
            self.wfile.write(html)

        elif self.path == "/users":
            self.user_list = self.user_manager.fetch_users()
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            html=list_str = ""

            with open(self.themePath + "web%s.html" % self.path, 'r') as content_file:
                html += content_file.read()

            for user in self.user_list:
                item = user.split()
                list_str += "<tr><td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td></tr>" % (item[0],item[2],item[1],item[3])
            html = html.replace("%USER_LIST%", list_str)
            self.wfile.write(html)
        else:
            f = open( self.themePath + "web%s" % self.path)
            if f:
                self.copyfile(f, self.wfile)
                f.close()

    def do_REDIRECT(self, path):
        self.send_response(301)
        self.send_header("Location", path)
        self.end_headers()
