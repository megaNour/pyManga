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

manager = Manager("..")
name = manager.getChapterName()

scribusScriptsPath = os.environ["SCRIBUSSCRIPTSPATH"] + "/"
scribus = "scribusNour.AppImage" if os.name !="nt" else "\"" + os.environ["SCRIBUSPATH"] + "/Scribus.exe" + "\""
pages = ""
parser = argparse.ArgumentParser()
parser.add_argument("-s", required=True, nargs="*", help="the script to run from the scribusScriptsPath")
parser.add_argument("-n", required=True, help="the name of the sla file to work with")
parser.add_argument("-a", help="additional arguments")

args, unknown = parser.parse_known_args()
#args.D is defined in Webtoonify.py

additionalArgs = ""
if args.a:
	additionalArgs = args.ab

if args.p:
    pagesArgs = " -p " + ",".join(args.p)
    pagesArgs = constants.zfillParamString(pagesArgs, 2)

parent = os.getcwd()

printAndRun(scribus + " -g -ns -py " + scribusScriptsPath  + args.s  
+ " -n " + args.n + " -d " + parent + additionalArgs) 
