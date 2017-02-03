import numpy as np
import base64
from skimage import io
import requests
import urllib2
import sys
import os
from scipy import misc
import test_image

def read_unicode(text, charset='utf-8'):
    if isinstance(text, basestring):
        if not isinstance(text, unicode):
            text = unicode(obj, charset)
    return text

pwd = os.path.dirname(os.path.realpath(__file__)) + os.sep

url = "https://stars.bilkent.edu.tr/homepage/captcha.php"
r = requests.get(url)

cookie_ = r.headers['Set-Cookie'].split(';')[0].split('=')
cookie = {cookie_[0]: cookie_[1]}
print cookie

stamp = '1005297121'
url2 = 'https://stars.bilkent.edu.tr/homepage/images/captcha.php?rndval={}'.format(stamp)
response = requests.post(url2, cookies=cookie)

uri = (base64.b64encode(response.content))

uri += "=" * ((4 - len(uri) % 4) % 4) #ugh

with open(pwd + "captcha.png", "wb") as fh:
    fh.write(uri.decode('base64'))

captcha = test_image.get_captcha('captcha.png')
post_data = {"user_code": captcha}
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
print captcha
lucky_response = requests.post(url, cookies=cookie, data=post_data, headers=headers)
print lucky_response.text
