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
parser.add_argument("-s", required=True, help="the script to run from the scribusScriptsPath")
parser.add_argument("-n", required=True, help="the name of the sla file to work with")
parser.add_argument("-a", nargs="*", help="additional arguments for -p you do p:1,2,3,4")

args, unknown = parser.parse_known_args()
#args.D is defined in Webtoonify.py

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
		print(additionalArgs)

printAndRun(scribus + " -g -ns -py " + scribusScriptsPath  + args.s  
+ " -n " + args.n + " -d " + parent + additionalArgs) 
