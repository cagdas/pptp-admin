__author__ = 'cagdas'

import cgi
import urlparse
from SimpleHTTPServer import SimpleHTTPRequestHandler
from classes.acl.users import Users

class Handler(SimpleHTTPRequestHandler):

    themePath = ''
    chap_secret_file = ''

    def __init__(self, request, client_address, server):

        self.users = Users( Handler.chap_secret_file )
        SimpleHTTPRequestHandler.__init__(self, request, client_address, server)

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_POST(self):
        form_post = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                    })

        if self.path == "/add-user":
            _u=_p=_s=_ip=""

            for item in form_post.list:
                if item.name == '_username':
                    _u=item.value
                if item.name == '_password':
                    _p=item.value
                if item.name == '_server':
                    _s=item.value
                if item.name == '_ip':
                    _ip=item.value

            self.users.add_user(_u,_p,_s,_ip)

            return self.do_REDIRECT("/users")

    def do_GET(self):
        if '?' in self.path:
            parts = self.path.split('?')
            self.path = parts[0]
            self.query_string = dict( (k, v if len(v)>1 else v[0] ) 
                        for k, v in urlparse.parse_qs(parts[1]).iteritems() )

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

        elif self.path == "/remove-user":
            id = self.query_string.get("id")
            self.users.remove_user( id )
            print "[", id , "]\tdeleted"

            return self.do_REDIRECT("/users")

        elif self.path == "/users":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            html = list_str = ""
            with open(self.themePath + "web%s.html" % self.path, 'r') as content_file:
                html += content_file.read()

            for user in self.users.fetch_users():
                list_str += "<tr>"
                list_str += "<td>%s</td><td>%s</td><td>%s</td><td>%s</td>" % (user.username, user.password, user.server, user.ip)
                list_str += "<td><a onclick=\"return confirm('Are you SURE?')\" href='remove-user?id=%d' title='remove account' ><img src='/images/delete.png' title='remove `%s`' /></a></td>" % (user.index,user.username)
                list_str += "</tr>"

            html = html.replace("%USER_LIST%", list_str)
            self.wfile.write(html)

        else:
            f = open( self.themePath + "web%s" % self.path)
            if f:
                self.copyfile(f, self.wfile)
                f.close()

    def do_REDIRECT(self, path):
        self.send_response(302)
        self.send_header("Cache-Control" , "no-cache" )
        self.send_header("Pragma", "no-cache" )
        self.send_header("Location", path )
        self.end_headers()
