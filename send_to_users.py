
from django.contrib.auth import get_user_model
from datetime import datetime

User = get_user_model()
now = datetime.now().timestamp()

all_users = User.objects.filter(is_active=True)
formatted_time = ""
activity_status = ""

'''
Mécanisme pour déterminer un utilsateur ne s'étant pas loggé depuis un 
'''
def set_deactivation_timer(on_probation): 
    pass


for user in all_users:
    if user.last_login != None:
        timelapse = (now - user.last_login.timestamp())/86400
        formatted_eng_time = user.last_login.strftime("%d.%m.%Y %H:%M:%S")
        just_the_timestamp = user.last_login.timestamp()
    else:
        formatted_time = "Never"
        timelapse = (now - user.date_joined.timestamp())/86400


    if timelapse > 90.0: 
        activity_status = "Quiet User"
        if flag_quiet_user == True and timelapse > 120:
            #user.is_active = False
            #user.save

            pass
        elif flag_quiet_user == True and timelapse == 120:
            message_body = f"Hello {user.first_name}, you account will be desactivated tommorow. \nIf you wish to preserve your access, login to the website and it will reset the timer.\n\n Regards,\n The Applications and Infrastruture NEEC Team"
            message_subject = f"NEEC Geoportal: Deactivation of account tommorow if no login"
            # Set datebase flag for quiet user
            user.email_user(message_subject, message_body, "admin@geoportal.ueee.ca")
        else:
            message_body = f"Hello {user.first_name}, you have not logged to the NEEOC Portal for more than 90 days (Last login: {formatted_eng_time}).\nIf you wish to preserve your access please access the website by login in. You have 30 days to do so. It will reset the timer.\n\n Regards,\n The Applications and Infrastruture NEEC Team"
            message_subject = f"NEEC Geoportal: Deactivation of account in 30 days if no login"
            # Set datebase flag for quiet user
            user.email_user(message_subject, message_body, "admin@geoportal.ueee.ca")

    else:
        
        activity_status = "Engaged User"
        flag_quiet_user = False #reset timer

    set_deactivation_timer(flag_quiet_user)

    print (now)
    print(f"{user.username} | E-mail {user.email} | Last Login: {just_the_timestamp} | Timelapse: {timelapse} | Status: {activity_status}" )

