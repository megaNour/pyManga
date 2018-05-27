import os
import glob
from manager import Manager
from pathlib import Path
manager = Manager("..")

for path in glob.glob("*[0-9].png"):
		foot = "yes" if manager.getPageNumber(path) > 0 else "no"
		print(path + " " + foot)


