import json

def get_config_element(element):
    with open('config.json') as conf:
        return json.load(conf)[element]

# Donne une liste des lignes problématiques, à enlever d'un message.
def get_problematic_lines():
    return get_config_element('problematic_lines')

def get_filtered_words():
    return get_config_element('filtered_words')

def get_config_url():
    return get_config_url('url')

# Le formulaire de config, format html
def get_config_form():
    return None

def update_config(config):
    # dans config : la réponse en brut reçue par le client avec le formulaire, je pense que c'est plus simple de gérer ça ici
    print("updating config")