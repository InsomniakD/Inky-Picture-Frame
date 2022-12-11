import glob
import os
import subprocess
import time
from pathlib import Path

from PIL import Image, ExifTags

curpath = str(Path(__file__).parent.resolve())
Image_original = str(os.path.join(curpath, "Image_original"))
image_a_envoyerfold = str(os.path.join(curpath, "Image_a_envoyer"))
background = str(os.path.join(curpath, "Fichiers_annexes\\Id\\background.jpg"))
i = 0
r = 0
rota = []

print(
    "Copie les images que tu souhaite envoyer dans le dossier 'Image_original'.\nCelles-ci seront redimenssionnées "
    "pour être compatible avec le cadre.")
time.sleep(3)

inp = input("\nVeux-tu que le dossier s'ouvre automatiquement ? (oui ou non et après appuie sur entrée)\nRéponse: ")
if inp == "Oui" or inp == "oui" or inp == "OUI":
    subprocess.Popen(f'explorer "{Image_original}"')

time.sleep(3)
inp = input("\nQuand tu les as deposées écrit 'ok' (tu peux également fermer le dossier).\nReponse : ")
if inp == "ok" or inp == "Ok" or inp == "OK":
    if os.listdir(Image_original) == []:
        print(
            "il semblerait qu'il n'y ait pas d'image dans le dossier 'Image_original'. Execute de nouveau le script "
            "et suis bien les indications.")
        time.sleep(8)
        quit()
    else:
        files = [file for file in os.listdir(Image_original) if file.endswith(('jpeg', 'png', 'jpg', 'PNG','JPG'))]
        for image in files:
            i += 1
            img = Image.open(os.path.join(Image_original, image))
            try:
                for orientation in ExifTags.TAGS.keys():
                    if ExifTags.TAGS[orientation] == 'Orientation':
                        break
                exif = img._getexif()
                if exif is not None:                 
                    if exif[orientation] == 0:
                        if img.width < img.height:
                            rota.append(image)
                            r += 1
                            img = img.transpose(Image.ROTATE_90)
                        else:
                            rota.append(image)
                            img = img.transpose(Image.ROTATE_90)
                            r += 1
                        
                    elif exif[orientation] == 1:
                        if img.width > img.height:
                            pass
                        else:
                            rota.append(image)
                            img = img.transpose(Image.ROTATE_90)
                            r += 1
                            
                    elif exif[orientation] == 3:
                        rota.append(image)
                        img = img.transpose(Image.ROTATE_180)
                        r += 1
                    elif exif[orientation] == 6:
                        if img.width > img.height:
                            img = img.transpose(Image.ROTATE_180)
                        else:
                            rota.append(image)
                            img = img.transpose(Image.ROTATE_270)
                            r += 1
                    elif exif[orientation] == 8:
                        if img.width > img.height:
                            img = img.transpose(Image.ROTATE_180)
                        else:
                            rota.append(image)
                            img = img.transpose(Image.ROTATE_90)
                            r += 1
                    elif exif[orientation] == 4:
                        if img.width > img.height:
                            pass
                        else:
                            rota.append(image)
                            img = img.transpose(Image.ROTATE_90)
                            r += 1
                    elif exif[orientation] == 5:
                        if img.width > img.height:
                            img = img.transpose(Image.ROTATE_180)
                        else:
                            rota.append(image)
                            img = img.transpose(Image.ROTATE_270)
                            r += 1
                    elif exif[orientation] == 7:
                        if img.width > img.height:
                            img = img.transpose(Image.ROTATE_180)
                        else:
                            rota.append(image)
                            img = img.transpose(Image.ROTATE_90)
                            r += 1
                            
                else:
                    if img.width < img.height:
                        rota.append(image)
                        r += 1
                        img = img.transpose(Image.ROTATE_90)

            except (AttributeError, KeyError, IndexError):
                pass
            
            imageori = img
            img.thumbnail((600, 448))
            wo, ho = imageori.width, imageori.height
            w, h = img.width, img.height
            if w != 600 or h != 448 :
                if w >= 570 and h >= 418:
                    img = imageori.resize((600,448))
                    w, h = 600, 448
                    img.save(image_a_envoyerfold + "\\" + image,optimize=True, quality=98)
                if h >= 418 and w < 570 and h !=448 :
                    img = imageori.resize((w,448))
                    h = 448
                    backgroundA = Image.open(background)
                    image_copy = backgroundA.copy()
                    position = ((int((backgroundA.width - img.width) / 2)), (int((backgroundA.height - img.height) / 2)))
                    image_copy.paste(img, position)
                    image_copy.save(image_a_envoyerfold + "\\" + image,optimize=True, quality=98)
                if w >= 570 and h < 418 and w !=600 :
                    img = imageori.resize((600,h))
                    w = 600
                    backgroundA = Image.open(background)
                    image_copy = backgroundA.copy()
                    position = ((int((backgroundA.width - img.width) / 2)), (int((backgroundA.height - img.height) / 2)))
                    image_copy.paste(img, position)
                    image_copy.save(image_a_envoyerfold + "\\" + image,optimize=True, quality=98)
                if w < 570 and h == 448 :
                    img = imageori.resize((w+25,h))
                    backgroundA = Image.open(background)
                    image_copy = backgroundA.copy()
                    position = ((int((backgroundA.width - img.width) / 2)), (int((backgroundA.height - img.height) / 2)))
                    image_copy.paste(img, position)
                    image_copy.save(image_a_envoyerfold + "\\" + image,optimize=True, quality=98)
                if h < 418 and w == 600:
                    img = imageori.resize((w,h+25))
                    backgroundA = Image.open(background)
                    image_copy = backgroundA.copy()
                    position = ((int((backgroundA.width - img.width) / 2)), (int((backgroundA.height - img.height) / 2)))
                    image_copy.paste(img, position)
                    image_copy.save(image_a_envoyerfold + "\\" + image,optimize=True, quality=98)
                if w < 570 and h < 418:
                    backgroundA = Image.open(background)
                    image_copy = backgroundA.copy()
                    position = ((int((backgroundA.width - img.width) / 2)), (int((backgroundA.height - img.height) / 2)))
                    image_copy.paste(img, position)
                    image_copy.save(image_a_envoyerfold + "\\" + image,optimize=True, quality=98)

            else:
                img.save(image_a_envoyerfold + "\\" + image,optimize=True, quality=98)

else:
    quit()

for file in glob.iglob(image_a_envoyerfold + "//" + "*.png"):
    im = Image.open(file)
    rgb_im = im.convert("RGB")
    rgb_im.save(file.replace("png" or "PNG", "jpg"), quality=95)
    os.remove(file)

for file in glob.iglob(image_a_envoyerfold + "//" + "*.jpeg"):
    im = Image.open(file)
    rgb_im = im.convert('RGB')
    rgb_im.save(file.replace("jpeg", "jpg"), quality=95)
    os.remove(file)

if i == 1:
    print("\n\nAu total ", i, "image a été redemensionnée")
    if r == 1:
        print("Elle a également subis une rotation")
    print(
        "Tu peux maintenant verifier si l'images a correctement été redimensionnée dans image_à_envoyer.\nouverture "
        "automatique du dossier dans 5 secondes.\n\n\n")
else:
    print("\n\nAu total ", i, "images ont été redemensionnées")
    if r == 1:
        print("\nUne a subis une rotation :", rota)
    elif r >= 2:
        print("\nil y a", r, "images qui ont subis une rotation :\n\n", rota)
    print(
        "\n\n\nTu peux maintenant verifier si les images ont correctement été redimensionnées dans le dossier "
        "image_à_envoyer.\nOuverture automatique du dossier dans quelques secondes.\n\n\n")

time.sleep(7)
subprocess.Popen(f'explorer "{image_a_envoyerfold}"')
time.sleep(4)
print(
    "Si les images ont été redimensionner comme tu le souhaite alors tu peux maintenant les envoyer\ngrâce au "
    "programme '2 - Envoyer_les_images_.py' sinon redimensionne les toi même ;)\n\n\n")

inp = input(
    "Si tu veux ouvrir le script qui permet d'envoyer les images tape 'oui' et appuie sur entrée.\nSinon appuie "
    "juste sur entrée pour fermer ce programme.\nRéponse: ")
if inp == "oui" or inp == "'oui'" or inp == "OUI" or inp == "Oui":
    os.startfile(curpath + "\\2 - Envoyer_les_images.py")
    exit(0)
else:
    exit(0)
