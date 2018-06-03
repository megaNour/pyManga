#!/usr/bin/env python3
import constants
import os
import argparse
import sys
import glob


parser = argparse.ArgumentParser()
parser.add_argument("-D", action="store_true", help="do not delete pdf files flag")

args, unknown = parser.parse_known_args()



for entry in glob.glob("*.py"):
    print(entry)
    print(type(entry))

"""
entries = ["1", "2", "3", "5-8", "12", "10"]
print(constants.listList(entries))
print(constants.listString("1,2,3,5-8,12,10"))
"""
"""
import test

os.chdir("scribus")

import webtoonify
"""
