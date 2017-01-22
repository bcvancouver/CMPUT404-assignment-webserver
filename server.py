#  coding: utf-8 
import SocketServer, os.path, datetime

# Copyright 2013 Abram Hindle, Eddie Antonio Santos, Michael Xi
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(SocketServer.BaseRequestHandler):
    requestHeader = []
    responseHeader = ""
    content = "hi~~~"

    def checkmethod(self, method):
        if method == "GET":
            if len(self.requestHeader) > 1:
                filepath = self.requestHeader[1]
                self.resolvepath(filepath)
            else:
                return
        else:
            self.responseHeader = "HTTP/1.1 405 Method Not Allowed\r\n"
        return

    def isdir(self, pathstr):
        return os.path.isdir(os.curdir + pathstr)

    def isfile(self, pathstr):
        return os.path.isfile(os.curdir + pathstr)

    def normalizepath(self, path):
        return os.path.normpath(os.path.normcase(path))

    def resolvepath(self, filepath):
        path = "/www/"
        if len(filepath)>1:
            path += filepath
        else:
            return

        if self.isfile(path):
            self.responseHeader = "HTTP/1.1 200 OK\r\n"
        else:
            self.responseHeader = "HTTP/1.1 404 NOT FOUND\r\n"
            self.responseHeader += "Content-Type: text/html;\r\n"
            self.content = "<html><head></head><body><h1>404 NOT FOUND</h1></body></html>"

    # Post current date& time in GMT to response header.
    def postdatetime(self):
        # https://docs.python.org/2/library/datetime.html#datetime.datetime
        # Returns the current UTC/GMT time.
        now = datetime.datetime.utcnow()
        # https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior
        formatdatetime = now.strftime("Date: %a, %d %b %Y %H:%M:%S GMT\r\n")
        self.responseHeader += formatdatetime
        return self.responseHeader

    def handle(self):
        self.data = self.request.recv(1024).strip()
        self.requestHeader = self.data.split(" ")
        #print self.requestHeader
        method=self.requestHeader[0]

        self.checkmethod(method)
        #print ("Got a request of: %s\n" % self.data)

        self.responseHeader = self.postdatetime()
        self.request.sendall(self.responseHeader + "\r\n" + self.content)

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
