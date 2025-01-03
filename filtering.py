import re, requests, socket
import config

cached_pages = {}


# Retourne le nom du serveur, le port et le document à partir de l'url
def split_url(url):
    url_avec_port_http = re.compile(r'[^:]+://([a-zA-Z0-9\.\-]+):(\d+)/(.*)$')
    url_sans_port_http = re.compile(r'[^:]+://([a-zA-Z0-9\.\-]+)/(.*)$')
    default_port = '80'
    resultat = url_avec_port_http.search(url)
    if resultat:
        return list(resultat.groups())
    resultat = url_sans_port_http.search(url)
    if resultat:
        resultat = list(resultat.groups())# 80 = port par défaut
        resultat.insert(1, default_port)
        return resultat

    url_avec_port_tls = re.compile(r'([a-zA-Z0-9\-,.]+):(\d+)$')
    url_sans_port_tls = re.compile(r'([a-zA-Z0-9\-,.]+)$')
    resultat = url_avec_port_tls.search(url)
    if resultat:
        return list(resultat.groups())
    resultat = url_sans_port_tls.search(url)
    if resultat:
        resultat = list(resultat.groups())
        resultat.insert(1, default_port)
        return resultat # 80 = port par défaut

# Prend une réponse avec une balise html title, et insert du texte après la première balise trouvée.
def add_text_to_title(message, text):
    # on avait un exemple dans un des TPs
    return message

# Filtre le contenu html, en remplaçant les mots trouvés dans le fichier de configuration 
# par des étoiles (par exemple, je sais pas ce qui est attendu par "filtrer")
filter_words = config.get_filtered_words()
def filter_content(content):
    for mot in filter_words :
        if content.find(mot) != -1:
            # bloquer page web
            return False
        else :
            continue
    return True


# Enlève les lignes problématiques trouvées dans le message
def remove_problematic_lines(message):
    splitted = message.split('\n')
    to_keep = message.split('\n')
    # to_remove = config.get_problematic_lines()
    to_remove = ['Connection: Keep-Alive', 'Accept-Encoding: gzip', 'Proxy-Connection: Keep-Alive']
    result = ''
    for line in splitted:
        for j in to_remove:
            if line.upper().startswith(j.upper()):
                to_keep.remove(line)
    for line in to_keep:
        result += line + '\n'
    return result

# faire des requêtes en HTTP 1.0 au lieu de 1.1
def modify_http_version(message):
    return message.replace('HTTP/1.1','HTTP/1.0')

def modify_title(modified_title, content):
    re_debut_titre = re.compile(r'<title>(.*)$', re.I)
    re_fin_titre = re.compile(r'^(.*)</title>', re.I)

    resultat = re_debut_titre.search(content)
    if resultat:
        start = resultat.start(1)
        while 1:
            resultat = re_fin_titre.search(content[start:])
            if resultat:
                end = start + resultat.end(1)
                break
        content = content[:start]+modified_title+content[end+1:]
    return content
