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
    (received_connection, client_tsap) = clientside_socket.accept()
    print("Connection from ", client_tsap)
    message = received_connection.recv(1024).decode('utf-8')
    print(message)
    # Extract de l'url pour récupérer les infos du serveur de destination
    url = message.split('\n')[0].split(' ')[1]
    print('url:', url)
    server_infos = flt.split_url(url)
    print('server_infos:', server_infos)

    # On retire les lignes problématiques
    cleaned = flt.remove_problematic_lines(message)
    print(cleaned)

    # On envoie le message cleaned au serveur, avec les infos qu'on a extract
    sys.exit(1)


# à déterminer : comment on gère deux sockets avec du transfert de données entre les deux

# Socket côté serveur: