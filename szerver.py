import socket

import sql_functions
import inserttodb


def server_start(host_name, port_num):
    HOST = host_name  # Standard loop back interface address (localhost)
    PORT = port_num  # Port to listen on (non-privileged ports are > 1023)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, address = s.accept()
        with conn:
            print(f"Connected by {address}")
            while True:
                data = conn.recv(1024)
                print(data)
                if not data:
                    return
                message = inserttodb.getVotesByCategoryToServer()
                conn.sendall(message.encode())


def listToString(list_element):
    # initialize an empty string
    str1 = ""

    # traverse in the string
    for ele in list_element:
        str1 += ele

        # return string
    return str1
