#!/usr/bin/python3
import sys
import glob
from os.path import splitext
import os
import manager
import re
import shutil

pattern = re.compile("chapitre_(\d+)$")
for folder in os.listdir():
	m = pattern.search(folder)
	if m:
		if len(m.group(1)) < 3:
			shutil.move(folder, "chapitre_" + m.group(1).zfill(3))
