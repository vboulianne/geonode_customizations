from django.contrib.auth import get_user_model
from datetime import datetime

User = get_user_model()
now = datetime.now().timestamp()




all_users = User.objects.filter(username="bouliannev") # Test function 
formatted_eng_time = ""
gn_action = ""

for user in all_users:
    
    if user.language == "fr":
        with open('/opt/geonode_custom/neec_geoportal/fr_email_quiet_users.txt','r', encoding='utf8') as f:
            email_int = f.read()
        email_subject = "Désactivation de votre compte géportail du CNUE dans 30 jours si vous ne vous connectez pas"
    else:
        with open('/opt/geonode_custom/neec_geoportal/en_email_quiet_users.txt','r', encoding='utf8') as f:
            email_int = f.read()
        email_subject = "Deactivation of NECC geoportal account in 30 days if there is no login"

    email_body = email_int.format(user.get_short_name())

    user.email_user(email_subject, email_body, "admin@geoportal.ueee.ca")
    
    