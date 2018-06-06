#!/usr/bin/python3
import constants2 as constants
import shutil
import glob
import os
import argparse
from os.path import splitext,basename
from subprocess import run
import re
parser = argparse.ArgumentParser()
parser.add_argument("-m", action="store_true", help="put generic margins between pages")
parser.add_argument("-f", action="store_true", help="put generic footer after pages")
parser.add_argument("-p", nargs="*", help="scribus pdf scrolls to be released as ranges: a-b, e-g, k, x-z...")
parser.add_argument("-w", help="page width ?")
parser.add_argument("-D", action="store_true", help="spare base pdf flag")
parser.add_argument("-F", action="store_true", help="flush release folder from old cache")

magick = "" if os.name != "nt" else "magick.exe "


for imagePath in glob.glob("*.jpg"):
	print(magick + "convert -crop 800x1200 -scene 1 " +  imagePath + " " + imagePath.split(".")[0] + ".png")
	run(magick + "convert -crop 800x1200 -scene 1 " +  imagePath + " " + imagePath.split(".")[0] + ".png")
	os.remove(imagePath)
#for imagePath in glob.glob("*-[0-9].png"):
#	shutil.move(imagePath, imagePath.replace("-", "_"))