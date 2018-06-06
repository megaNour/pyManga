#!/usr/bin/python3
import shutil
import glob
for output in glob.glob("*/*"):
	shutil.copy2(output, ".")
