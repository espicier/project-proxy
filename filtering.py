import re, requests, socket

visited_pages = {}


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
        print(1)
        resultat = list(resultat.groups())# 80 = port par défaut
        print(resultat)
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
filter_words = ["macron", "démission"]
def filter_content(url):
    page_web = requests.get(url) # bon fond bad form
    contenu_html = page_web.text
    for mot in filter_words :
        if contenu_html.find(mot) != -1:
            # bloquer page web
            return True
        else :
            continue
    return False


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

# faire des requêtes en HTTP 1.0 au lieu de 1.1
def modify_http_version(message):
    return message.replace('HTTP/1.1','HTTP/1.0')

def afficher_contenu_page(url):
    return visited_pages[url]

def memoriser_contenu_page(url):
    contenu = requests.get(url)
    visited_pages[url] = contenu.content # idée mais pas forme
