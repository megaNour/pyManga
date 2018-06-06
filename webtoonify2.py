#!/usr/bin/python3
import constants2 as constants
from constants2 import printAndRun
import glob
import zipfile
import os
import time
import sys
import re
import argparse
from manager import Manager
from os.path import basename, splitext
from pathlib import Path
import shutil
start = time.time()

parser = argparse.ArgumentParser()
parser.add_argument("-m", action="store_true", help="put generic margins between pages")
parser.add_argument("-f", action="store_true", help="put generic footer after pages")
parser.add_argument("-p", nargs="*", help="scribus pdf scrolls to be released as ranges: a-b, e-g, k, x-z...")
parser.add_argument("-w", help="page width ?")
parser.add_argument("-D", action="store_true", help="spare base pdf flag")
parser.add_argument("-F", action="store_true", help="flush release folder from old cache")

args, unknown = parser.parse_known_args()

width = args.w if args.w else 800

manager = Manager("..")
scrollSuffix = "_scroll.jpg"
magick = "" if os.name != "nt" else "magick "
append = " " if not args.f else " -append "

command = magick + "convert -colorspace sRGB -append " 

def doMagick():
	auxCommand = command
	pngGlob = sorted(glob.glob("*.png"))
	print("GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG1")	
	print(pngGlob)
	targets = None
	if not args.p:
		print("GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG2")
		print(pngGlob)
		if os.path.isfile("../scribus/sequence.txt"):
			print("GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG3")	
			print(pngGlob)
			file = open("../scribus/sequence.txt", "r")
			args.p = file.readline().strip()
			file.close()
			targets = args.p.split()
		else: targets = list(pngGlob)
		print("GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG4")	
		print(targets)
		scrollTargets = list()
		for scrollString in targets:
			scrollTargets.append(constants.getTargets(pngGlob, constants.listString(scrollString)))
		print("GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG7")	
		print(targets)
		print(scrollTargets)
		targets = list(scrollTargets)
	else:
		print("GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG5")	
		print(args.p)
		targets = []
		for sequence in args.p:		
			targets.append(constants.getTargets(pngGlob, constants.listString(sequence)))
	scrollIndex = 0
	for path in targets:
		scrollIndex += 1
		auxCommand = command
		print("GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG6")	
		print(targets)
		print(path)
		for fragment in path:
			printAndRun(magick + "convert" + append + fragment + foot + "../panels/" + fragment)
			auxCommand += " " + basename(fragment) + marge
		auxCommand = re.sub(" " + str(marginPath).replace("\\", "/") + " $", "", auxCommand)
		auxCommand = re.sub("  +", " ", auxCommand)
		auxCommand = auxCommand.replace(marge, " ", 1)
		if args.f: auxCommand += " " + str(footerPath) + " "
		auxCommand += "../scrolls/" + manager.getChapterName() + splitext(scrollSuffix)[0] + "_" + str(scrollIndex).zfill(2) + splitext(scrollSuffix)[1]
		printAndRun(auxCommand)
	bigScroll = glob.glob("*.png")
	auxCommand = command + marge.join(bigScroll).strip() + foot + "../scrolls/" + manager.getChapterName() + scrollSuffix
	auxCommand = auxCommand.replace(marge, " ", 1)
	printAndRun(auxCommand)

if args.F:
	shutil.rmtree("../release", ignore_errors=True)
	os.mkdir("../release")

os.chdir("..")

#cleaning	
shutil.rmtree("scrolls", ignore_errors=True)
shutil.rmtree("panels", ignore_errors=True)


os.chdir("scribus")
scrolls = constants.getTargets(glob.glob("*.pdf"), args.p)

print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
print(glob.glob("*.pdf"))
print("###############")
targets = constants.getTargets(glob.glob("*.pdf"), args.p)
print(targets)
for pdf in targets:
	fileName = splitext(basename(pdf))[0]
	fileShortName = constants.removeRange(fileName)
	print(pdf)
	match = constants.getIndexStart(fileName)
	index = "1" if match is None else str(match.group(1))

	printAndRun(magick + "convert -density 300 -scene " + index + " -resize " + str(width) + " " 
	+ pdf + " ../release/" + fileShortName + "_p%02d.png")	

	if not args.D:
		os.remove(pdf)

os.chdir("../release")

os.mkdir("../scrolls")
os.mkdir("../panels")

marginPath = Path.cwd().parent.parent.absolute() / "generic" / "release" / "margin.png"
footerPath = Path.cwd().parent.parent.absolute() / "generic" / "release" / "footer.png"

foot = marge = " "
if args.f:
	foot = " " + str(footerPath) + " "
	append = " -append "
if args.m:
	marge = " " + str(marginPath) + " "

print("########################################")
doMagick()
print("\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\")

print(os.getcwd())
os.chdir("../panels")

for imagePath in glob.glob("*.png"):
	printAndRun(magick + "convert -crop 800x1200 -scene 1 " +  imagePath + " " + imagePath.split(".")[0] + ".jpg")
	os.remove(imagePath)
#for imagePath in glob.glob("*-[0-9].jpg"):
#	shutil.move(imagePath, imagePath.replace("-", "_"))

print("time taken: {:.2f}s {}".format((time.time() - start), os.path.basename(__file__)))


