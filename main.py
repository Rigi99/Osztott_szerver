from http.server import HTTPServer
from threading import Thread
import szerver
import web_server


def print_hi(name):
    print(f'Hi, {name}')


if __name__ == '__main__':

    webServer = HTTPServer((web_server.hostName, web_server.serverPort), web_server.MyServer)
    print("Server started http://%s:%s" % (web_server.hostName, web_server.serverPort))
    t = Thread(target=szerver.server_start, args=("127.0.0.1", 65432))
    print('Tcp server started 1')
    t.start()
    print('Tcp server started')
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
