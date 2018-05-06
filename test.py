import os
import glob
from manager import Manager
manager = Manager("..")

f = glob.glob("./*.pdf")
os.remove(f[0])

