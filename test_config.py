import config

# + ou - ce qu'on extrait, brut, de la requête.
def list_words():
    return 'test,chien,patate'

def list_problines():
    return 'Connection,Proxy-Connection,Accept-Encoding'

config.update_config('osef')
with open("test_configform.html", 'w') as file:
    file.write(config.get_config_form())