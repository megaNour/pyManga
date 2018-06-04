#!/usr/bin/env python3
import constants
import os
import glob
import re
import shutil
import argparse
from manager import Manager
from pathlib import Path

def rename(swapNamePrefix: str, start: int, step: int, patternStr: str, newNamePrefix: str):
    #start becomes the index
    targets = glob.glob("*")
    targets.sort()
    pattern = re.compile(patternStr)
    for path in (path for path in targets if os.path.isfile(path)):
        matcher = pattern.search(path)
        if matcher:        
            newPrefix = newNamePrefix
            if newNamePrefix == "managerInfered":
                newPrefix = manager.getPageName(start, matcher.group(2))                
            newPath = swapNamePrefix + newPrefix
            shutil.move(path, newPath)
        else :
            print(path + " doesn't comply to the patern")
        start += step

def beautify(swapNamePrefix: str = "", start: int = 1, step: int = 1, pattern: str = constants.INDEXED_FILENAME_PATTERN, newNamePrefix="managerInfered"):
    rename("beautiful_", start, step, pattern)
    rename(swapNamePrefix, start, step, pattern)

parser = argparse.ArgumentParser()
parser.add_argument("--pattern", nargs="?", help="pattern to target")
parser.add_argument("--start", nargs="?", help="index start for renamed files")
parser.add_argument("--step", nargs="?", help="increment step for renamed files")
parser.add_argument("--name", nargs="?", help="increment step for renamed files")

args, unknown = parser.parse_known_args()

pattern = args.pattern if args.pattern else constants.INDEXED_FILENAME_PATTERN
start = int(args.start) if args.start else 1
step = int(args.step) if args.step else 1
newNamePrefix = args.name if args.name else "managerInfered"

manager = Manager("..")
beautify(pattern, start=start, step=step, newNamePrefix=newNamePrefix)


