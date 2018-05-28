#!/usr/bin/env python3

import os
import glob
import re
import shutil
from manager import Manager
from pathlib import Path

def beautify():
    manager = Manager("..")
    for path in glob.glob("*[0-9].png") + glob.glob("*[0-9].jpg"):
        p = re.compile("\D(\d+)\.(\w+)$")
        path = os.path.basename(path)
        m = p.search(path)
        if m:
           shutil.move(path, manager.getPageName(int(m.group(1)), m.group(2)))

beautify()                
