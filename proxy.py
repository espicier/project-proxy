import socket, sys, select, webbrowser

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

# Pour avoir un cache des sites web les + visités
compteur = {}


def remote_server_connection(remote_server_infos):

    remote_server_address = socket.gethostbyname(remote_server_infos[0])
    remote_server_port = int(remote_server_infos[1])

    try :
        serverside_connection_socket.connect((remote_server_address, remote_server_port))
    except Exception as e :
        print(e.args)
        sys.exit(1)



while 1:
    (received_connection, client_tsap) = clientside_socket.accept()
    print("Connection from ", client_tsap)
    request = received_connection.recv(1024).decode('utf-8')

    # Extract de l'url pour récupérer les infos du serveur de destination
    request_type = request.split('\n')[0].split(' ')[0]
    url = request.split('\n')[0].split(' ')[1]
    remote_server_infos = flt.split_url(url)
    print("server_infos: ", remote_server_infos)

    if request_type =='CONNECT': # gestion d'une connection TLS

        remote_server_connection(remote_server_infos)
        print("ouverture tunnel communication serveur réussi")

        # informer client avec réponse HTTP que tunnel de communication ouvert
        successful_connection_notification = "HTTP/1.0 200 OK"
        received_connection.sendall(successful_connection_notification.encode('utf-8'))

        # Filtrage des communications en interdisant l’accès à certains sites en fonction de leur contenu
        # if flt.filter_content(remote_server_infos[0]):
        #     print("== ACCES INTERDIT ==")
        #     received_connection.close()
        #     continue # à modifier

        # transfert paquets dans les 2 sens par le proxy une fois le tunnel établi
        surveillance = [received_connection, serverside_connection_socket]
        (evnt_entree, evnt_sortie, evnt_exception) = select.select(surveillance, [], [])
        for side in evnt_entree:
        # recevoir des données côté serveur web ou navigateur
            message = side.recv(1024)
            print("requête", message.decode('utf-8'))
            if not message:
                print("oups le vent")
                break
            else: # les transmettre à l'autre extrémité du tunnel
                if side==received_connection: # si message en provenance du navigateur, appliquer modifications
                    cleaned = flt.remove_problematic_lines(message)
                    message = flt.modify_http_version(cleaned)  # pour utiliser HTTP/1.0
                    print("final message: ", message)
                for other_side in evnt_entree:
                    if other_side is not side : # que c'est moche
                        other_side.sendall(message)
                        print("message transmis")


    if request_type =='GET':
        # traitement
        #cleaned = flt.remove_problematic_lines(request)
        #final_request = flt.modify_http_version(cleaned)  # ppur utiliser HTTP/1.0

        remote_server_connection(remote_server_infos)
        serverside_connection_socket.sendall(request.encode('utf-8'))
        while 1 :
            server_response = serverside_connection_socket.recv(1024)
            print(server_response.decode('utf-8'))
            if not server_response:
                print("oups le vent")
                break
            else :
                received_connection.sendall(server_response)
                print("message transmis")
                # comment couper la communication ?


    if request_type =='POST':
        # récupérer les données à transmettre
        # data_lenght = request.split('\n')[3].split(' ')[1]
        # data =  request.split('\n')[-1]
        # if data_lenght > len(data) :
        #     data = request.split('\n')[-2] + data

        cleaned = flt.remove_problematic_lines(request)
        final_request = flt.modify_http_version(cleaned)

        remote_server_connection(remote_server_infos)
        serverside_connection_socket.sendall(final_request.encode('utf-8')) # transmettre simplement données ?

    serverside_connection_socket.close()
    received_connection.close()
    print("== FIN COMMUNICATION ==")
    sys.exit(1)



