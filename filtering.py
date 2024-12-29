import re

# Retourne le nom du serveur, le port et le document à partir de l'url
def split_url(url):
    split_url_avec_port = re.compile(r'[^:]://([a-zA-Z0-9\-]+):(\d+)/(.*)$')
    split_url_sans_port = re.compile(r'[^:]://([a-zA-Z0-9\-]+)/(.*)$')
    resultat = split_url_avec_port.search(url)
    if resultat:
        return resultat.groups()
    resultat = split_url_sans_port.search(url)
    if resultat:
        return resultat.groups()

# Prend une réponse avec une balise html title, et insert du texte après la première balise trouvée.
def add_text_to_title(message, text):
    # on avait un exemple dans un des TPs
    return message

# Filtre le contenu html, en remplaçant les mots trouvés dans le fichier de configuration 
# par des étoiles (par exemple, je sais pas ce qui est attendu par "filtrer")
def filter_content(message):
    return message

# Enlève les lignes problématiques trouvées dans le message
def remove_problematic_lines(message):
    print('=== REMOVING PROBLEMATIC LINES:')
    splitted = message.split('\n')
    to_keep = message.split('\n')
    to_remove = get_problematic_lines()
    result = ''
    for line in splitted:
        for j in to_remove:
            if line.upper().startswith(j.upper()):
                to_keep.remove(line)
    for line in to_keep:
        result += line + '\n'
    print('=== DONE')
    return result

# Donne une liste des lignes problématiques, à enlever d'un message.
def get_problematic_lines():
    # dans un premier temps, on va juste faire avec une liste en dur. Le but sera d'aller lire le fichier de config pour avoir la liste.
    return [
        'Connection',
        'Proxy-Connection',
        'Accept-Encoding'
    ]