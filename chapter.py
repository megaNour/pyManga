#!/usr/bin/env python3

import os
import sys
import re
import argparse
import shutil
import shutil
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("-t", help="chapter title ?")
parser.add_argument("-n", type=int, help="number of pages ?")

args, unknown = parser.parse_known_args()

#sys.argv.append("caca")
#sys.argv[1] = "coucou"
#print(sys.argv[1])
#print(len(sys.argv))
    
chapNum = 1
chapter = "chapitre_"
p = re.compile("(?<!_)_(\d+)(_.+)?")
for s in os.listdir():
    m = p.search(s)
    if m:
        result = int(m.group(1))
        if not result < chapNum:
            chapNum = result + 1
index = str(chapNum).zfill(3)
chapterName = chapter + index
chapterName = chapterName + "_" + args.t if args.t else chapterName

print("creating " + chapterName)

os.makedirs(chapterName)
os.chdir(chapterName)
os.makedirs("dump")
os.makedirs("kra")
os.makedirs("scenario")
os.makedirs("scribus")
os.makedirs("thumbnails")
os.makedirs("release")

os.chdir("kra")

import populate

os.chdir("../..")

content = open("./generic/scribus/generic.sla").read()
content = re.sub("_c\d+", "_c" + index, content)
content = re.sub("CHAPTER \d+ ", "CHAPTER " + str(chapNum) , content)

writeFile = open("./" + chapterName + "/scribus/" + chapterName + ".sla", "w")
writeFile.write(content)
writeFile.close()

#print(content)
#shutil.copyfile("./generic/scribus/generic.sla", "./" + chapterName + "/scribus/" + chapterName + ".sla")   
