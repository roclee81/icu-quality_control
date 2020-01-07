#!/usr/bin/python3
import os
import time
import shutil
from bypy import ByPy

os.system("mount /dev/sda1 /mnt/usb")
time.sleep(10)

t = time.strftime("%Y-%m-%d %H-%M", time.localtime())
shutil.copy(
    "/home/pi/piserver/django-addon.exe",
    "/mnt/usb/bypy/notebook/%s-django-addon.exe" %
    t)

os.chdir("/mnt/usb/bypy")

bp = ByPy()
bp.syncup()

os.chdir("/home/pi")

time.sleep(10)
os.system("umount /mnt/usb")
