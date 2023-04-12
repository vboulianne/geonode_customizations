
from django.contrib.auth import get_user_model
from datetime import datetime
from django.core.mail import send_mail
from json import dumps, loads
# import os

User = get_user_model()
now = datetime.now().timestamp()

#all_users = User.objects.filter(is_active=True)
all_users = User.objects.filter(username="bouliannev") # Test function 
formatted_eng_time = ""
gn_action = ""
notified_user_emailbody = "\n\nCOURRIEL ENVOYÉ\:\n\n"
deactivated_user_emailbody = "\n\nACCÈS DÉSACTIVÉ\:\n\n"


#path, filename = os.path.split(os.path.abspath(__file__))

path = "/opt/geonode_custom/neec_geoportal/"



with open(path + 'saved_state.json', 'r') as fich:
    chain = fich.read()
    if not chain:
        notified_user_list = {}
    else:
        notified_user_list = loads(chain)



for user in all_users:


    if user.last_login != None:
        timelapse = (now - user.last_login.timestamp())/86400
        formatted_eng_time = user.last_login.strftime("%d.%m.%Y %H:%M:%S")
    else:
        formatted_eng_time = "Never"
        timelapse = (now - user.date_joined.timestamp())/86400


    if timelapse > 180.0:
    
        if  timelapse > 210 and notified_user_list.get(user.username, None) == 1:
        #----------- Deactivate user ----------
        #    user.is_active = False
        #    user.save
            deactivated_user_emailbody += "L'accès de" + user.username + " a été désactivé.\n" 
            notified_user_list.pop(user.username, None)
            gn_action = "Inactivated"

        else:
            
            if user.language == "fr":
                    with open(path + 'fr_email_quiet_users.txt','r', encoding='utf8') as f:
                        email_int = f.read()
                    email_subject = "Désactivation de votre compte géportail du CNUE dans 30 jours si vous ne vous connectez pas"
            else:
                with open(path + 'en_email_quiet_users.txt','r', encoding='utf8') as f:
                    email_int = f.read()
                email_subject = "Deactivation of NECC geoportal account in 30 days if there is no login"

                email_body = email_int.format(user.get_short_name())

            user.email_user(email_subject, email_body, "geoportal@ueee.ca")
            notified_user_emailbody += "Un courriel a été envoyé à " + user.username + " (" + user.email + ")\n" 
            notified_user_list[user.username] = 1
            gn_action = "Email sent"

    else:
        notified_user_list.pop(user.username, None) # Remove 180 notification flag
        gn_action = "None"

    #--- Test ---
    #print(f"{user.username} | Timelapse: {int(timelapse)} | Active?: {user.is_active} | Action: {gn_action}" )
    
# Envoyer courriel à l'administrateur de geoportal

admin_email_body = "Actions entreprises par le script de vérification des usagers ne s'étant pas connectés depuis plus de 180 jours\n\n" + notified_user_emailbody + deactivated_user_emailbody
admin_email_subject = "Rapport d'action sur le statuts des usagers sans connection depuis 180 jours"
send_mail(admin_email_subject, admin_email_body, "geoportal@ueee.ca", ["vincent.boulianne@ec.gc.ca"])


# Inscrire dans fichier l'état des notifications.
with open(path + 'saved_state.json', mode='w') as fich:
    fich.write(dumps(notified_user_list))

