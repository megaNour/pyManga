#!/usr/bin/env python3
import constants
import os
import glob
import re
import shutil
import argparse
from manager import Manager
from pathlib import Path

manager = Manager("..")

def rename(swapNamePrefix: str, patternStr: str, newNameSuffix: str):
    #start becomes the index
    targets = glob.glob("*")
    targets.sort()
    pattern = re.compile(patternStr)
    for path in (path for path in targets if os.path.isfile(path)):
        matcher = pattern.search(path)
        if matcher:        
            newPrefix = newNameSuffix
            if newNameSuffix == "managerInfered":
                newPrefix = manager.getPageName(matcher.group(1), matcher.group(2))                
            newPath = swapNamePrefix + newPrefix
            shutil.move(path, newPath)
        else :
            print(path + " doesn't comply to the patern")
        
def reindex(swapNamePrefix: str, start: int, step: int, patternStr: str, newNameSuffix: str):
    #start becomes the index
    targets = glob.glob("*")
    targets.sort()
    pattern = re.compile(patternStr)
    for path in (path for path in targets if os.path.isfile(path)):
        matcher = pattern.search(path)
        if matcher:        
            newPrefix = newNameSuffix
            if newNameSuffix == "managerInfered":
                newPrefix = manager.getPageName(start, matcher.group(2))                
            newPath = swapNamePrefix + newPrefix
            shutil.move(path, newPath)
            start += step
        else :
            print(path + " doesn't comply to the patern")


def beautify(swapNamePrefix: str = "", start: int = 1, step: int = 1, pattern: str = constants.INDEXED_FILENAME_PATTERN, newNameSuffix="managerInfered"):
    rename(beautifulPrefix, pattern, newNameSuffix)
    rename(swapNamePrefix, pattern, newNameSuffix)

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
beautifulPrefix = "beautiful_"


