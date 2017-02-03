import numpy as np
import base64
from skimage import io
import requests
import urllib2
import sys
import os
from scipy import misc


def to_grayscale(image):
    [height, width] = [len(image), len(image[0])]

    grayscale = np.array([[0] * width] * height)

    for i in xrange(height):
        for j in xrange(width):
            grayscale[i][j] = float(sum(image[i][j]))/float(3)

    return grayscale

cmd = os.environ.get('SCIPY_PIL_IMAGE_VIEWER', 'see')

# Get the working directory.
pwd = os.path.dirname(os.path.realpath(__file__)) + os.sep

letters = []
times = 100

for curimg in xrange(times):
    img = to_grayscale(io.imread(pwd + 'images/img{}.png'.format(curimg)))
    [height, width] = [len(img), len(img[0])]

    # Apply thresholding.
    output = np.array([[0] * width] * height)
    for i in xrange(height):
        for j in xrange(width):
            cur = img[i][j]
            # Leave only the pixels whose value is less than 130.
            if (cur < 130):
                output[i][j] = 1
            else:
                output[i][j] = 0

    vertical_breaks = []
    sums = map(lambda x: 1 if x==0 else 0, np.sum(output, axis=0))

    mode_ = False
    start = 0
    count = 0
    for i in xrange(len(sums)):
        cur = sums[i]
        if cur == 1 and not mode_:
            continue
        elif cur == 0 and not mode_:
            mode_ = True
            start = i
        elif cur == 0 and mode_:
            count += 1
        else:
            mode_= False
            vertical_breaks.append([start, count])
            count = 0
            start = 0
    vertical_breaks = sorted(vertical_breaks, key=lambda x: x[1], reverse=True)
    misc.toimage(output).show()
    for i in xrange(5):
        [start, end] = vertical_breaks[i]
        letter = output[:, start-1:start + end + 1]
        [height, width] = [len(letter), len(letter[0])]

        misc.toimage(letter).show()
        cur_letter = raw_input('Current letter: ')
        if cur_letter in letters:
            continue
        else:
            letters.append(cur_letter)
            misc.imsave(pwd + 'letters/{}.png'.format(cur_letter), letter)

        if len(letters) == 28:
            sys.exit()
