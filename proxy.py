# ====================================== Imports
import socket, sys, select, os

import filtering as flt
import config as conf
from filtering import filter_content

# ====================================== Définitions
# Socket côté client :
clientside_address = 'localhost'
clientside_port = 8080

clientside_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
clientside_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
clientside_socket.bind((clientside_address, clientside_port))
clientside_socket.listen(socket.SOMAXCONN)

# Pour avoir un cache des sites web les + visités
# On va faire un historique dans config pour gérer ça
compteur = {}

def remote_server_connection(remote_server_infos):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # pb : doit être ré-ouverte à chaque tunnel < je pense pas que ce soit un pb
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    print('================== CONNECTING TO REMOTE ======================')
    remote_server_address = socket.gethostbyname(remote_server_infos[0])
    remote_server_port = int(remote_server_infos[1])
    try :
        server_socket.connect((remote_server_address, remote_server_port))
        print("connection established with", remote_server_infos[0])
        return server_socket
    except Exception as e :
        print(e.args)
        sys.exit(1)

def transmit_get_request(client_connection, serverside_socket, request):
    serverside_socket.sendall(request.encode('utf-8'))
    print('================== TRANSMITING RESPONSE ======================')
    while 1 :
        server_response = serverside_socket.recv(1024).decode('utf-8')
        server_response_end_test = server_response.replace(' ', '%')
        if server_response_end_test.count('%') == len(server_response) :
            break
        else:
            if filter_content(server_response) : # True = pas de mot interdit détecté
                print("server response", server_response)
                client_connection.sendall(server_response.encode('utf-8'))
                print("Transmission d'une réponse au client")
            else :
                print("== ACCES INTERDIT ==")
                return
    return

def tls_communication_tunnel(client_connection, serverside_socket):
    surveillance = [client_connection, serverside_socket]
    (evnt_entree, evnt_sortie, evnt_exception) = select.select(surveillance, [], [])
    for side in evnt_entree:
        # recevoir des données côté serveur web ou navigateur
        message = side.recv(1024)
        print("Request:", message.decode('utf-8'), "from", side.getpeername())
        if not message:
            print("No request received")
            return
        else:  # les transmettre à l'autre extrémité du tunnel
            if side == client_connection:  # si message en provenance du navigateur, appliquer modifications
                cleaned = flt.remove_problematic_lines(message)
                message = flt.modify_http_version(cleaned)  # pour utiliser HTTP/1.0
                print("final message: ", message)

            for other_side in evnt_entree:
                if other_side is not side:  # que c'est moche
                    other_side.sendall(message)
                    print("message transmis")

def identify_header(request):
    header = b''
    body = b''
    index = request.find(b'\r\n\r\n')
    header += request[:index]
    body += request[index + 4:]
    return header.decode('utf-8'), body


def proxy_loop():
    (client_connection, client_tsap) = clientside_socket.accept()
    print("client accepted:", client_tsap)
    print('======================= CLIENT REQUEST ======================')
    client_request = client_connection.recv(1024)
    if client_request.startswith(b'POST'):
        # Faudrait séparer la data de la requête, là où y'a la ligne vide.
        # sinon ça plante sur l'url decode, le body d'un post étant pas en utf-8
        # faudrait séparer les deux, passer le body dans une variable à part, et faire en fonction
        header, body = identify_header(client_request)
        str_header = header
    else:
        str_header = client_request.decode('utf-8')
    # Si on a une requête vide, on recommence juste une boucle en attendant des instructions du client
    if len(str_header) == 0:
        return
    print(client_request)
    print('=============================================================')

    # Extract de l'url pour récupérer les infos du serveur de destination
    request_type = str_header.split('\n')[0].split(' ')[0]
    url = str_header.split('\n')[0].split(' ')[1]
    remote_server_infos = flt.split_url(url)

    print("server_infos: ", remote_server_infos)

    # Si l'url du serveur correspond au serveur de config, on demande
    if remote_server_infos[0] == conf.get_config_url():
        if request_type == 'GET':
            print('Connecting to proxy configuration :')
            # on envoie au client le formulaire_config
            response = ('HTTP/1.0 200 OK\nContent-Type: text/html\n\n' + conf.get_config_form() + '\n').encode('utf-8')
            print(response)
            client_connection.sendall(response)
            print('Config page sent. Waiting for response...')
        else:
            print('client responded with : ', body)
            # TODO: on sauvegarde la réponse
            conf.update_config(body)
        print('Closing connection')
        print("==================== END OF COMMUNICATION ====================")
        client_connection.close()
        return

        serverside_socket = remote_server_connection(remote_server_infos)

        print('======================= SERVER REQUEST ======================')
        if request_type =='CONNECT': # gestion d'une connection TLS
            print("Connection TLS")

            # informer client avec réponse HTTP que tunnel de communication ouvert
            successful_connection_notification = "HTTP/1.1 200 OK"
            client_connection.sendall(successful_connection_notification.encode('utf-8'))

            # transfert paquets dans les 2 sens par le proxy une fois le tunnel établi
            tls_communication_tunnel(client_connection, serverside_socket)

        if request_type =='GET':
            print("P'TIT GET")
            # traitement
            request = flt.remove_problematic_lines(str_request)
            request = flt.modify_http_version(request)  # ppur utiliser HTTP/1.0

            transmit_get_request(client_connection, serverside_socket, request=request)
            print("fin GET")


    print('=============================================================')
    # Le problème : on ferme la connexion, alors qu'on aimerai pouvoir transmettre d'autres fichiers (comme des fonts ou des images) 
    # La solution : j'ai déplacé dans remote_server_connection la création du socket, pour en avoir un neuf à chaque itération de boucle (chaque nouvelle connexion d'un client) 
    print("Closing connection")
    client_connection.close()
    serverside_socket.close()
    print("== FIN COMMUNICATION ==")

# ====================================== main

while 1:
    proxy_loop()
sys.exit(1)
