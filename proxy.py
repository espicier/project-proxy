import os, socket, sys

import filtering as flt

# Socket côté client:
clientside_address = 'localhost'
clientside_port = 8080

clientside_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
clientside_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
clientside_socket.bind((clientside_address, clientside_port))
clientside_socket.listen(socket.SOMAXCONN)

while 1:
    (recieved_connection, client_tsap) = clientside_socket.accept()
    print("Connection from ", client_tsap)
    message = recieved_connection.recv(1024).decode('utf-8')
    
    print(message)


# à déterminer : comment on gère deux sockets avec du transfert de données entre les deux

# Socket côté serveur: