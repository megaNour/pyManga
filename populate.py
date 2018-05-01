import re
import argparse
import shutil
from pathlib import Path
parser = argparse.ArgumentParser()
parser.add_argument("-n", type=int, help="number of items ?")
args, unknown = parser.parse_known_args()

def getChapterNumber(chapterName):
    p = re.compile("(?<!_)_(\d+)(_.+)?")
    m = p.search(chapterName)
    return m.group(1).zfill(3)

if not args.n:
    args.n = 14

extention = Path.cwd().name
seriesName = Path.cwd().parent.parent.parent.name
chapNum = getChapterNumber(Path.cwd().parent.name)

for i in range(1, args.n + 1):
    genericPath = Path(Path.cwd().absolute() / ".." / ".." / "generic" / extention / ("generic." + extention)).resolve()
    shutil.copyfile(genericPath, seriesName + "_c" + chapNum + "_p" + str(i).zfill(2) + "." + extention)


