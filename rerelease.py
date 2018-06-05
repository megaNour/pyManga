#!/usr/bin/python3
import glob
import zipfile
import os
import time
import sys
import re
import argparse
from os.path import basename, splitext
import shutil

start = time.time()

parser = argparse.ArgumentParser()
parser.add_argument("-P", action="store_true", help="flag for not producing pages. Usefull to just run the scribus part")
parser.add_argument("-p", nargs="*", help="pages to be released >>> FROM ALL SCRIBUS SCROLLS <<<, accept x, y, x-z...")
parser.add_argument("-D", action="store_true", help="spare base pdf flag")
parser.add_argument("-F", action="store_true", help="flush release folder from old cache")


args, unknown = parser.parse_known_args()
#for Webtoonify

#if args.p:
#    sys.argv.extend(args.p)

if not args.P:
    flag = -1
    i = 1
    for arg in sys.argv[i:len(sys.argv)]:
        if sys.argv[i].startswith("-"): 
            flag = i
            print("flag at " + str(i))
            del sys.argv[flag:]
            break
        i += 1
    os.chdir("kra")
    import produce
    os.chdir("..")

os.chdir("scribus")
print("9999999999999999999999999")
print(os.getcwd())
if not args.D:
    for pdf in glob.glob("*.pdf"): os.remove(pdf)
import scribus2
import webtoonify2
           
print("time taken: {:.2f}s {}".format((time.time() - start), os.path.basename(__file__)))


