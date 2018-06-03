#!/usr/bin/python3
import constants
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



os.chdir("../release")
for garbage in glob.glob("*") : shutil.rmtree(garbage, ignore_errors=True)
for garbage in glob.glob("*") : 
    if os.path.isfile(garbage): os.remove(garbage)

os.chdir("../scribus")
scrolls = glob.glob("*.sla")
if len(scrolls) > 0:
    for scroll in scrolls: os.mkdir("../release/" + splitext(basename(scroll))[0])

magick = "" if os.name != "nt" else "magick "
append = " " if not args.f else " -append "

targets = constants.getTargets(glob.glob("./*.pdf"), args.s)
for pdf in targets:
    fileName = splitext(basename(pdf))[0]
    subfolder = fileName + "/" if len(targets) > 1 else ""
    
    printAndRun(magick + "convert -density 300 -scene " + str(index) + " -resize " + str(width) + " " 
    + os.path.abspath(pdf) + " ../release/" + subfolder + fileName + ".png")
    #-crop 3036x4725+236+236 

    if not args.D:
        os.remove(pdf)
    
    #run (magick + "convert -size " + str(width) + "x" + str(margin) +" canvas:black margin.png")
    marginPath = Path.cwd().parent.parent.absolute() / "generic" / "release" / "margin.png"
    footerPath = Path.cwd().parent.parent.absolute() / "generic" / "release" / "footer.png"

os.chdir("../release")

print("########################################")

listDir = [filtered for filtered in os.listdir(".") if os.path.isdir(filtered)]
for dirName in listDir:
    os.chdir(dirName)
    for fileName in glob.glob("*"):
        shutil.copyfile(basename(fileName), "../" + fileName)
    os.chdir("..")

import beautify

command = magick + "convert -colorspace sRGB -append " 

for path in sorted(glob.glob("*[0-9].png")):		
    foot = marge = " "
    if args.f:
        foot = " " + str(footerPath) + " "
        append = " -append "
    if args.m:
        marge = " " + str(marginPath) + " "
    if not manager.getPageNumber(path) > 1:
           foot = marge = " "
    print("for path: " + path + ": " + str(manager.getPageNumber(path)))
    print("foot: " + foot)
    printAndRun(magick + "convert" + append + basename(path) + foot + splitext(basename(path))[0] + ".jpg")
    command += basename(path) + marge
      
command = re.sub(" " + str(marginPath) + " $", "", command)
command = re.sub("  +", " ", command)
if args.f: command += " " + str(footerPath) + " "
command += manager.getChapterName() + ".jpg"
printAndRun(command)

for path in glob.glob("*.png"): os.remove(path)

print("time taken: {:.2f}s {}".format((time.time() - start), os.path.basename(__file__)))


