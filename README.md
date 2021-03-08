# PySS (python screen shots) - command line screenshot utility

Command line utility to get screenshots of a webpage in different viewports. 
Supports full page screenshots and custom JS on page load and scroll.

Tested on `Linux Debian "Buster"` with `pyhton@3.7` installed.

# Basic usage

Get 3 screenshots of html.it with views ports: 320x568 (iPhone 5), 768x1024 (iPad Mini) and 1024x1366 (iPad Pro)

`$ python3 pyss.py -u "http://www.html.it" -s 320x568 768x1024 1024x1366`

Get 1 full page screenshot of html.it

`$ python3 pyss.py -u "http://www.html.it" -s 1024xfull`

# Install

Requirements:

- Python 3.7
- Pip
- Firefox driver

Install Python dependencies:

`python3.7 -m pip install --upgrade pip`
`python3.7 -m pip install selenium`
`python3.7 -m pip install pyvirtualdisplay`
`python3.7 -m pip install Pillow`

Install Firefox driver:

`wget https://github.com/mozilla/geckodriver/releases/download/v0.23.0/geckodriver-v0.23.0-linux64.tar.gz`
`tar -xzf geckodriver-v0.23.0-linux64.tar.gz`
`sudo cp geckodriver /opt/`
`sudo chmod 755 /opt/geckodriver`
`sudo ln -fs /opt/geckodriver /usr/bin/geckodriver`
`sudo ln -fs /opt/geckodriver /usr/local/bin/geckodriver`

# Configuration

Around line `30` of `pyss.py` you can change a few parameters of the program:

- enable_display    = True/False (True: browser opens in background. On macOs must be set on False)
- load_css          = True/False (enable / disable css)
- load_js           = True/False (enable / disable javascript)
- load_images       = True/False (enable / disable images loading)
- timeout           = 5 (seconds for page loading timeout)

# Custom Javascript

Around line `40` of `pyss.py` you can set custom javascript in two separated moments:

- On page load
- On scroll

You can use custom javascript on page load to remove unwanted pop-ups or alerts:

`js_on_load   = "document.getElementById('cookie-notice').setAttribute('style', 'display: none;');"`

You can hide fixed elements on full page screenshots to avoid a repetition in the resulting image:

`js_on_scroll = "document.getElementById('header').setAttribute('style', 'display: none;');"`

You can adjust the custom javascrit code to do the same with tags, classes and any other DOM element on the page.

# Author

antoniogioia.com


