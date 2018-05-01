#!/usr/bin/python3
import glob
import zipfile
import os
import time
import sys
import re
from os.path import basename, splitext
import shutil
from subprocess import run
start = time.time()

def produceFile(filePath):
    baseName = (splitext(basename(filePath))[0])
    print(baseName + " ### Production")
    zipfile.ZipFile(filePath, "r").extract("mergedimage.png")
    #run([magick, "convert", "-resize", "800", "-density", "300", "mergedimage.png", "../jpg/" + baseName + ".jpg"], shell=True)
    run(magick + "convert -resize 800 -density 300 mergedimage.png ../jpg/" + baseName + ".jpg", shell=True)
    print("JPG => OK")
    shutil.move("mergedimage.png", "../png/" + baseName + ".png")
    print("PNG => OK")

def findAndProduce(fileIndex):
    f = glob.glob("./*_p" + fileIndex.zfill(2) + ".kra")
    if f:
        print(f)
        produceFile(f[0])

os.makedirs("../jpg/", exist_ok=True)
os.makedirs("../png/", exist_ok=True)
magick = "" if os.name != "nt" else "magick "

#Batch <= because no specific file indicated
if len(sys.argv) == 1 :
    print(sys.argv)
    print(len(sys.argv))
    for f in glob.glob("./*[0-9].kra"):
        print(f)
        produceFile(f)
else:
    for s in sys.argv[1:len(sys.argv)]:
        if("-" not in s):
            findAndProduce(s)
        else:
            split = s.split("-")
            for i in range(int(split[0]), int(split[1])+1):
                findAndProduce(str(i))
                
print("time taken: %.2f " % (time.time() - start))


