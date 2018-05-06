import os
import glob
import re
import shutil
from manager import Manager
from pathlib import Path

manager = Manager("..")
for path in glob.glob("*.png") + glob.glob("*.jpg"):
    p = re.compile(".+-(\d+)\.(\w+)$")
    path = os.path.basename(path)
    m = p.search(path)
    if m:
        shutil.move(path, manager.getPageName(int(m.group(1))+1, m.group(2)))

                
