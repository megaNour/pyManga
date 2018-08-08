#!/usr/bin/python3
import os
import glob

for f in glob.glob("*~"):
	os.remove(f)
