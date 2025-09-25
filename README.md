# Réalisation d’un proxy pour le Web (protocole HTTP)

Projet réalisé en 1ere année de master informatique Cryptis en binôme avec Corentin Clerc, étudiant en M1 ISICG, à l'Université de Limoges sous l'encadrement de Mr Pierre-François Bonnefoi dans le cadre de l'UE Protocoles & Programmation réseau. 
## Description
Un serveur proxy sert d'intermédiaire entre un serveur Web et un client Web (le navigateur) qui communiquent suivant le protocole HTTP, basé TCP.
Le rôle de notre proxy est de 
- filtrer les communications (interdire l'accès à certains sites selon une liste de mots-clés)
- mémoriser le contenu des pages les plus souvent visitées (pour ne pas avoir à les récupérer auprès du serveur à chaque fois)
- modifier les données transmises (censure, protection parentale, etc...)
- assurer une meilleure sécurité (les machines clientes ne dialoguent pas directement avec les serveurs situés à l’extérieur du réseau local, mais uniquement avec le proxy.

  La liste des mots-clés à filtrer et l'activation ou non du filtrage sont configurables par l’intermédiaire d’un accès Web particulier capturé par le proxy.

## Fonctionnement
Le proxy se comporte comme un serveur et attend les connexions du navigateur. Il dispose donc d'un SAP (adresse IP, numéro de port) à renseigner au niveau des préférences du navigateur.
Le proxy :
- crée une socket pour permettre au navigateur de se connecter à lui
- reçoit une requête de la part du navigateur
- décompose l’URL présente dans cette requête (nom serveur web, numéro port, chemin d'accès au document)
- crée une seconde socket pour pouvoir se connecter au serveur Web
- envoie une requête légèrement modifiée au serveur Web (chemin d'accès -> URL document dans la requête), récupère la réponse et la renvoie au navigateur.

### Remarques
Pour le bon fonctionnement de notre proxy, il a été nécessaire de :
- supprimer les lignes commençant par Connection : Keep-Alive/Proxy-Connection : Keep-Alive
- supprimer la ligne commençant par Accept-Encoding : gzip
- faire les requêtes en HTTP/1.0

