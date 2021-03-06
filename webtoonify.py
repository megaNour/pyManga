#!/usr/bin/python3
import constants
import beautify
from constants import printAndRun
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
parser.add_argument("-i", help="pagination index starts at ?")
parser.add_argument("-m", action="store_true", help="put generic margins between pages")
parser.add_argument("-f", action="store_true", help="put generic footer after pages")
parser.add_argument("-s", nargs="*", help="scribus pdf scrolls to be released, accept x, y, x-z...")
parser.add_argument("-w", help="page width ?")
parser.add_argument("-D", action="store_true", help="spare base pdf flag")

args, unknown = parser.parse_known_args()

index =  args.i if args.i else 0
width = args.w if args.w else 800

manager = Manager("..")
scrollSuffix = "_scroll.jpg"
magick = "" if os.name != "nt" else "magick "
append = " " if not args.f else " -append "

command = magick + "convert -colorspace sRGB -append " 

def doMagick(extraPath="", doCopy=True):
	auxCommand = command
	global append
	for path in sorted(glob.glob("*[0-9].png")):	
		foot = marge = " "
		if args.f:
			foot = " " + str(footerPath) + " "
			append = " -append "
		if args.m:
			marge = " " + str(marginPath) + " "
		#if not manager.getPageNumber(path) > 1:
		#	   foot = marge = " "
		if doCopy:
			printAndRun(magick + "convert" + append + path + foot + extraPath + "../panels/" + path)
		auxCommand += " " + basename(path) + marge
	auxCommand = re.sub(" " + str(marginPath).replace("\\", "/") + " $", "", auxCommand)
	auxCommand = re.sub("  +", " ", auxCommand)
	if args.f: auxCommand += " " + str(footerPath) + " "
	auxCommand += manager.getChapterName() + scrollSuffix
	printAndRun(auxCommand)
	

os.chdir("../release")

for garbage in glob.glob("*"): 
	if os.path.isfile(garbage): os.remove(garbage)
	#empty directories are a crash legacy that interfer with the script. If they are, we'll dispose them.
	elif not os.listdir(garbage): os.rmdir(garbage)

#cleaning	
shutil.rmtree("../scrolls", ignore_errors=True)
shutil.rmtree("../panels", ignore_errors=True)


os.chdir("../scribus")
scrolls = constants.getTargets(glob.glob("*.pdf"), args.s)
#removing only the directories targeted.
#We removed empty dirs and now dirs to be updated. So we keep the not empty dirs that don't need update
for scroll in scrolls: 
	shutil.rmtree("../release/" + splitext(basename(scroll))[0], ignore_errors=True)
	os.mkdir("../release/" + splitext(basename(scroll))[0])

targets = constants.getTargets(glob.glob("*.pdf"), args.s)

for pdf in targets:
	fileName = splitext(basename(pdf))[0]
	subfolder = fileName + "/" # if len(targets) > 1 else ""
	printAndRun(magick + "convert -density 300 -scene " + str(index) + " -resize " + str(width) + " " 
	+ os.path.abspath(pdf) + " ../release/" + subfolder + fileName + ".png")
	#-crop 3036x4725+236+236 

	if not args.D:
		os.remove(pdf)
	
	#run (magick + "convert -size " + str(width) + "x" + str(margin) +" canvas:black margin.png")
	

os.chdir("../release")

os.mkdir("../scrolls")
os.mkdir("../panels")

marginPath = Path.cwd().parent.parent.absolute() / "generic" / "release" / "margin.png"
footerPath = Path.cwd().parent.parent.absolute() / "generic" / "release" / "footer.png"

print("########################################")

beautify.beautify()

listDir = [filtered for filtered in os.listdir(".") if os.path.isdir(filtered)]
releaseDir = os.getcwd()
print(listDir)
for dirName in listDir:
	os.chdir(dirName)	
	print(os.getcwd())
	doMagick("../")
	for pngFile in glob.glob("*.png"):
		shutil.copyfile(pngFile, "../" + pngFile) 
	shutil.move(manager.getChapterName() + scrollSuffix, dirName + scrollSuffix)
	os.chdir(releaseDir)
doMagick(doCopy=False)

for scroll in (scroll for scroll in glob.glob("**/*" + scrollSuffix, recursive=True) if os.path.isfile(scroll)): 
	shutil.move(scroll, "../scrolls/" + basename(scroll))
#for garbage in (garbage for garbage in glob.glob("*/*.jpg") if not garbage.endswith(scrollSuffix)):
#	os.remove(garbage)
for path in glob.glob("*.png"): os.remove(path)
#for path in glob.glob("*.jpg"): shutil.move(path, "../panels/" + path)
beautify.beautify()
os.chdir("../panels")
beautify.beautify(start=0)
for imagePath in glob.glob("*.png"):
	printAndRun(magick + "convert " + imagePath + " -crop 800x1200 " + imagePath.split(".")[0] + "_%d" + ".jpg")
	os.remove(imagePath)

print("time taken: {:.2f}s {}".format((time.time() - start), os.path.basename(__file__)))


