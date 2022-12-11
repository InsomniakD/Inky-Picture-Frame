import glob
import os
import pyminizip
import shutil
import smtplib
import ssl
import time
import warnings
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from pathlib import Path

message = MIMEMultipart()

warnings.filterwarnings("ignore", category=DeprecationWarning)

port = 587  # For starttls
smtp_server = "smtp.gmail.com"
curpath = str(Path(__file__).parent.resolve())
upload_folder = str(os.path.join(curpath, "Fichiers_annexes\\zip_envoie_mail"))
Destfolder = str(os.path.join(curpath, "Fichiers_annexes\\zip_envoie_mail\\Image_add.zip"))
image_a_envoyerfold = str(os.path.join(curpath, "Image_a_envoyer"))
pwfile = str(os.path.join(curpath, "Fichiers_annexes\\id\\maillogin.pwd"))
tte_images = str(os.path.join(curpath, "Toutes_les_images"))

inp = input(
    "Si tu as bien lancé le script pour redimensionner les images, celles que tu veux envoyer sont normalement dans "
    "le dossier 'Image_a_envoyer'.\n\nTu peux toujour en déposer toi même mais attention leurs dimensions doivent "
    "être de 600pixels en largeur et 448pixels en hauteur.\nTu peux utiliser https://www.resizepixel.com/edit"
    " c'est un site pratique.\n\nÉcrit 'ok' quand c'est bon pour toi : ")
if inp == "ok" or inp == "Ok" or inp == "OK":
    print("Super !")
else:
    print("abadakor, mauvaise réponse")
    time.sleep(10)
    quit()

picsL = glob.glob(image_a_envoyerfold + "\\*jpg")
if picsL == []:
    print("\nil semblerait qu'il n'y a pas d'image dans le dossier Image_a_envoyer")
    time.sleep(10)
    quit()

with open(pwfile, "r") as pf:
    pw_lines = [line.rstrip('\n') for line in pf]
    receiver_email = pw_lines[0]
    password = pw_lines[1]
    passarc = pw_lines[2]

sender_email = receiver_email

message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = "Image_add"

pyminizip.compress_multiple(picsL, [], Destfolder, passarc, 1)
print("Archive en cours de création ! ;)")

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
    print("L'archive est là et prête à être envoyé vers le cadre")
else:
    print("oups y un soucis la")
    time.sleep(10)
    quit()
inp = input("On l'envoi ? (oui ou non) :")
if inp == "oui" or inp == "Oui" or inp == "OUI":
    print("\nC'est en cours d'envoi")
else:
    print("Bon et bien supprimons ça")
    print("Suppresion de l'archive")
    os.remove(Destfolder)
    print("Archive supprimée")
    time.sleep(10)
    quit()

with open(zipfile, "rb") as attachment:
    payload = MIMEBase('application', 'octate-stream')
    payload.set_payload((attachment).read())
    encoders.encode_base64(payload)  # encode the attachment
    payload.add_header('Content-Disposition', 'attachment', filename="Image_add.zip")
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
    print(
        "\n\n il y a eu un problème avec l'authentification mail merci de me contacter pour une resolution dans les "
        "plus bref délai")
finally:
    print("archive envoyé")
    server.quit()

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
    print("archive supprimée")
else:
    print("The file does not exist")

for file_name in os.listdir(image_a_envoyerfold):
    source = image_a_envoyerfold + "//" + file_name
    destination = tte_images + "//" + file_name
    if os.path.isfile(source):
        shutil.copy(source, destination)

for f in os.listdir(image_a_envoyerfold):
    os.remove(os.path.join(image_a_envoyerfold, f))

input("appuie sur entrée pour quitter le programme")
exit(0)
