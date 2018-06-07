#!/usr/bin/python3
import constants2 as constants
import shutil
import glob
import os
import argparse
from os.path import splitext,basename
from subprocess import run
import re


def findWidestRange(listString):
	flat = " ".join(listString)
	biggest = smallest = None
	pattern = re.compile("(\d+)")
	for x in (int(x) for x in re.findall("(\d+)", flat)):
		print(x)
		biggest = x if biggest is None else x if x > biggest else biggest
		smallest = x if smallest is None else x if x < smallest else smallest
	return str(smallest) + "-" + str(biggest)

rangeStr = ['WASTE_c032_p01.png', 'WASTE_c032_p02.png', 'WASTE_c032_p03.png', 'WASTE_c032_p04.png', 'WASTE_c032_p05.png', 'WASTE_c032_p06.png', 'WASTE_c032_p07.png']
print(constants.zfillParamString(findWidestRange([constants.getFileNameIndexAndExtention(path)[0] for path in rangeStr]), 2))

os.chdir("kra")
print(glob.glob("*.kra"))
print([findWidestRange(constants.getFileNameIndexAndExtention(path)[0] for path in glob.glob("*.kra"))])
