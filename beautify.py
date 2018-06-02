#!/usr/bin/env python3

import os
import glob
import re
import shutil
from manager import Manager
from pathlib import Path


def rename(newNamePrefix):
    i = 0    
    targets = glob.glob("*." + Path.cwd().name)
    targets.sort()
    p = re.compile("p(\d+.*)\.(\w+$)")
    for path in (path for path in targets if os.path.isfile(path)):      
        m = p.search(path)
        i += 1
        newIndex = i if not len(newNamePrefix) else m.group(1)
        newPath = newNamePrefix + manager.getPageName(newIndex, m.group(2))
        if m:
           shutil.move(path, newPath)
           #print(manager.getPageName(m.group(1), m.group(2)))
        else :
           print(path + " doesn't comply to the patern")

def beautify():
    rename("beautiful_")
    rename("")

manager = Manager("..")
beautify()


