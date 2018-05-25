#!/usr/bin/python3
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
from subprocess import run
from beautify import beautify
start = time.time()

parser = argparse.ArgumentParser()
parser.add_argument("-i", help="pagination index starts at ?")
parser.add_argument("-m", action='store_true', help="put generic margins between pages")
parser.add_argument("-f", action='store_true', help="put generic footer after pages")
parser.add_argument("-w", help="page width ?")
args, unknown = parser.parse_known_args()

index =  args.i if args.i else 0
width = args.w if args.w else 800

manager = Manager("..")

f = glob.glob("./*.pdf")

fileName = splitext(basename(f[0]))[0]

os.chdir("../release")
for file in glob.glob("*") : os.remove(file)
os.chdir("../scribus")

magick = "" if os.name != "nt" else "magick "
run(magick + "convert -density 300 -scene " + str(index) + " -resize " + str(width) + " " + os.path.abspath(f[0]) + " ../release/" + fileName + ".png", shell=True)
#-crop 3036x4725+236+236 
os.remove(f[0])

os.chdir("../release")
#run (magick + "convert -size " + str(width) + "x" + str(margin) +" canvas:black margin.png")
marginName = "margin.png"
footerName = "footer.png"
marginPath = Path.cwd().parent.parent.absolute() / "generic" / "release" / marginName
footerPath = Path.cwd().parent.parent.absolute() / "generic" / "release" / footerName

margin = " "
footer = " "
append = " "
if args.m:
	margin = " " + marginName + " "
	shutil.copyfile(str(marginPath), marginName)
if args.f:
		footer = " " + footerName + " "
		shutil.copyfile(footerPath, footer.strip())
		append = " -append "

beautify()

command = magick + "convert -colorspace sRGB -append " 


for path in glob.glob("*[0-9].png"):
		foot, marge = footer, margin
		if not manager.getPageNumber(path) > 0:
				foot = marge = " "
		run(magick + "convert" + append + basename(path) + foot + splitext(basename(path))[0] + ".jpg", shell=True)
		command += basename(path) + marge
        
command = re.sub(margin + "$", "", command)
command = re.sub("  +", " ", command)
command += footer + manager.getChapterName() + ".jpg"
print(command)
run(command, shell=True)

for path in glob.glob("*.png"): os.remove(path)

print("time taken: %.2f " % (time.time() - start))


