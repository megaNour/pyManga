#!/usr/bin/env python3

import glob
import os.path
import re
import argparse
import shutil
from pathlib import Path
from manager import Manager

manager = Manager("../")
parser = argparse.ArgumentParser()
parser.add_argument("-n", required=True, type=int, help="number of items ?")
parser.add_argument("-A", action="store_true", help="flag for not additional but total number")
parser.add_argument("-i", type=int, help="insert after page so for i=21 you get p21_2, p21_3, p21_4 with s a double digit page num")

args, unknown = parser.parse_known_args()

if not args.A and not args.i:
	listKra = glob.glob("*[0-9].kra")
	args.n += len(listKra)


extention = Path.cwd().name

chapNum = manager.chapNum

index = "" if not args.i else str(args.i).zfill(2) + "_"

genericPath = Path(Path.cwd().absolute() / ".." / ".." / "generic" / extention / ("generic." + extention)).resolve()

for i in range(1, args.n + 1):
	destinationFile = manager.seriesName + "_c" + manager.chapNum + "_p" + index + str(i).zfill(2) + "." + extention
	if not os.path.isfile(destinationFile):
		shutil.copyfile(str(genericPath), destinationFile)

