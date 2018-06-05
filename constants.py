from subprocess import run
import os
import re

INDEXED_FILENAME_PATTERN="\D_([\d_\-]+)\.(\w+)$"
pattern = re.compile(INDEXED_FILENAME_PATTERN)

def printAndRun(command: str):
    print(command)
    run(command, shell = True)

def listString(listString: str, splitter:str=",") -> list:
    return listList(listString.split(splitter))
    
def listList(entries: list):
    result = []    
    for entry in entries:
        entry = str(entry)
        if "-" in entry:
            low, high = entry.split("-")
            result.extend(range(int(low), int(high)+1))
        else: result.append(int(entry))
    return sorted(result)

def getFileNameIndexAndExtention(fileName: str) -> (str, str):
    matcher = pattern.search(fileName)
    return matcher.group(1), matcher.group(2)

def getTargets(possibleTargets: list(), pointers: list()) -> list:
    targets = list(possibleTargets)
    if pointers is not None: 
        params = listList(pointers)
        targets = [scroll for scroll in possibleTargets if getFileNameIndexAndExtention(scroll)[0] in [zfillParamString(str(param), 2) for param in params]]
    return targets

def zfillParamString(paramString: str, zeroes: int):
    return re.sub(r'\d+', lambda x: x.group(0).zfill(zeroes), paramString)
