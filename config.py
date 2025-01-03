import json

# Donne le formulaire de config, format html, prêt à être inséré dans une requête, en pré-remplissant les valeurs déjà en config.
def get_config_form():
    # Lire le fichier
    try:
        html_form = open("formulaire_config.html", "r")
    except Exception as e:
        print(e.args)
        return None
    str_form = ''
    while 1:
        line = html_form.readline()
        if not line:
            break
        # change la value de  en id="filter" checked si get_config()['filter_is_on'] == 1
        if get_config()['filter_is_on'] == 1:
            line = line.replace('id="filter"', 'id="filter" checked')
        # insérer le contenu de get_filtered_words dans 'name="mots a filtrer"></textarea>'
        if line.find('name="filter_words"></textarea>') != -1:
            line =line.replace('name="filter_words"></textarea>', 'name="mots a filtrer">')
            for word in get_filtered_words():
                line += word + ','
            line = line.strip(',')
            line += '</textarea>'
        # id="title" value="" avec la valeur à ajouter aux titres de chaque page visitée
        if line.find('id="title"') != -1:
            line = line.replace('value=""', 'value="' + get_config()['title_prefix'] + '"')
        str_form += line
    
    return str_form

def get_config():
    with open('config.json') as conf:
        return json.load(conf)

# Wrappers simples, pas nécéssaires en soit
def get_problematic_lines():
    return get_config()['problematic_lines']

def get_filtered_words():
    return get_config()['filtered_words']

def get_config_url():
    return get_config()['url']

def update_config(config_http):
    # dans config : la réponse en brut reçue par le client avec le formulaire, je pense que c'est plus simple de gérer ça ici
    # faire comme ça permet de garder certains éléments de config dans le même fichier, sans les exposer via le formulaire (comme l'url d'accès), pour pouvoir le modifier côté serveur, ou l'historique, géré par la gestion du cache.
    config = get_config()
    new_config = get_config_content(config_http)
    
    config['filter_is_on'] = new_config['filter_is_on']
    config['filtered_words'] = new_config['filtered_words']
    config['problematic_lines'] = new_config['problematic_lines']
    config['title_prefix'] = new_config['title_prefix']

    with open("config.json", "w") as conf_file:
        json.dump(config, conf_file)
    print("updating config")

# Fera un split du résultat de la requête, quand on aura pu la tester
# Après retour via chrome sur le formulaire, le format semble être : 
# filtrage+active=on&titre+modifie=proxy+-+&mots+a+filtrer=test%2Cmacron%2Cbrigitte%2Cdemission
def get_config_content(http_config):
    return{
        'url': "proxy-superconfig.fr",
        'filter_is_on':1,
        'title_prefix':'proxy - ',
        'filtered_words':["test",
        "macron",
        "brigitte",
        "demission"],
        'problematic_lines':[
            "Connection",
            "Proxy-Connection",
            "Accept-Encoding"]
    }