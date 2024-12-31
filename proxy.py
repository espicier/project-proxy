import os, socket, sys

import filtering as flt

# Socket côté client :
clientside_address = 'localhost'
clientside_port = 8080

clientside_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
clientside_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
clientside_socket.bind((clientside_address, clientside_port))
clientside_socket.listen(socket.SOMAXCONN)

# Socket côté serveur pour connection serveur web :
serverside_connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # pb : doit être ré-ouverte à chaque tunnel



def remote_server_connection(remote_server_infos, request):

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
    print("Remote server connection = tunnel established")



while 1:
    (received_connection, client_tsap) = clientside_socket.accept()
    print("Connection from ", client_tsap)
    connect_tunnel = received_connection.recv(1024).decode('utf-8')

    # Extract de l'url pour récupérer les infos du serveur de destination
    url = connect_tunnel.split('\n')[0].split(' ')[1]
    remote_server_infos = flt.split_url(url)
    print("server_infos: ", remote_server_infos)

    # On retire les lignes problématiques
    # On envoie le message cleaned au serveur, avec les infos qu'on a extract
    cleaned = flt.remove_problematic_lines(connect_tunnel)
    request = flt.modify_http_version(cleaned) # ppur utiliser HTTP/1.0
    print("final request: ", request)

    remote_server_connection(remote_server_infos, request)
    print("ouverture tunnel communication serveur réussi")

    # transfert paquets dans les 2 sens par le proxy une fois le tunnel établi
    while 1:
        pid = os.fork()
        if pid == 0:
            requete = received_connection.recv(1024)
            print("requete :", requete)
            if not requete:
                print("oups requete")
                received_connection.close()
                serverside_connection_socket.close()
                break
            serverside_connection_socket.sendall(requete)
            print("let's go requete")

        else:
            reponse = serverside_connection_socket.recv(1024)
            print("reponse :", reponse)
            if not reponse :
                print("oups reponse")
                serverside_connection_socket.close()
                received_connection.close()
                break
            received_connection.sendall(reponse)
            print("let's go reponse")

    print("== FIN COMMUNICATION ==")






    sys.exit(1)



