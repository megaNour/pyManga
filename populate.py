import os.path
import re
import argparse
import shutil
from pathlib import Path
from manager import Manager

manager = Manager("../")
parser = argparse.ArgumentParser()
parser.add_argument("-n", type=int, help="number of items ?")
args, unknown = parser.parse_known_args()

if not args.n:
    args.n = 14

extention = Path.cwd().name

chapNum = manager.chapNum

for i in range(1, args.n + 1):
    genericPath = Path(Path.cwd().absolute() / ".." / ".." / "generic" / extention / ("generic." + extention)).resolve()
    destinationFile = manager.seriesName + "_c" + manager.chapNum + "_p" + str(i).zfill(2) + "." + extention
    if not os.path.isfile(destinationFile):
        shutil.copyfile(genericPath, destinationFile)


