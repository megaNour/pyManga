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

scribusScriptsPath = os.environ["SCRIBUSSCRIPTSPATH"] + "/"
scribus = "scribusNour.AppImage" if os.name !="nt" else "\"" + os.environ["SCRIBUSPATH"] + "/Scribus.exe" + "\""
pages = ""
parser = argparse.ArgumentParser()
parser.add_argument("-s", required=True, help="the script to run from the scribusScriptsPath")
parser.add_argument("-a", nargs="*", help="additional arguments for -p you do p:1,2,3,4")

args, unknown = parser.parse_known_args()
#args.D is defined in Webtoonify.py

print(sys.argv)

parent = os.getcwd()

additionalArgs = ""
if args.a:
	for argString in args.a:
		split = argString.split(":")
		flag = "-" + split[0]
		arguments = " ".join(split[1].split(","))
		argument = " " + flag + " " + arguments
		print("injecting argument: " + argument)
		additionalArgs += argument
		additionalArgs = additionalArgs.rstrip()


printAndRun(scribus + " -g -ns -py " + scribusScriptsPath  + args.s
+ " -d " + parent + additionalArgs)
