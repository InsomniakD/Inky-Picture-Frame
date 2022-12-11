#!/usr/bin/env python3

import os
import random
import shutil
import signal
import subprocess
import time
import RPi.GPIO as GPIO
from PIL import Image
from inky.inky_uc8159 import Inky
from threading import Thread

synctime = subprocess.call("/home/pi/Inky/schedules/syncTime.sh")

Hactu = int(time.strftime('%H', time.localtime()))

if Hactu < 5:
    subprocess.Popen("/home/pi/Inky/schedules/add_startup_shutdown_night.sh")
    exec(open("/home/pi/Inky/clean.py").read())
else:
    subprocess.Popen("/home/pi/Inky/schedules/add_startup_shutdown_3min_15min.sh")

if os.path.isdir("/home/pi/Inky/image_spe"):
    exec(open("/home/pi/Inky/image_spe/message_spe.py").read())
    exit()

with open("/home/pi/Inky/cycle.txt", 'r') as ccl:
    nbcyclelist = ccl.readline()
    ccl.close()

with open("/home/pi/Inky/cycle.txt", 'w') as ccl:
    if nbcyclelist == '':
        nbcycle = 0
    else:
        nbcycle = int(nbcyclelist)

    if nbcycle < 5:
        ccl.write(str(nbcycle + 1))
    elif nbcycle == 5:
        exec(open("/home/pi/Inky/clear.py").read())
        ccl.write("0")
    else:
        ccl.write("0")

recent = "/home/pi/Inky/recent"
diapo = "/home/pi/Inky/diapo"
save = "/home/pi/Inky/savepic"
inky = Inky()
saturation = 0.5
os.umask(0)

BUTTONS = [5, 6, 16, 24]  # A ,B ,C ,D
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_UP)

if len(os.listdir(save)) == 0:
    image = Image.open("/home/pi/Inky/img/no_image.jpg")
    inky.set_image(image, saturation=saturation)
    inky.show()
    exit()

def handle_but_run(pin):
    global run
    if run == 0:
        run = 1
        if Hactu < 6:
            subprocess.Popen("/home/pi/Inky/schedules/add_shutdown_night.sh")
        else:
            subprocess.Popen("/home/pi/Inky/schedules/add_startup_shutdown_4min_14min.sh")
        if pin == 5:
            Thread(target=next_pic).start()
        elif pin == 6:
            Thread(target=previous_pic).start()
        elif pin == 16:
            Thread(target=clean_screen).start()
        else:  # pin 24
            Thread(target=delete_pic).start()
    else:
        pass

def next_pic():
    global run, nbrL, nbrline, order_lines, current_pic
    if nbrL == nbrline or nbrL == nbrline-1:   #if there is no previous pic button press before
            if len(os.listdir(diapo)) == 0:
                os.rmdir(diapo)
                shutil.move(recent, diapo)
                os.mkdir(recent)
            current_pic=random.choice([x for x in os.listdir(diapo)if os.path.isfile(os.path.join(diapo, x))])
            if len(order_lines) > 1:
                for i in range(10):
                    if current_pic == order_lines[nbrline-1]:
                        current_pic = random.choice([x for x in os.listdir(diapo) if os.path.isfile(os.path.join(diapo, x))])
                    else:
                        break
            image = Image.open(diapo + "/" + current_pic)
            inky.set_image(image, saturation=saturation)
            inky.show()
            with open("/home/pi/Inky/order.txt", 'a') as aorder:
                aorder.write(current_pic + "\n")
                aorder.close()
            shutil.move(diapo + "/" + current_pic, recent + "/" + current_pic)
            with open("/home/pi/Inky/order.txt",'r') as orderln:
                order_lines = [line.rstrip('\n') for line in orderln]
                nbrline = len(order_lines)
                orderln.close()
            nbrL = nbrline

    else:
        nbrL+=1
        pic = order_lines[nbrL]
        image = Image.open(save + "/" + pic)
        inky.set_image(image, saturation=saturation)
        inky.show()
        current_pic = pic
    run = 0


def previous_pic():
    global run, nbrL, order_lines, current_pic
    nbrL-=1
    if nbrL >= 0:
        pic = order_lines[nbrL]
        if pic == current_pic:
            nbrL-=1
            pic = order_lines[nbrL]
        image = Image.open(save + "/" + pic)
        inky.set_image(image, saturation=saturation)
        inky.show()
        current_pic = pic
    elif nbrL == -1:
        image = Image.open("/home/pi/Inky/img/histo_fin.jpg")
        inky.set_image(image, saturation=saturation)
        inky.show()
        current_pic = ""
    elif nbrL < -1:
        nbrL = -1
    run = 0

def clean_screen():
    global run, current_pic
    exec(open("/home/pi/Inky/clean.py").read())
    current_pic = ""
    run = 0
    return


def delete_pic():
    global run, nbrL, nbrline, order_lines, current_pic

    if nbrL == nbrline and current_pic != ""  :
        image = Image.open("/home/pi/Inky/img/sure_delete.jpg")
        inky.set_image(image, saturation=saturation)
        inky.show()

        start = time.time()
        det = 0
        while time.time() - start < 20 :
            if GPIO.input(5):
                pass
            else:
                det = 5
                break
            if GPIO.input(24):
                pass
            else:
                det = 24
                break
            time.sleep(0.001)

        if det == 24:
            if os.path.exists(save +"/"+ current_pic):
                os.remove(save +"/"+ current_pic)
            if os.path.exists(diapo +"/"+ current_pic):
                os.remove(diapo +"/"+ current_pic)
            else:
                os.remove(recent +"/"+ current_pic)
            with open("/home/pi/Inky/order.txt", 'r') as rorder:
                lines = rorder.readlines()
                rorder.close()
            with open("/home/pi/Inky/order.txt", 'w') as worder:
                for line in lines:
                    if line.strip("\n") != current_pic:
                        worder.write(line)
                worder.close()
            with open("/home/pi/Inky/order.txt",'r') as orderln:
                order_lines = [line.rstrip('\n') for line in orderln]
                nbrline = len(order_lines)
                orderln.close()
            nbrL=nbrline
            current_pic = ""
            image = Image.open("/home/pi/Inky/img/image_suprimee.jpg")
            inky.set_image(image, saturation=saturation)
            inky.show()

        else:#answer no or timeout
            image = Image.open(save + "/" + current_pic)
            inky.set_image(image, saturation=saturation)
            inky.show()


    elif current_pic != ""  :

        image = Image.open("/home/pi/Inky/img/sure_delete.jpg")
        inky.set_image(image, saturation=saturation)
        inky.show()

        start = time.time()
        det = 0
        while time.time() - start < 20 :
            if GPIO.input(5):
                pass
            else:
                det = 5
                break
            if GPIO.input(24):
                pass
            else:
                det = 24
                break
            time.sleep(0.001)

        if det == 24:
            if os.path.exists(save +"/"+ current_pic):
                os.remove(save +"/"+ current_pic)
            if os.path.exists(diapo +"/"+ current_pic):
                os.remove(diapo +"/"+ current_pic)
            else:
                os.remove(recent +"/"+ current_pic)
            with open("/home/pi/Inky/order.txt", 'r') as rorder:
                lines = rorder.readlines()
                rorder.close()
            with open("/home/pi/Inky/order.txt", 'w') as worder:
                i=1
                nbr_li = nbrL
                for line in lines:
                    if line.strip("\n") != current_pic:
                        worder.write(line)
                        i+=1
                    else:
                        if i < nbrL:
                            nbr_li = nbr_li - 1
                        i+=1
                nbrL = nbr_li
                worder.close()
            with open("/home/pi/Inky/order.txt",'r') as orderln:
                order_lines = [line.rstrip('\n') for line in orderln]
                nbrline = len(order_lines)
                orderln.close()
            current_pic =""
            image = Image.open("/home/pi/Inky/img/image_suprimee.jpg")
            inky.set_image(image, saturation=saturation)
            inky.show()

        else:#answer no or timeout
            image = Image.open(save +"/"+ current_pic)
            inky.set_image(image, saturation=saturation)
            inky.show()

    else:
        image = Image.open("/home/pi/Inky/img/no_image.jpg")
        inky.set_image(image, saturation=saturation)
        inky.show()
        current_pic = ""
    run = 0


with open("/home/pi/Inky/order.txt", 'r') as orderln:
    order_lines = [line.rstrip('\n') for line in orderln]
    nbrline = len(order_lines)
    orderln.close()

if not os.path.exists(diapo):
    os.mkdir(diapo)
    if os.path.exists(recent):
        shutil.rmtree(recent)
    os.mkdir(recent)
    src_files = os.listdir(save)
    for file_name in src_files:
        full_file_name = os.path.join(save, file_name)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, diapo)

if not os.path.exists(recent):
    os.mkdir(recent)
    if os.path.exists(diapo):
        shutil.rmtree(diapo)
    os.mkdir(diapo)
    src_files = os.listdir(save)
    for file_name in src_files:
        full_file_name = os.path.join(save, file_name)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, diapo)

if len(os.listdir(diapo)) == 0:
    os.rmdir(diapo)
    shutil.move(recent, diapo)
    os.mkdir(recent)
    current_pic=random.choice([x for x in os.listdir(diapo)if os.path.isfile(os.path.join(diapo, x))])
    if len(order_lines) > 1:
        for i in range(10):
            if current_pic == order_lines[nbrline-1]:
                current_pic = random.choice([x for x in os.listdir(diapo) if os.path.isfile(os.path.join(diapo, x))])
            else:
                break
    image = Image.open(diapo + "/" + current_pic)
    inky.set_image(image, saturation=saturation)
    inky.show()
    with open("/home/pi/Inky/order.txt", 'a') as aorder:
        aorder.write(current_pic + "\n")
        aorder.close()
    shutil.move(diapo + "/" + current_pic, recent + "/" + current_pic)

else:
    current_pic=random.choice([x for x in os.listdir(diapo)if os.path.isfile(os.path.join(diapo, x))])
    if len(order_lines) > 1:
        for i in range(10):
            if current_pic == order_lines[nbrline-1]:
                current_pic = random.choice([x for x in os.listdir(diapo) if os.path.isfile(os.path.join(diapo, x))])
            else:
                break
    image = Image.open(diapo + "/" + current_pic)
    inky.set_image(image, saturation=saturation)
    inky.show()
    nbimage=len(os.listdir(recent))
    with open("/home/pi/Inky/order.txt", 'a') as aorder:
        aorder.write(current_pic + "\n")
        aorder.close()
    shutil.move(diapo + "/" + current_pic, recent + "/" + current_pic)

with open("/home/pi/Inky/order.txt",'r') as orderln:
            order_lines = [line.rstrip('\n') for line in orderln]
            nbrline = len(order_lines)
            orderln.close()


if nbrline >= 25:
    with open("/home/pi/Inky/order.txt", 'w') as fout:
        for i in range(nbrline-15,nbrline-1):
            linei = order_lines[i]
            fout.writelines(linei+"\n")
        fout.close()
    with open("/home/pi/Inky/order.txt",'r') as orderln:
        order_lines = [line.rstrip('\n') for line in orderln]
        nbrline = len(order_lines)
        orderln.close()

nbrL = nbrline

for pin in BUTTONS:
    GPIO.add_event_detect(pin, GPIO.FALLING, handle_but_run, bouncetime=200)

run = 0
signal.pause()