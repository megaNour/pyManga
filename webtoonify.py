#!/usr/bin/python3
import glob
import zipfile
import os
import time
import sys
import re
from manager import Manager
from os.path import basename, splitext
import shutil
from subprocess import run
start = time.time()

manager = Manager("..")


f = glob.glob("./*.pdf")

fileName = splitext(basename(f[0]))[0]

os.chdir("../release")
for file in glob.glob("*.jpg") : os.remove(file)
os.chdir("../scribus")

magick = "" if os.name != "nt" else "magick "
run(magick + "convert -density 300 -scene 1 -crop 3036x4725+236+236 -resize 800 " + f[0] + " ../release/" + fileName + ".jpg")

#os.remove(f[0])

os.chdir("../release")
import beautify

print("time taken: %.2f " % (time.time() - start))


