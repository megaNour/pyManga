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
parser.add_argument("-m", help="margin width between pages ?")
parser.add_argument("-w", help="page width ?")
args, unknown = parser.parse_known_args()

index =  args.i if args.i else 0
width = args.w if args.w else 800

manager = Manager("..")

f = glob.glob("./*.pdf")

fileName = splitext(basename(f[0]))[0]

os.chdir("../release")
for file in glob.glob("*.jpg") : os.remove(file)
os.chdir("../scribus")

magick = "" if os.name != "nt" else "magick "
run(magick + "convert -density 300 -scene " + str(index) + " -resize " + str(width) + " " + f[0] + " ../release/" + fileName + ".png")
#-crop 3036x4725+236+236 
os.remove(f[0])

os.chdir("../release")
#run (magick + "convert -size " + str(width) + "x" + str(margin) +" canvas:black margin.png")
genericPath = Path.cwd().parent.parent.absolute() / "generic" / "release" / "margin.png"
footerPath = Path.cwd().parent.parent.absolute() / "generic" / "release" / "footer.png"

shutil.copyfile(genericPath, "margin.png")

footer = " "
extra = " "
if footerPath.exists():
        footer = " footer.png "
        shutil.copyfile(footerPath, footer.strip())
        extra = " -append "

beautify()

command = magick + "convert -append "


for path in glob.glob("*[0-9].png"):
        foot = footer if manager.getPageNumber(path) > 0 else " "
        run(magick + "convert" + extra + basename(path) + foot + splitext(basename(path))[0] + ".jpg")
        command += basename(path) + " margin.png "
        
command = re.sub("margin.png $", "", command)
command += footer + manager.getChapterName() + ".jpg"
print(command)
run(command)

for path in glob.glob("*.png"): os.remove(path)

print("time taken: %.2f " % (time.time() - start))


