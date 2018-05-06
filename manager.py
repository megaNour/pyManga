import re
import os
from pathlib import Path
class Manager:
    """a class to infer useful info:
        seriesName: the name of the series
        chapNum: the number of the chapter with leading zeroes
        chapTitle: the title of the chapter"""
    def getChapterNumber(self, chapterName):
        p = re.compile("(?<!_)_(\d+)(_(.+))?")
        m = p.search(chapterName)
        return m.group(1).zfill(3), m.group(3)
    
    def __init__(self, chapDir="."):
        previousDir = Path.cwd()
        os.chdir(chapDir)
        self.seriesName = Path.cwd().parent.parent.name
        self.chapNum, self.chapTitle = self.getChapterNumber(Path.cwd().name)
        os.chdir(previousDir)

    def getPageName(self, pageNum, extention):
        pageNum = str(pageNum).zfill(2)
        return self.seriesName + "_c" + self.chapNum + "_p" + pageNum + "." + extention

