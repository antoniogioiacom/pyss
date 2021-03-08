# PySS (python screen shots) - command line screenshot utility

# example usage: 
# $ python3 pyss.py - u "https://www.html.it/" -s "1200x600 1380x600 1200xfull"

import io
import argparse
import validators
import time
import random
import string
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from pyvirtualdisplay import Display
from datetime import datetime
from PIL import Image
from urllib.parse import urlparse

# timer

start = datetime.now()

# configuration

enable_display    = True
load_css          = True
load_js           = True
load_images       = True
timeout           = 5
screen_default_width  = 1920
screen_default_height = 1080

# custom javascript

js_on_load   = "" # example: "document.getElementById('cookie-notice').setAttribute('style', 'display: none;');"
js_on_scroll = ""

# functions

# random string
def filename_str(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

# full page
def full_screenshot(driver, save_path):
    save_path = save_path + '.png' if save_path[-4::] != '.png' else save_path
    img_li = []
    offset = 0
    height = driver.execute_script('return Math.max('
                                'document.documentElement.clientHeight, window.innerHeight);')
    max_window_height = driver.execute_script('return Math.max('
                                            'document.body.scrollHeight, '
                                            'document.body.offsetHeight, '
                                            'document.documentElement.clientHeight, '
                                            'document.documentElement.scrollHeight, '
                                            'document.documentElement.offsetHeight);')
    while offset < max_window_height:
        if int(offset) > 100:
            try:
                driver.execute_script(js_on_load)
            except:
                print("> javascript error       :  custom js not executed on scroll")
        driver.execute_script(f'window.scrollTo(0, {offset});')
        img = Image.open(io.BytesIO((driver.get_screenshot_as_png())))
        img_li.append(img)
        offset += height

    box = (0, height - height * (max_window_height / height - max_window_height // height), img_li[-1].size[0], img_li[-1].size[1])
    img_li[-1] = img_li[-1].crop(box)
    img_frame_height = sum([img_frag.size[1] for img_frag in img_li])
    img_frame = Image.new('RGB', (img_li[0].size[0] - 12, img_frame_height))
    offset = 0
    for img_frag in img_li:
        img_frame.paste(img_frag, (0, offset))
        offset += img_frag.size[1]
    img_frame.save(save_path) 

# display (with enable_display = True the browser runs in background)
def set_display():
    if (enable_display == True):
        display = Display(visible=0, size=(int(screen_default_width), int(screen_default_height)))
        display.start()

# handle screenshot
def manage_screenshot(vh, url):
    f = filename_str()
    file_path = './screenshots/' + (urlparse(str(url)).netloc) + '-' + v + '-' + f + '.png'
    if str(vh) == "full":
        full_screenshot(driver, file_path)
        print("> screenshot (full page) @  " + file_path)
    else:
        body = driver.find_element_by_tag_name('body')
        body.screenshot(file_path)
        screenshot = Image.open(file_path)
        screenshot = screenshot.crop((0, 0, int(vw) - 12, int(vhz) - 74))
        screenshot.save(file_path)
        print("> screenshot             @  " + file_path)

# args

parser = argparse.ArgumentParser(description='PySS (python screen shots) - command line screenshot utility')
parser.add_argument('-u', help='target url address', required=True)
parser.add_argument('-s', nargs='+', help='screen view port(s) list', required=True)
args = parser.parse_args()
if not validators.url(args.u):
    print("> url error              :  not valid")
    quit()
print("> start                  : ", start.strftime("%d/%m/%Y %H:%M:%S"))
print("> url                    : ", args.u)
print("> view port(s)           : ", args.s)

# display

set_display()

# browser

options = Options()
options.set_preference("browser.privatebrowsing.autostart", True)
if load_css == False:
    options.set_preference('permissions.default.stylesheet', 2)
if load_js == True:
    options.set_preference('javascript.enabled', True)
else:
    options.set_preference('javascript.enabled', False)
if load_images == False:
    options.set_preference('permissions.default.image', 2)
driver = webdriver.Firefox(options=options)

# init

for v in args.s:

    vs = v.split('x')
    vw = vs[0]
    vh = vs[1]
    vhz = vh
    if(str(vhz)) == "full":
        vhz = 1200
    else:
        vhz = int(vhz) + 74
    driver.set_window_size(int(vw), int(vhz))

    try:
        driver.get(args.u)
    except:
        print("> connection error       :  unable to load the page")
    else:
        print("> page loaded            :  view port " + v)
        try:
            element_present = EC.presence_of_element_located((By.TAG_NAME, 'body'))
            WebDriverWait(driver, timeout).until(element_present)
        except TimeoutException:
            print("> timeout error          :  page not loaded")
        else:
            try:
                driver.execute_script(js_on_load)
            except:
                print("> javascript error       :  custom js not executed on load")
            manage_screenshot(vh, args.u)

driver.quit()

end = datetime.now()
end_date = end.strftime("%d/%m/%Y %H:%M:%S")
print("> end                    : ", end_date)
duration = (end - start).total_seconds()
print("> total time (s)         : ", duration)

# antoniogioia.com