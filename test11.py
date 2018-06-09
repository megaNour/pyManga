#!/usr/bin/python3
import sys
import glob
from os.path import splitext
import os
import manager

manager = manager.Manager("..")
def swapXml(xml, targets, prefix):
	print(targets)
	print(prefix + "777777777777777777777777777777777777777777777777")
	index = 1
	for adress in targets:
		print("replacing: " + splitext(adress)[0] + " by: " + prefix + manager.getPageName(index))
		xml = re.sub("(\D)" + splitext(adress)[0], lambda x:x.group(1) + prefix + manager.getPageName(index),xml)
		index += 1
	return xml
os.chdir("../kra")
before = sorted(glob.glob("*.kra"))
os.chdir("../scribus")
for sla in glob.glob("*.sla"):
			file = open(sla, "r")
			xml = file.read()
			file.close()

			#print(xml)
			xml = swapXml(xml, before, "beautiful_")
			os.chdir("../kra")
			xml = swapXml(xml, sorted("beautiful_" + splitext(beautiful)[0] for beautiful in glob.glob("*.kra")),  "")
			#print(xml)
			os.chdir("../scribus")
			file = open("new"+sla,"w")
			file.write(xml)
			file.close()
