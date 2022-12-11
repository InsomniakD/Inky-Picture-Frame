import glob
import os
import pyminizip
import smtplib
import ssl
import subprocess
import time
import warnings
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from os.path import join
from pathlib import Path

message = MIMEMultipart()

warnings.filterwarnings("ignore", category=DeprecationWarning)

port = 587  # For starttls
smtp_server = "smtp.gmail.com"
curpath = str(Path(__file__).parent.resolve())
upload_folder = str(os.path.join(curpath, "Fichiers_annexes\\zip_envoie_mail"))
Dfolder = str(os.path.join(curpath, "Image_a_supprimer"))
Destfolder = str(os.path.join(curpath, "Fichiers_annexes\\zip_envoie_mail\\Image_a_supprimer.zip"))
Save_picfold = str(os.path.join(curpath, "Toutes_les_images"))
pwfile = str(os.path.join(curpath, "Fichiers_annexes\\id\\maillogin.pwd"))

with open(pwfile, "r") as pf:
    pw_lines = [line.rstrip('\n') for line in pf]
    sender_email = pw_lines[0]
    password = pw_lines[1]
    passarc = pw_lines[2]

receiver_email = sender_email
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = "Remove_PIC"

print(
    "Copy les images que tu souhaites supprimer contenu dans le dossier 'Toutes_les_images' vers le dossier "
    "'Image_a_supprimer'")

inp = input("\nVeux-tu ouvrir automatiquement les deux dossiers ?. (oui ou non)\nRéponse: ")
if inp == "Oui" or inp == "oui" or inp == "OUI":
    subprocess.Popen(f'explorer "{Save_picfold}"')
    time.sleep(0.5)
    subprocess.Popen(f'explorer "{Dfolder}"')
    time.sleep(2)

time.sleep(1)

inp = input("\nQuand tu as deposées les images à supprimer écrit 'ok'.\nReponse : ")
if inp == "ok" or inp == "Ok" or inp == "OK":
    imgtodel = glob.glob(Dfolder + "\\*jpg")
    if imgtodel == []:
        print(
            "il n'y a pas d'image dans le dossier 'Image_a_supprimer'. Execute de nouveau le script et suis bien les "
            "indications.")
        time.sleep(8)
        quit()
else:
    print("Mauvaise réponse, fermeture du programme")
    quit()

pyminizip.compress_multiple(imgtodel, [], Destfolder, passarc, 1, )
print("Archive de suppression en cours de création !")

c, passage, ziplocation = 0, 0, []
while c == 0 and passage <= 20:
    ziplocation = glob.glob(upload_folder + "\\*zip")
    if ziplocation != []:
        c = 1
    else:
        passage += 1
        time.sleep(0.5)

ziplocation = glob.glob(upload_folder + "\\*zip")
zipfile = ' '.join(map(str, ziplocation))

if os.path.exists(zipfile):
    print("L'archive de supression est là et prête à être envoyé vers le cadre")
else:
    print("oups y un soucis la")
    time.sleep(3)
    quit()

inp = input("Tu es sûr de vouloir en supprimer ? (oui ou non) : ")
if inp == "oui" or inp == "Oui" or inp == "OUI" or inp == "o":
    print("\nallons y alors :'( ")
else:
    print("Bon et bien annulons ça alors, quelle mauvaise idée aussi de\nsupprimer ces belles images roooh")
    time.sleep(1.5)
    print("Suppresion de l'archive")
    time.sleep(1.5)
    os.remove(Destfolder)
    print("Archive supprimée")
    time.sleep(10)
    quit()

with open(zipfile, "rb") as attachment:
    payload = MIMEBase('application', 'octate-stream')
    payload.set_payload(attachment.read())
    encoders.encode_base64(payload)  # encode the attachment
    payload.add_header('Content-Disposition', 'attachment', filename="Image_a_supprimer.zip")
    message.attach(payload)

text = message.as_string()
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.load_verify_locations(
    curpath + r"\Fichiers_annexes\ID\roots.pem")  # attention il pourra avoir besoin d'update ce bougre

try:
    server = smtplib.SMTP(smtp_server, port)
    server.starttls(context=context)  # Secure the connection
    server.ehlo()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, text)
except Exception as e:
    print(e)
finally:
    print("archive de supression envoyé")
    server.quit()

image_to_r = [f for f in os.listdir(Dfolder) if os.path.isfile(join(Dfolder, f))]
image_present = [f for f in os.listdir(Save_picfold) if os.path.isfile(join(Save_picfold, f))]

if os.path.exists(Destfolder):
    print("suppresion de l'archive dans (ctrl + c pour annuler) \n    5")
    time.sleep(1)
    print("    4")
    time.sleep(1)
    print("    3")
    time.sleep(1)
    print("    2")
    time.sleep(1)
    print("    1")
    time.sleep(1)
    os.remove(Destfolder)
    for f in os.listdir(Dfolder):
        os.remove(os.path.join(Dfolder, f))
    for image_to_remove in image_to_r:
        for image_pre in image_present:
            if image_to_remove == image_pre:
                os.remove(Save_picfold + "\\" + image_to_remove)

    print("archive supprimée")

else:
    print("The file does not exist")

input("\nLes images seront supprimées au prochain démarrage du cadre.\nappuie sur entrée pour quitter le programme")
exit(0)
