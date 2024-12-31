import os, socket, sys

import filtering as flt

# Socket côté client :
clientside_address = 'localhost'
clientside_port = 8080

clientside_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
clientside_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
clientside_socket.bind((clientside_address, clientside_port))
clientside_socket.listen(socket.SOMAXCONN)

# Socket côté serveur pour réception réponse serveur web :
serverside_address = 'localhost'
serverside_port = 6789

serverside_reception_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
serverside_reception_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverside_reception_socket.bind((serverside_address, serverside_port))
serverside_reception_socket.listen(socket.SOMAXCONN)

# Socket côté serveur pour connection serveur web :
serverside_connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def remote_server_connection(remote_server_infos, cleaned):
    remote_server_address = socket.gethostbyname(remote_server_infos[0])
    remote_server_port = int(remote_server_infos[1])

    try :
        serverside_connection_socket.connect((remote_server_address, remote_server_port))
    except Exception as e :
        print(e.args)
        sys.exit(1)

    # informer client avec réponse HTTP que tunnel de communication ouvert
    successful_connection_notification = "HTTP/1.1 200 OK"
    received_connection.sendall(successful_connection_notification.encode('utf-8'))
    print("Remote server connection established")

    serverside_connection_socket.sendall(cleaned.encode('utf-8'))

    while 1 :
        remote_server_response = serverside_connection_socket.recv(1024).decode('utf-8')
        if not remote_server_response:
            serverside_connection_socket.close()
            break
        print("remote_server_response :", remote_server_response)



while 1:
    (received_connection, client_tsap) = clientside_socket.accept()
    print("Connection from ", client_tsap)
    message = received_connection.recv(1024).decode('utf-8')

    # Extract de l'url pour récupérer les infos du serveur de destination
    url = message.split('\n')[0].split(' ')[1]
    remote_server_infos = flt.split_url(url)
    print("server_infos: ", remote_server_infos)

    # On retire les lignes problématiques
    # On envoie le message cleaned au serveur, avec les infos qu'on a extract
    cleaned = flt.remove_problematic_lines(message)
    request = flt.modify_http_version(cleaned)
    print("final request: ", request)

    # à déterminer : comment on gère deux sockets avec du transfert de données entre les deux
    remote_server_connection(remote_server_infos, cleaned)
    print("envoi message serveur réussi")



    sys.exit(1)



