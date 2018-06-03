#!/usr/bin/env python3

import os
import glob
from manager import Manager
from pathlib import Path
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("-D", action="store_true", help="do not delete existing files flag")
parser.add_argument("-F", action="store_true", help="spare base pdf flag")

args, unknown = parser.parse_known_args()

print(args.D)
print(args.F)

pages = list(range(5,8))
pages.extend(range(3,1))
pages.append(19)
print(pages)
