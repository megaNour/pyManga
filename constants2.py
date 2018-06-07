from subprocess import call
import os
import re

INDEXED_FILENAME_PATTERN="_p([\d_-]+)\.(\w+~?)$"
INDEXED_SCROLL_PATTERN="_p(\d+)(-(\d+))?(\.\w*)?$"
patternFile = re.compile(INDEXED_FILENAME_PATTERN)
patternScroll = re.compile(INDEXED_SCROLL_PATTERN)
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
	matcher = patternFile.search(fileName)
	return matcher.group(1), matcher.group(2)

def getTargets(possibleTargets, pointers):
	targets = list(possibleTargets)
	#print(possibleTargets)
	#for scroll in possibleTargets:
	#	print(getFileNameIndexAndExtention(scroll))
	#print(pointers)
	if pointers is not None:
		targets = [scroll for scroll in possibleTargets if getFileNameIndexAndExtention(scroll)[0] in [zfillParamString(str(param), 2) for param in pointers]]
	return targets

def zfillParamString(paramString, zeroes):
	return re.sub(r'\d+', lambda x: x.group(0).zfill(zeroes), paramString)

def getIndexStart(name):
	matcher = patternScroll.search(name)
	return matcher

def removeRange(name):
	return re.split(INDEXED_SCROLL_PATTERN, name)[0]
