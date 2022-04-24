import cgi
from http.server import BaseHTTPRequestHandler
import pandas as pd
from IPython.display import HTML
from threading import Thread

from typing import Dict

import szerver
import sql_functions

import inserttodb

hostName = "localhost"
serverPort = 8090


def listToString(s):
    str1 = ""

    for ele in s:
        str1 += ele

        # return string
    return str1


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("content-type", "text/html")
        self.end_headers()
        index_file = open("index.html", "r")
        webpage = index_file.read()
        self.wfile.write(bytes(webpage.encode()))

    def do_POST(self):
        global sqlstring
        pdict: Dict[str, str]
        ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
        pdict['boundary'] = bytes(pdict['boundary'], "utf-8")

        content_len = int(self.headers.get('Content-length'))
        pdict['CONTENT-LENGTH'] = content_len
        if ctype == 'multipart/form-data':
            fields = cgi.parse_multipart(self.rfile, pdict)
            Full_name = listToString(fields.get('fname')) + ' ' + listToString(fields.get('lname'))
            county = listToString(fields.get('county'))
            email = listToString(fields.get('email'))
            identity = listToString(fields.get('identity'))
            vote = listToString(fields.get('votee'))
            inserttodb.insertIntoUserDb(Full_name, identity, email, vote)
            sqlstring = inserttodb.getVotesByCategory()

        self.send_response(200)
        self.send_header("content-type", "text/html")
        self.end_headers()
        output = '<!DOCTYPE html> <html lang="hu" <head> <title>Foo</title> <meta charset="utf-8"> </head> <body> <div id="container"> <p> ' + sqlstring + ' </p> </div> </body> </html>'

        self.wfile.write(bytes(output.encode()))
