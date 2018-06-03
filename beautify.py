#!/usr/bin/env python3
import constants
import os
import glob
import re
import shutil
from manager import Manager
from pathlib import Path


def rename(newNamePrefix):
    i = 0    
    targets = glob.glob("*")
    targets.sort()
    pattern = re.compile(constants.INDEXED_FILENAME_PATTERN)
    for path in (path for path in targets if os.path.isfile(path)):
#    for path in targets if (os.path.isfile(path)):
        matcher = pattern.search(path)
        i += 1
#        newIndex = i if not len(newNamePrefix) else matcher.group(1)
        newIndex = i
        newPath = newNamePrefix + manager.getPageName(newIndex, matcher.group(2))
        if matcher:
           shutil.move(path, newPath)
           #print(manager.getPageName(matcher.group(1), matcher.group(2)))
        else :
           print(path + " doesn't comply to the patern")

def beautify():
    rename("beautiful_")
    rename("")

manager = Manager("..")
beautify()


