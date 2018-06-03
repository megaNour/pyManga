#!/usr/bin/env python3

import os
import glob
from manager import Manager
from pathlib import Path
import argparse
import sys

parser = argparse.ArgumentParser()
args, unknown = parser.parse_known_args()

args.D = True
args.F = False
sys.argv.append("-D")
sys.argv.append("True")
import test 
