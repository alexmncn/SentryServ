from app.services.net_and_connections import notify_new_public_ip

init = True

def on_init():
    global init
    if init == True:
        try:
            notify_new_public_ip()
            init = False
        except:
            print('Init Error')