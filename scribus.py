#!/usr/bin/env python3
import constants
from constants import printAndRun
import glob
#import os.path
import os
#import re
import argparse
#import shutil
from pathlib import Path

scribusPath = os.environ["SCRIBUSPATH"]
scribusScriptsPath = os.environ["SCRIBUSSCRIPTSPATH"] + "/"
scribus = "scribusNour.AppImage" if os.name !="nt" else "\"" + scribusPath + "/Scribus.exe" + "\""
pages = ""
parser = argparse.ArgumentParser()
parser.add_argument("-p", nargs="*", help="pages, accept x, y, x-z...")
parser.add_argument("-s", nargs="*", help="scribus pdf scrolls to be released, accept x, y, x-z...")
#parser.add_argument("-s", default="5", help="size of the step: number of items per pdf? 5 by default - Not implemented for now as working with several small .sla files is prefered than working with a big one")

args, unknown = parser.parse_known_args()
#args.D is defined in Webtoonify.py

pagesArgs = ""
if args.p:
    pagesArgs = " -p " + ",".join(args.p)

scrollsArgs = " -s " + ",".join(glob.glob("*.sla"))
if args.s:
    targets = constants.getTargets(glob.glob("*.sla"), args.s)
    scrollsArgs = " -s " + ",".join(targets)

parent = Path.cwd().absolute()

printAndRun(scribus + " -g -ns -py " + scribusScriptsPath  + "pdf.py" 
+ " -d " + str(parent) + scrollsArgs + pagesArgs)
