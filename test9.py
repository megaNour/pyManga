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
		biggest = x if biggest is None else x if x > biggest else biggest
		smallest = x if smallest is None else x if x < smallest else smallest
	return str(smallest) + "-" + str(biggest)

os.chdir("../kra")
print(glob.glob("*.kra"))
targets = [findWidestRange(constants.getFileNameIndexAndExtention(path)[0] for path in glob.glob("*.kra"))]
os.chdir("../release")
print(targets)
