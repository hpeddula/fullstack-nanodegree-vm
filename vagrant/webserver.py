from database_setup import MenuItem,Restraunt,Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy     import create_engine
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import cgi

engine = create_engine('sqlite:///restrauntmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):


        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()

                output =""
                output +="<html><body><center>Hello</center>"
                output += "<form method=\'POST\' enctype=\'multipart/form-data\' action=\'hello\'>" \
                          "<h2>What would you like me to say</h2><input name=\'message\' type=\'text\'>" \
                          "<input type=\'submit\' value=\'Submit\'></form>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return
            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()

                output =""
                output +="<html><body><center><a href=\"/hello\">&#16 Hola</a></center>"
                output += "<form method=\'POST\' enctype=\'multipart/form-data\' action=\'hello\'>" \
                          "<h2>What would you like me to say</h2><input name=\'message\' type=\'text\'>" \
                          "<input type=\'submit\' value=\'Submit\'></form>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return
            if self.path.endswith("/restraunts"):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()

                restraunts=session.query(Restraunt).all()
                output=""
                output +="<a href=\"/new\">Make New Restraunt Here</a>"
                for i in restraunts:
                    output +="<html><body><li>"+i.name+"</li>" \
                                "<a href=\"#\">Edit</a><br>" \
                                 "<a href=\"#\">Delete</a>"
                    output +="</body></html>"

                self.wfile.write(output)
                print output
                return
            if self.path.endswith("/new"):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()

                output =""
                output +="<html><body>" \
                         "<form method=\"POST\" enctyoe=\"multipart/form-data\" action=\"/new\">" \
                         "<h2>Make New Restraunt Here</h2>" \
                         "<input name=\"restraunt\" type=\"text\">" \
                         "<input type=\"submit\" value=\"Create\">" \
                         "</form></body></html>"
                self.wfile.write(output)
                print output
                return
        except IOError:
            self.send_error(404,"File Not Found %s"%self.path)
    def do_POST(self):
        try:
            if self.path.endswith("/new"):
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', 'restraunts')
                self.end_headers()
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('restraunt')
                new = Restraunt(name=messagecontent[0])
                session.add(new)
                session.commit()
                output = "Restaurant added"
                output += "<br><a href = '/restraunts'> Back to restaurants </a></br>"
                output += "</body></html>"

                self.wfile.write(output)

            # output = ""
            # output += "<html><body>" \
            #           "<form method=\"POST\" enctyoe=\"multipart/form-data\" action=\"restraunts\">" \
            #           "<h2>Create A new restraunt</h2>" \
            #           "<input name=\'restraunt\' type=\"text\">" \
            #           "<input type=\"submit\" value=\"Submit\">" \
            #           "</form>"
            # self.wfile.write(output)
            # print output
            # self.send_response(301)
            # self.end_headers()
            # ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            # if ctype == 'multipart/form-data':
            #     fields = cgi.parse_multipart(self.rfile,pdict)
            #     messagecontent = fields.get('message')
            #
            # output = ""
            # output +="<htmL><body>"
            # output +="<h2>Okay,how about this: </h2>"
            # output +="<h1> %s </h1>" % messagecontent[0]
            # output +="<form method=\'POST\' enctype=\'multipart/form-data\' action=\'hello\'>" \
            #          "<h2>What would you like me to say</h2><input name=\'message\' type=\'text\'>" \
            #          "<input type=\'submit\' value=\'Submit\'></form>"
            # output +="</body></html>"
            # self.wfile.write(output)
            # print output

        except:
            pass
def main():
    try:
        port = 8080
        server = HTTPServer(('',port),webserverHandler)
        print "Web Server running on port %s" %port
        server.serve_forever()
    except KeyboardInterrupt:
        print "Control C pressed socket closed"
        server.socket.close()
if __name__ == '__main__':
    main()
