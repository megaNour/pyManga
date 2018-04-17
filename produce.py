import glob, zipfile, os, time
from os.path import basename, splitext
from shutil import move
from subprocess import call
start = time.time()
magick = "" if os.name != "nt" else "magick "
for f in glob.glob("./*[0-9].kra"):
	baseName = (splitext(basename(f))[0])
	zipfile.ZipFile(f, "r").extract("mergedimage.png")
	call(magick + "convert -resize 800 -density 300 mergedimage.png ../jpg/" + baseName + ".jpg")
	move("mergedimage.png", "../png/" + baseName + ".png")
print("time taken: %.2f " % (time.time() - start))