#!/usr/bin/env python3
import constants2 as constants
import os
import glob
import re
import shutil
import argparse
from manager import Manager
from pathlib import Path

manager = Manager("..")

def rename(swapNamePrefix, globExpr):
	#start becomes the index
	start = step = 1
	targets = sorted(glob.glob(globExpr))
	pattern = re.compile(constants.INDEXED_FILENAME_PATTERN)
	for path in (path for path in targets if os.path.isfile(path)):
		matcher = pattern.search(path)
		if matcher:		
			newName = manager.getPageName(start, matcher.group(2))				
			newPath = swapNamePrefix + newName
			shutil.move(path, newPath)
			start += step
		else :
			print(path + " doesn't comply to the patern")
	return target

def beautify():
	target = rename(beautifulPrefix, "*.kra")
	rename(beautifulPrefix, "*.kra~")
	rename("", "*.kra")
	rename("", "*.kra~")
	if target != glob.glob("*.kra")

	
'''
parser = argparse.ArgumentParser()
parser.add_argument("--pattern", nargs="?", help="pattern to target")
parser.add_argument("--start", nargs="?", help="index start for renamed files")
parser.add_argument("--step", nargs="?", help="increment step for renamed files")
parser.add_argument("--name", nargs="?", help="increment step for renamed files")

args, unknown = parser.parse_known_args()

pattern = args.pattern if args.pattern else constants.INDEXED_FILENAME_PATTERN
start = int(args.start) if args.start else 1
step = int(args.step) if args.step else 1
newNameSuffix = args.name if args.name else "managerInfered"
'''
beautifulPrefix = "beautiful_"

beautify()

