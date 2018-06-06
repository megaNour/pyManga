#!/usr/bin/python3
import constants2 as constants
import shutil
import glob
import os
import argparse
from os.path import splitext,basename
from subprocess import run
parser = argparse.ArgumentParser()
parser.add_argument("-m", action="store_true", help="put generic margins between pages")
parser.add_argument("-f", action="store_true", help="put generic footer after pages")
parser.add_argument("-p", nargs="*", help="scribus pdf scrolls to be released as ranges: a-b, e-g, k, x-z...")
parser.add_argument("-w", help="page width ?")
parser.add_argument("-D", action="store_true", help="spare base pdf flag")
parser.add_argument("-F", action="store_true", help="flush release folder from old cache")
magick = ""


for imagePath in glob.glob("*.jpg"):
	print("coucou")
	indexParam = "_%02d"
	scene = "-scene 1"
	print(magick + "convert -crop 800x1200 " + scene + " " +  imagePath + " " + imagePath.split(".")[0] + indexParam + ".jpg")
	run(magick + "convert -crop 800x1200 " + scene + " " +  imagePath + " " + imagePath.split(".")[0] + indexParam + ".png")
	niceCut = splitext(imagePath)[0].rsplit("_", 1)
	if int(niceCut[1]) == 1 and not os.path.isfile(niceCut[0] + "_" + str(int(niceCut[1])+1).zfill(2) + splitext(imagePath)[1]):
		shutil.move(imagePath, niceCut[0] + splitext(imagePath)[1])
		imagePath = niceCut[0] + splitext(imagePath)[1]
		indexParam = ""
		scene = ""
		print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
	else: print("ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ")
	os.remove(imagePath)
