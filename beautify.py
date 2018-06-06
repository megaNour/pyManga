#!/usr/bin/env python3
import constants2 as constants
import os
import glob
import re
import shutil
import argparse
from manager import Manager
from pathlib import Path
import sys

manager = Manager("..")

def rename(swapNamePrefix, globExpr):
	#start becomes the index
	start = step = 1
	targets = sorted(glob.glob(globExpr))
	pattern = re.compile(constants.INDEXED_FILENAME_PATTERN)
	for path in (path for path in targets if os.path.isfile(path)):
		matcher = pattern.search(path)
		if matcher:		
			newName = manager.getPageName(start, matcher.group(2))				
			newPath = swapNamePrefix + newName
			shutil.move(path, newPath)
			start += step
		else :
			print(path + " doesn't comply to the patern")
	return targets

def swapExtention(old: str, new: str, items: list):
	return [re.sub("\." + old + "$", "." + new, item) for item in items] 
	
def beautify():
	before = rename(beautifulPrefix, "*.kra")
	rename(beautifulPrefix, "*.kra~")
	rename("", "*.kra")
	rename("", "*.kra~")
	after = glob.glob("*.kra")
#if before != after:
	print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
	print("!!!!!!!!!!!!!!you need beautification!!!!!!!!!!!!!!")
	print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
	#before = "b:" + ",".join(swapExtention("kra", "png", before))
	#after = "a:" + ",".join(swapExtention("kra", "png", after))
	
	before = swapExtention("kra", "png", before)
	after = swapExtention("kra", "png", after)
	'''
	sys.argv.append("-s")
	sys.argv.append("beautifulScribus.py")

	sys.argv.append("-a")
	sys.argv.append(before)
	sys.argv.append(after)

	os.chdir("../scribus")

	import scribus3
	'''	
	os.chdir("../scribus")
	for sla in glob.glob("*.sla"):
		file = open(sla, "r")
		xml = file.read()
		file.close()
		
		index = 0
		for adress in before:
			xml = xml.replace(before[index], after[index])
			index += 1 
		
		file = open(sla,"w")
		file.write(xml)
		file.close()

# ####################################################################################
beautifulPrefix = "beautiful_"
beautify()

