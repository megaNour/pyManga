#!/usr/bin/env python3
import pyManga.constants2 as constants
from pyManga.manager import Manager
import os
import glob
import re
import shutil
from pathlib import Path
from os.path import splitext
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-g", nargs="*", help="list of globs you are targeting, otherwise *")
parser.add_argument("-I", action="store_true" , help="do not reIndex")

args, unknown = parser.parse_known_args()

manager = Manager("..")

def rename(swapNamePrefix="beautiful_", globExpr = "*"):
	index = step = 1
	targets = sorted(glob.glob(globExpr))
	pattern = re.compile(constants.INDEXED_FILENAME_PATTERN)
	for path in (path for path in targets if os.path.isfile(path)):
		matcher = pattern.search(path)
		if matcher:
			pageNum = index if not args.I else matcher.group(1)
			newName = manager.getPageName(pageNum)
			newPath = swapNamePrefix + newName + ".kra"
			shutil.move(path, newPath)
			index += step
		else :
			print(path + " doesn't comply to the patern")
	return targets

def swapExtention(old: str, new: str, items: list):
	return [re.sub("\." + old + "$", "." + new, item) for item in items]

def swapXml(xml, targets, prefix):
	print(targets)
	print(prefix + "777777777777777777777777777777777777777777777777")
	index = 1
	for adress in targets:
		print("replacing: " + splitext(adress)[0] + " by: " + prefix + manager.getPageName(index))
		xml = re.sub("(\W)" + splitext(adress)[0], lambda x:x.group(1) + prefix + manager.getPageName(index),xml)
		index += 1
	return xml

def beautify(globs):

	for globExpr in globs:
		before = rename(globExpr=globExpr)
		rename("", globExpr)

	if "*.kra" in globs:
		after = sorted(glob.glob("*.kra"))
		#if before != after and len(after) > 0:
		print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
		print("!!!!!!!!!!!!!!!!!!!beautification!!!!!!!!!!!!!!!!!!!")
		print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
		#before = "b:" + ",".join(swapExtention("kra", "png", before))
		#after = "a:" + ",".join(swapExtention("kra", "png", after))
		#before = swapExtention("kra", "png", before)
		#after = swapExtention("kra", "png", after)

		os.chdir("../scribus")
		for sla in glob.glob("*.sla"):
			file = open(sla, "r")
			xml = file.read()
			file.close()

			xml = swapXml(xml, before, "beautiful_")
			os.chdir("../kra")
			xml = swapXml(xml, sorted("beautiful_" + splitext(beautiful)[0] for beautiful in glob.glob("*.kra")),  "")
			os.chdir("../scribus")
			file = open(sla,"w")
			file.write(xml)
			file.close()

# ####################################################################################
if args.g:
	beautify(args.g)
else: beautify(["*.kra"])

