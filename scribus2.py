#!/usr/bin/env python3
import constants
from constants import printAndRun
from manager import Manager
import glob
#import os.path
import os
#import re
import argparse
#import shutil
from pathlib import Path
import re
import sys

manager = Manager("..")
name = manager.getChapterName()

scribusScriptsPath = os.environ["SCRIBUSSCRIPTSPATH"] + "/"
scribus = "scribusNour.AppImage" if os.name !="nt" else "\"" + os.environ["SCRIBUSPATH"] + "/Scribus.exe" + "\""
pages = ""
parser = argparse.ArgumentParser()
parser.add_argument("-p", nargs="*", help="pages, accept x, y, x-z...")

args, unknown = parser.parse_known_args()
#args.D is defined in Webtoonify.py

pagesArgs = ""
if args.p:
    pagesArgs = "p:" + ",".join(args.p)
    pagesArgs = constants.zfillParamString(pagesArgs, 2)

parent = os.getcwd()

sys.argv.append("-s")
sys.argv.append("pdf2.py")

sys.argv.append("-n")
sys.argv.append(name)

if args.p:
	sys.argv.append("-a")
	sys.argv.append(pagesArgs)

import scribus3
