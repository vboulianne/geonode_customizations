notified_user_list.pop(user.username, None)

for i in list:
    if id_partie and i['id'] == id_partie:
        i['prochain_joueur'] = prochain_joueur
        i['état'] = état
        if gagnant:
            i['gagnant'] = gagnant
        trouvé = 1

# Créer nouvelle nouvelle entrée
if not trouvé:
    id_partie = str(uuid4())
    rightnow = datetime.now().strftime("%Y-%m-%d %X")
    list.append({'id': id_partie, 'date': rightnow ,'prochain_joueur': prochain_joueur, \
        'joueurs': [joueur1, joueur2], 'état': état, 'gagnant' : None, 'bot': robot_utilisé})


with open(path + 'saved_state.json', mode='a') as fich:
    pass