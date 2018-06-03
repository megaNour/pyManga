#!/usr/bin/python3
from os.path import basename
import os
for dirName in os.listdir("."): print(dirName)

test = "chocolat"

def chocoMethod():
    print(test)

test2 = "chocolata.pdf"
print(basename(test2).split(".")[0])
chocoMethod()
