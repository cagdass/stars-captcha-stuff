import numpy as np
import base64
from skimage import io
import requests
import urllib2
import sys
import os
from scipy import misc

def find_min_count(vertical_breaks):
    pair = vertical_breaks[0]
    for i in xrange(1,len(vertical_breaks)):
        if vertical_breaks[i][1] < pair[1]:
            pair = vertical_breaks[i]
    return pair

def to_grayscale(image):
    [height, width] = [len(image), len(image[0])]

    grayscale = np.array([[0] * width] * height)

    for i in xrange(height):
        for j in xrange(width):
            grayscale[i][j] = float(sum(image[i][j]))/float(3)

    return grayscale

def get_captcha(path):
    pwd = os.path.dirname(os.path.realpath(__file__)) + os.sep

    letters = []
    letters_ = []
    with open(pwd + 'letters.dat') as letters_file:
        for i in letters_file:
            letters_.append(i.strip())
            letters.append(io.imread(pwd + 'letters/{}.png'.format(i.strip())))

    # times = 40
    # for curimg in xrange(times):
    cur_captcha = ''

    img = to_grayscale(io.imread(pwd + path))
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
    letter_count = 0
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
            if letter_count < 5:
                vertical_breaks.append([start, count])
                letter_count += 1
            else:
                min_count = find_min_count(vertical_breaks)
                if min_count[1] < count:
                    vertical_breaks.remove(min_count)
                    vertical_breaks.append([start, count])
            count = 0
            start = 0
    cc = 0
    for pair in vertical_breaks:
        cc += 1
        [start, end] = pair
        test_letter = output[:, start - 1:start + end + 1]

        cur_max = ['', 0]
        for i in xrange(len(letters_)):

            cur_letter = letters[i]
            [height1, width1] = [len(cur_letter), len(cur_letter[0])]
            [height2, width2] = [len(test_letter), len(test_letter[0])]

            matches = 0
            for x in xrange(min(height1, height2)):
                for y in xrange(min(width1, width2)):
                    if test_letter[x,y] == 1 and cur_letter[x,y] == 255:
                        matches += 2
                    elif (test_letter[x,y] == 0 and cur_letter[x,y] == 255) or (test_letter[x,y] == 1 and cur_letter[x,y] == 0):
                        matches -= 1

            matches = float(matches)/(height1*width1)

            if matches > cur_max[1]:
                print letters_[i],
                cur_max = [letters_[i], matches]
        cur_captcha += cur_max[0]
    return cur_captcha
