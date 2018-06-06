#!/usr/bin/python3
import constants2 as constants
import shutil
import glob
import os
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-m", action="store_true", help="put generic margins between pages")
parser.add_argument("-f", action="store_true", help="put generic footer after pages")
parser.add_argument("-p", nargs="*", help="scribus pdf scrolls to be released as ranges: a-b, e-g, k, x-z...")
parser.add_argument("-w", help="page width ?")
parser.add_argument("-D", action="store_true", help="spare base pdf flag")
parser.add_argument("-F", action="store_true", help="flush release folder from old cache")

args, unknown = parser.parse_known_args()

magick = "" if os.name != "nt" else "magick "
append = " " if not args.f else " -append "

command = magick + "convert -colorspace sRGB -append " 

auxCommand = command
print(args.p)
pngGlob = sorted(glob.glob("*.jpg"))
targets = list()
print(pngGlob)
print("////////////////////////////////")
if not args.p:
		if os.path.isfile("../scribus/sequence.txt"):
			file = open("../scribus/sequence.txt", "r")
			args.p = file.readline().strip()
			file.close()
			targets = args.p.split()
		else: targets = list(pngGlob)
		targets = constants.getTargets(pngGlob, constants.listList(targets))
else:
	for sequence in args.p:		
		targets.extend(constants.getTargets(pngGlob, constants.listString(sequence)))

print(targets)
