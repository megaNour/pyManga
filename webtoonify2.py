#!/usr/bin/python3
import pyManga.constants2 as constants
from pyManga.constants2 import printAndRun
from pyManga.manager import Manager
import glob
import zipfile
import os
import time
import sys
import re
import argparse

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
parser.add_argument("-S", action="store_true", help="Ignore your scribus/sequence.txt, because...you can")

args, unknown = parser.parse_known_args()

width = args.w if args.w else 800

manager = Manager("..")
scrollSuffix = "_scroll.jpg"
magick = "" if os.name != "nt" else "magick "
append = " " if not args.f else " -append "

command = magick + "convert -colorspace sRGB -append "

def findWidestRange(listString):
	flat = " ".join(listString)
	biggest = smallest = None
	pattern = re.compile("(\d+)")
	for x in (int(x) for x in re.findall("(\d+)", flat)):
		biggest = x if biggest is None else x if x > biggest else biggest
		smallest = x if smallest is None else x if x < smallest else smallest
	return str(smallest) + "-" + str(biggest)

def getDefaultSequence(globTarget):
	targets = None
	allDone = False
	if os.path.isfile("../scribus/sequence.txt") and not args.S:
		file = open("../scribus/sequence.txt", "r")
		targetsString = file.readline().strip()
		file.close()
		targets = targetsString.split()
	elif not args.p:
		os.chdir("../kra")
		targets = [findWidestRange(constants.getFileNameIndexAndExtention(path)[0] for path in glob.glob("*.kra"))]
		os.chdir("../release")
		allDone = True
	scrollTargets = list()
	if targets:
		for scrollString in targets:
			scrollTargets.append(constants.getTargets(globTarget, constants.listString(scrollString)))
	return list(scrollTargets), allDone

def makeScrolls(targets, extraPath=""):
	scrollIndex = 0
	if len(extraPath):	os.mkdir("../scrolls/" + extraPath)
	for rangeStr in targets:
			scrollIndex += 1
			auxCommand = command
			print("SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
			for panel in rangeStr:
				export = magick + "convert" + append + panel + foot + "../panels/" + panel
				if int(manager.getPageNumber(panel)) == 1: export = export.replace(foot, " ")
				printAndRun(export)
				auxCommand += " " + basename(panel) + marge
			auxCommand = re.sub(" " + str(marginPath).replace("\\", "/") + " $", "", auxCommand)
			auxCommand = re.sub("  +", " ", auxCommand)
			auxCommand = auxCommand.replace(marge, " ", 1)
			if args.f: auxCommand += " " + str(footerPath) + " "
			auxCommand += "../scrolls/" + extraPath  + manager.getChapterName() + splitext(scrollSuffix)[0] + "_" + constants.zfillParamString(findWidestRange([constants.getFileNameIndexAndExtention(path)[0] for path in rangeStr]), 2) + splitext(scrollSuffix)[1]
			printAndRun(auxCommand)

def doMagick():
	auxCommand = command
	pngGlob = sorted(glob.glob("*.png"))
	targets = None
	targets, allDone = getDefaultSequence(pngGlob)
	snapshots = []
	if targets:	makeScrolls(targets)
	if args.p:
		for sequence in args.p:
			snapshots.append(constants.getTargets(pngGlob, constants.listString(sequence)))
		makeScrolls(snapshots, "snapshots/")
	mainScrollPath = "../scrolls/" + manager.getChapterName() + scrollSuffix
	if not allDone:
		bigScroll = sorted(glob.glob("*.png"))
		auxCommand = command + marge.join(bigScroll).strip() + foot + mainScrollPath
		auxCommand = auxCommand.replace(marge, " ", 1)
		printAndRun(auxCommand)
	else:
		scrollWithUsellRange = os.listdir("../scrolls")[0]
		shutil.move("../scrolls/" + scrollWithUsellRange, mainScrollPath)
		print("########################################################################################################")
		print("########################################################################################################")
		print("moved: " + scrollWithUsellRange + " to " + mainScrollPath)
		print("define a sequence.txt in your scribus subfolder to define the range of subscrolls based on your sla file")
		print("########################################################################################################")
		print("########################################################################################################")

if args.F:
	shutil.rmtree("../release", ignore_errors=True)
	os.mkdir("../release")

os.chdir("..")

shutil.rmtree("scrolls", ignore_errors=True)
shutil.rmtree("panels", ignore_errors=True)

os.chdir("scribus")

targets = constants.getTargets(glob.glob(manager.getChapterName() + "*.pdf"), args.p)
for pdf in targets:
	fileName = splitext(basename(pdf))[0]
	fileShortName = constants.removeRange(fileName)
	match = constants.getIndexStart(fileName)
	index = "1" if match is None else str(match.group(1))

	printAndRun(magick + "convert -density 300 -scene " + index + " -resize " + str(width) + " "
	+ pdf + " ../release/" + manager.getChapterName() + "_p%02d.png")

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

doMagick()

os.chdir("../panels")

for imagePath in glob.glob("*.png"):
	printAndRun(magick + "convert -crop 800x1200 -scene 1 " +  imagePath + " " + imagePath.split(".")[0] + ".jpg")
	os.remove(imagePath)

print("time taken: {:.2f}s {}".format((time.time() - start), os.path.basename(__file__)))

