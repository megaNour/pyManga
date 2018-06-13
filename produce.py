#!/usr/bin/python3
from constants import printAndRun
import glob
import zipfile
import os
import time
import sys
import re
from os.path import basename, splitext
import shutil
from subprocess import run
import argparse
from os.path import basename, splitext
import shutil

parser = argparse.ArgumentParser()
parser.add_argument("-p", nargs="*", help="pages to be released >>> FROM ALL SCRIBUS SCROLLS <<<, accept x, y, x-z...")

args, unknown = parser.parse_known_args()

start = time.time()

def produceFile(filePath):
	baseName = (splitext(basename(filePath))[0])
	print(baseName + " ### Production")
	zipfile.ZipFile(filePath, "r").extract("mergedimage.png")
	#run([magick, "convert", "-resize", "800", "-density", "300", "mergedimage.png", "../jpg/" + baseName + ".jpg"], shell=True)
	printAndRun(magick + "convert -resize 800 -density 300 mergedimage.png ../jpg/" + baseName + ".jpg")
	print("JPG => OK")
	shutil.move("mergedimage.png", "../png/" + baseName + ".png")
	print("PNG => OK")

def findAndProduce(fileIndex):
	f = glob.glob("./*_p" + fileIndex.zfill(2) + ".kra")
	if f:
		print(f)
		produceFile(f[0])

def produceList(listRanges):
	if "-" not in s:
		findAndProduce(s)
	elif not s.startswith("-") :
		split = s.split("-")
		max = int(split[1]) if split[1] != "end" else len(glob.glob("*.kra"))
		for i in range(int(split[0]), max + 1):
			findAndProduce(str(i))

os.makedirs("../jpg/", exist_ok=True)
os.makedirs("../png/", exist_ok=True)
magick = "" if os.name != "nt" else "magick "

#Batch <= because no specific file indicated
args.p = args.p if args.p else sys.argv[1:]
if args.p:
	for s in args.p :
		produceList(s)
else :
	for f in sorted(glob.glob("./*[0-9].kra")):
		print(f)
		produceFile(f)

print("time taken: {:.2f}s {}".format((time.time() - start), os.path.basename(__file__)))

