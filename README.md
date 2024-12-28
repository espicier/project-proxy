# project-proxy
## Un programme principal:
- un socket qui écoute sur le port 8080
- un socket qui renvoie cette requête à la destination prévue une fois modifiée
Le second socket devra être fork après, pour avoir la requête 

En tout cas, faudra faire :
- Une fonction pour découper l'url et récupérer un tuple avec le nom du serv, le numéro de port (en mettant 80 si y'en a pas d'indiqué) et le chemin d'accès au document
- Lecture et update d'un fichier de configuration, pour ensuite le faire via une page web
- Une fonction pour filtrer le contenu reçu
à découper en sous fonction, genre: 
- une qui fait l'ajout de texte dans le titre
- une qui s'occupe de filtrer le contenu en fonction des mots trouvés dans le fichier de config 
- une qui supprime les ressources aux mauvais formats...
Aussi, de façon systématique, supprimmer les lignes données dans le sujet

Que ces fonctions utilisent les paramètres du fichier de config pour être lancées
Une page web, donc un accès web capturé par le proxy si une URL spécifique est entrée
La page web associée (plain HTML hein)

Je sais pas si y'a des trucs particuliers à faire pour gérer POST et GET

Dans tous les cas, la première chose à faire, je pense que ce serait une connexion "transparente":
On récup une requête, on la transmet vanilla au serveur concerné, on récup la réponse, et on envoie tel quel au client.


## Exemple de réception GET:
Une fois le socket lancé, en écoute en local, après avoir configuré firefox, sur le socket.recv on reçoit ça:

GET http://p-fb.net/ HTTP/1.1
Host: p-fb.net
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: keep-alive
Upgrade-Insecure-Requests: 1
Priority: u=0, i

