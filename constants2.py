from subprocess import call
import os
import re

INDEXED_FILENAME_PATTERN="\D_([\d_\-]+)\.(\w+)$"
pattern = re.compile(INDEXED_FILENAME_PATTERN)

def printAndRun(command):
    print(command)
    call(command, shell = True)

def listString(listString, splitter=","):
    return listList(listString.split(splitter))
    
def listList(entries):
    result = []    
    for entry in entries:
        entry = str(entry)
        if "-" in entry:
            low, high = entry.split("-")
            result.extend(range(int(low), int(high) + 1))
        else: result.append(int(entry))
    return sorted(result)

def getFileNameIndexAndExtention(fileName):
    matcher = pattern.search(fileName)
    return matcher.group(1), matcher.group(2)

def getTargets(possibleTargets, pointers):
    targets = list(possibleTargets)
    if pointers is not None: 
        targets = [scroll for scroll in possibleTargets if getFileNameIndexAndExtention(scroll)[0] in [zfillParamString(str(param), 2) for param in pointers]]
    return targets

def zfillParamString(paramString, zeroes):
    re.sub(r'\d+', lambda x: x.group(0).zfill(zeroes), paramString)
