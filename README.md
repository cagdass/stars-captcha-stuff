# Stars Captcha Stuff

## Before getting started

This project is incomplete, I have to return a session with cookies after sending the correct captcha. However, if you're in a hurry, just fire your browser go to any page in Stars that requires captcha before letting you in, enter the captcha and check your cookies. 

Use the key **PHPSESSID** and its value found to send as cookies in your application and it'll work like a charm.

![alt text](https://i.imgur.com/Sv7FCKW.png "PHPSESSID")

## Getting started

Captcha solver for Bilkent's Stars

**Help needed**: Although the captcha is correctly read, there is probably an issue with sending it as a string. The reasons may be related to the cookies, user-agent or some other dipshit. This part remains unsolved.

## Usage

```
# First, clone the repository.
git clone https://github.com/cagdass/stars-captcha-stuff

# There are a few Python libraries you may need to install,
# can be done while getting errors.

# If you'd like to reproduce the letters, else skip to *$@*:
mkdir images
python save_images.py # Saves 100 captcha images from Stars, this number can be modified.
python get_digits.py # Asks the user to label each character extracted from the image, labeling part can be modified.

# *$@*:
python main.py
```

## Improvements

The letters and digits from the captchas have already been extracted, though some have a noise of a pixel or two. 

However, although each letter and digit has the same height in the **letters** folder, the image width of the letters and digits is not standardized, each varies with regard to the characteristics of the character - the image with **w** is wider than **v**.

* To do: Have a fixed width, add extra pixels to images. If the image width **w** and height **h**, and the fixed width is **W**, add 0 pixels on the left and the right, the sizes of these blocks should be **h** x **w/2** on each side, if **w % 2 != 0**, the right side can have an extra vertical line **h** x **1**.
* When I gave it a quick run, the program correctly classified **82** characters out of **100** characters. However, the success rate was only 55%. Since all 5 characters in the captcha image must be correctly classified in order to get access, this needs to be improved. One idea is to extract multiple instances of characters, say 5 images each character, and run a KNN classifier.
 
