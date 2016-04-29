#!/usr/bin/python

import os
from PIL import Image
import sys 
from random import randint
import time

# How to use: $ python trim_img.py [srcDir] [dstDir]
# Function: 
#   - Use this script to randomly generate images from given image dataset
#   - Mainly used for creating lots of negative images

WIDTH = 640
HEIGHT = 640
X_BASE = 0
Y_BASE = 100
PIECE = 2 # how many images each street view generates 

def trim_img(img_path, width, height, piece, dstDir):
    try:
        f = Image.open(img_path)
    except:
        print 'ERROR: cannot open: ' + img_path
        return
    else:
        xsize, ysize = f.size
        for i in range(piece):
            xstart = randint(X_BASE, xsize - width)
            ystart = randint(Y_BASE, ysize - height)
            box = (xstart, ystart, xstart + width, ystart + height)
            f.crop(box).save(dstDir + '/' + `int(round(time.time() * 10000))` + '.jpg')

# Set the directory you want to start from
def dir_walk(rootDir, indent, dstDir):
    for dirName, subdirList, fileList in os.walk(rootDir):
        print indent + dirName
        img_num = 0
        for fname in fileList: # file 
            if '.jpg' in fname or '.JPG' in fname:
            	img_num += 1
                trim_img(dirName + '/' + fname, WIDTH, HEIGHT, PIECE, dstDir)
	print 'Image number: ' + `img_num`

if __name__ == '__main__':
    # should go through all imgs here...
    if len(sys.argv) != 3:
        sys.exit('ERROR: wrong argc!')
    if not os.path.exists(sys.argv[1]):
        sys.exit('ERROR: ' + sys.argv[1] + ' was not found!')

    rootDir = sys.argv[1]
    dstDir = sys.argv[2]
    # create dest dir
    if not os.path.exists(dstDir):
        os.makedirs(dstDir)

    dir_walk(sys.argv[1], '', sys.argv[2]) # walk through 
    
    print "done"
