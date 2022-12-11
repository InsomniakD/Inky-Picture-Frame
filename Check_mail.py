#!/usr/bin/env python3

import glob
import os
import shutil
import time
import traceback
import warnings
import ssl
from os.path import join

import pyminizip
import requests
import subprocess
from imbox import Imbox
from PIL import Image
from inky.inky_uc8159 import Inky

warnings.filterwarnings("ignore", category=DeprecationWarning)


def check_internet():                              # Check if internet connection is established
    url = 'https://www.google.com/'
    timeout = 2
    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        return False


download_folder = "/home/pi/Inky/DownloadFMail"     # Folder where pictures from mail are decompressed and store briefly
Remove_pic_fold = "/home/pi/Inky/Remove_pic"        # Folder with the pictures to delete ( same name as the one in save_pic)
Save_picfold = "/home/pi/Inky/savepic"              # Backup folder with all pictures
diapfold = "/home/pi/Inky/diapo"                    # Folder with picture to diplay
recent_pic = "/home/pi/Inky/recent"                 # Folder with the pictures already displayed
pwfile = "/home/pi/Inky/ID/maillogin.pwd"           # The password and mail use by the program
update_fold = "/home/pi/Inky/update"                # update folder (for programs update)
os.umask(0)
host = "imap.gmail.com"
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.load_verify_locations(
    '/home/pi/Inky/ID/roots.pem')  # Google certificate may need update (Gmail)
    
with open(pwfile, "r") as pf:                       # Open the file with all password and mail information
    pw_lines = [line.rstrip('\n') for line in pf]
    username = pw_lines[0]                          # Email of your screen (need to be created and configured)
    authorised_sender = pw_lines[1]                 # Email of authorised sender (yours for example)
    password = pw_lines[2]                          # Email of the screen password 
    passw = pw_lines[3]                             # Archive password

if not os.path.isdir(download_folder):
    os.makedirs(download_folder, exist_ok=True)
if not os.path.isdir(Remove_pic_fold):
    os.makedirs(Remove_pic_fold, exist_ok=True)

for i in range(20):             #loop to check for internet connection
    if not check_internet():
        time.sleep(10)
    else:
        break

if not check_internet():        # if still no internet connection exit the program
    exit(0)

mailS = Imbox(host, username=username, password=password, ssl=True, ssl_context=context, starttls=False)     #creating the mail
Unread_authorised_sender = mailS.messages(unread=True, sent_from=authorised_sender, subject="Image_add")
Unread_inky = mailS.messages(unread=True, sent_from=username, subject="Image_add")
Unread_authorised_sender_removepic = mailS.messages(unread=True, sent_from=authorised_sender, subject="Remove_PIC")
Unread_inky_removepic = mailS.messages(unread=True, sent_from=username, subject="Remove_PIC")
authorised_sender_Prog_Update = mailS.messages(unread=True, sent_from=authorised_sender, subject="Program_Update")
inky_Prog_Update = mailS.messages(unread=True, sent_from=username, subject="Program_Update")
inky_delete_and_add = mailS.messages(unread=True, sent_from=username, subject="Delete_&_add")
authorised_sender_delete_and_add = mailS.messages(unread=True, sent_from=authorised_sender, subject="Delete_&_add")

mailListe_add = [Unread_inky, Unread_authorised_sender]
mailListe_rm = [Unread_authorised_sender_removepic, Unread_inky_removepic]
mailListe_upt = [authorised_sender_Prog_Update, inky_Prog_Update]
mailListe_d_a = [inky_delete_and_add, authorised_sender_delete_and_add]

for mailcar in mailListe_rm:                        # Check if there is an unread message in mail box with picture to remove
    for (uid, message) in mailcar:
        mailS.mark_seen(uid)
        long = len(os.listdir(download_folder))
        if long == 0:
            long = ""
        else:
            long = str(long) + "_"

        for (idx, attachment) in enumerate(message.attachments):
            try:
                att_fn = attachment.get('filename')
                download_path = f"{download_folder}/{long}{att_fn}"
                with open(download_path, "wb") as fp:
                    fp.write(attachment.get('content').read())

            except:
                print(traceback.print_exc())

    zipl = glob.glob(download_folder + "/*Image_to_del.zip")            
    if zipl != []:
        for n in range(len(os.listdir(download_folder))):
            pyminizip.uncompress(zipl[n], passw, Remove_pic_fold, 0)            # Decompress the archive with the password
            os.remove(zipl[n])

image_to_r = [f for f in os.listdir(Remove_pic_fold) if os.path.isfile(join(Remove_pic_fold, f))]

if image_to_r != []:
    image_present = [f for f in os.listdir(Save_picfold) if os.path.isfile(join(Save_picfold, f))]
    for f in os.listdir(Remove_pic_fold):
        with open("/home/pi/Inky/order.txt", 'r') as rorder:
            lines = rorder.readlines()
            rorder.close()
        with open("/home/pi/Inky/order.txt", 'w') as worder:
            for line in lines:
                if line.strip("\n") != str(f):
                    worder.write(line)
            worder.close()
    for image_to_remove in image_to_r:
        for image_pre in image_present:
            if image_to_remove == image_pre:
                os.remove(Save_picfold + "/" + image_to_remove)
                if os.path.isfile(diapfold + "/" + image_to_remove):
                    os.remove(diapfold + "/" + image_to_remove)
                if os.path.isfile(recent_pic + "/" + image_to_remove):
                    os.remove(recent_pic + "/" + image_to_remove)

    for f in os.listdir(Remove_pic_fold):
        os.remove(os.path.join(Remove_pic_fold, f))

    inky = Inky()
    os.system("sudo pkill -f /home/pi/Inky/diapo_eink.py")
    os.system("sudo pkill -f /home/pi/Inky/clean.py")
    os.system("sudo pkill -f /home/pi/Inky/clear.py")
    time.sleep(15)
    image = Image.open("/home/pi/Inky/img/images_supr.jpg")
    inky.set_image(image, saturation=0.5)
    inky.show()
    subprocess.Popen(['sudo', 'python3', '/home/pi/Inky/fonction_button.py'])

for mailcar in mailListe_add:               #download and add the picture
    for (uid, message) in mailcar:
        mailS.mark_seen(uid)
        long = len(os.listdir(download_folder))
        if long == 0:
            long = ""
        else:
            long = str(long) + "_"

        for (idx, attachment) in enumerate(message.attachments):
            try:
                att_fn = attachment.get('filename')
                download_path = f"{download_folder}/{long}{att_fn}"
                with open(download_path, "wb") as fp:
                    fp.write(attachment.get('content').read())

            except:
                pass
    zipl = glob.glob(download_folder + "/*Image_add.zip")
    if zipl != []:
        for n in range(len(os.listdir(download_folder))):
            pyminizip.uncompress(zipl[n], passw, download_folder, 0)
            for jpgfile in glob.iglob(os.path.join(download_folder, "*.jpg")):
                name = os.path.basename(jpgfile)
                shutil.copy(os.path.join(download_folder, name), os.path.join(Save_picfold, name))
                shutil.move(os.path.join(download_folder, name), os.path.join(diapfold, name))
            os.remove(zipl[n])
        inky = Inky()
        os.system("sudo pkill -f /home/pi/Inky/diapo_eink.py")
        os.system("sudo pkill -f /home/pi/Inky/clean.py")
        os.system("sudo pkill -f /home/pi/Inky/clear.py")
        os.system("sudo pkill -f /home/pi/Inky/fonction_button.py")
        time.sleep(15)
        # noinspection PyUnboundLocalVariable
        image = Image.open(os.path.join(Save_picfold, name))
        inky.set_image(image, saturation=0.5)
        inky.show()
        subprocess.Popen(['sudo', 'python3', '/home/pi/Inky/fonction_button.py'])


for mailcar in mailListe_upt:
    for (uid, message) in mailcar:
        mailS.mark_seen(uid)
        for (idx, attachment) in enumerate(message.attachments):
            try:
                att_fn = attachment.get('filename')
                download_path = f"{download_folder}/{att_fn}"
                with open(download_path, "wb") as fp:
                    fp.write(attachment.get('content').read())

            except:
                pass

        zipl = glob.glob(download_folder + "/*Prog_Update.zip")
        if zipl != []:
            mailS.logout()
            if not os.path.isdir(update_fold):
                os.makedirs(update_fold, exist_ok=True)
            pyminizip.uncompress(zipl[0], passw, update_fold, 0)
            os.system("sudo pkill -f /home/pi/Inky/clean.py")
            os.system("sudo pkill -f /home/pi/Inky/diapo_eink.py")
            for py in glob.iglob(os.path.join(update_fold, "*.py")):
                name = os.path.basename(py)
                shutil.move(os.path.join(download_folder, name), os.path.join("/home/pi/Inky", name))
            os.remove(zipl[0])
            os.system("sudo chmod +x /home/pi/Inky/clean.py")
            os.system("sudo chmod +x /home/pi/Inky/diapo_eink.py")
            if os.path.exists("/home/pi/Inky/update.py"):
                os.system("sudo chmod +x /home/pi/Inky/update.py")
                exec(open("/home/pi/Inky/update.py").read())
            os.system("sudo reboot")
            exit(0)

for mailcar in mailListe_d_a:
    for (uid, message) in mailcar:
        mailS.mark_seen(uid)
        long = len(os.listdir(download_folder))
        if long == 0:
            long = ""
        else:
            long = str(long) + "_"

        for (idx, attachment) in enumerate(message.attachments):
            try:
                att_fn = attachment.get('filename')
                download_path = f"{download_folder}/{long}{att_fn}"
                with open(download_path, "wb") as fp:
                    fp.write(attachment.get('content').read())
            except:
                pass

    zipl = glob.glob(download_folder + "/*Image_add.zip")
    if zipl != []:
        os.system("sudo pkill -f /home/pi/Inky/diapo_eink.py")
        if os.path.exists("/home/pi/Inky/recent"):
            shutil.rmtree("/home/pi/Inky/recent")
            os.mkdir("/home/pi/Inky/recent")
        if os.path.exists("/home/pi/Inky/diapo"):
            shutil.rmtree("/home/pi/Inky/diapo")
            os.mkdir("/home/pi/Inky/diapo")
        if os.path.exists("/home/pi/Inky/savepic"):
            shutil.rmtree("/home/pi/Inky/savepic")
            os.mkdir("/home/pi/Inky/savepic")
        for n in range(len(os.listdir(download_folder))):
            pyminizip.uncompress(zipl[n], passw, download_folder, 0)
            for jpgfile in glob.iglob(os.path.join(download_folder, "*.jpg")):
                name = os.path.basename(jpgfile)
                shutil.copy(os.path.join(download_folder, name), os.path.join(Save_picfold, name))
                shutil.move(os.path.join(download_folder, name), os.path.join(diapfold, name))
            os.remove(zipl[n])
        inky = Inky()
        os.system("sudo pkill -f /home/pi/Inky/diapo_eink.py")
        os.system("sudo pkill -f /home/pi/Inky/clean.py")
        os.system("sudo pkill -f /home/pi/Inky/clear.py")
        os.system("sudo pkill -f /home/pi/Inky/fonction_button.py")
        time.sleep(15)
        # noinspection PyUnboundLocalVariable
        image = Image.open(os.path.join(Save_picfold, name))
        inky.set_image(image, saturation=0.5)
        inky.show()
        subprocess.Popen(['sudo', 'python3', '/home/pi/Inky/fonction_button.py'])

mailS.logout()  #log out of mail adress