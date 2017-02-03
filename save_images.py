import base64
import requests
import urllib2
import sys

# url = "https://stars.bilkent.edu.tr/homepage/captcha.php"
# r = requests.get(url)
# # print r.text
# cookie_ = r.headers['Set-Cookie'].split(';')[0].split('=')
# # cookie = {cookie_[0]: cookie_[1]}
# c = 'erh8mir0g5n4dqgusr9ku71u00'
# cookie = {cookie_[0]: c}
# print cookie

times = 100

stamp = '1005297121'
url2 = 'https://stars.bilkent.edu.tr/homepage/images/captcha.php?rndval={}'.format(stamp)

for i in xrange(times):
    response = requests.post(url2)
    uri = (base64.b64encode(response.content))

    uri += "=" * ((4 - len(uri) % 4) % 4) #ugh

    with open("images/img{}.png".format(i), "wb") as fh:
        fh.write(uri.decode('base64'))
