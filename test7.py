#!/usr/bin/python3
import constants2 as constants
import shutil
import glob
import os
import argparse
from os.path import splitext,basename
from subprocess import run
import re
parser = argparse.ArgumentParser()
parser.add_argument("-m", action="store_true", help="put generic margins between pages")
parser.add_argument("-f", action="store_true", help="put generic footer after pages")
parser.add_argument("-p", nargs="*", help="scribus pdf scrolls to be released as ranges: a-b, e-g, k, x-z...")
parser.add_argument("-w", help="page width ?")
parser.add_argument("-D", action="store_true", help="spare base pdf flag")
parser.add_argument("-F", action="store_true", help="flush release folder from old cache")

args, unknown = parser.parse_known_args()

targets = constants.getTargets(glob.glob("*.pdf"), args.p)
#for imagePath in glob.glob("*-[0-9].png"):
#	shutil.move(imagePath, imagePath.replace("-", "_"))

print(targets)