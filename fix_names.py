import path
import os
import sys
from pathlib import Path
import glob
png_files = glob.glob('./*.png')
for png_file in png_files:
    new_png_file = png_file.replace("_", "-")
    if png_file != new_png_file:
        print(png_file, '->', new_png_file)
        os.rename(png_file, new_png_file)
