from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import time
import json

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import shutil
import wget
import urllib.request
from urllib.request import urlopen
import os




def downloader(pattern=None):
    driver = webdriver.Chrome('/Users/nuthankumar/Data/chromedriver_mac_arm64/chromedriver')
    base_url = 'https://www.nnnow.com/women-tops-tshirts?p=1'
    pattern_url = f'&f-pa={pattern}'
    if pattern==None:
        url = base_url
    else:
        url = base_url+pattern_url
    driver.get(url)
    time.sleep(3)
    privious_height = driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

    link_list = []

    while True:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(15)
        img_results = driver.find_elements(
        by=By.XPATH,
        value="//img[contains(@class,'nwc-lazyimg is-loaded')]"
        )
        
        for img_result in img_results:
            src = img_result.get_attribute('src')
            if 'https://' in src:
                #print(src)
                link_list.append(src)
            else:
                print('Base 64 in source.')
            new_height = driver.execute_script('return document.body.scrollHeight')
        
        print(len(link_list))
        if new_height == privious_height:
            break
        privious_height = new_height
    print(len(img_results))
    # print(link_list)
    i=1
    for link in link_list:
        file_name=str(pattern) + str(i)
        img_file=open(file_name +'.jpg','wb')
        img_file.write(urllib.request.urlopen(link).read())
        img_file.close()
        i+=1


if __name__ == "__main__":
    patterns = ['Printed', 'Solid', 'Striped', 'Embroidered', 'Textured', 'Patterned%20weave', 'Checked', 'Heathered', 'Lace', 'Embellished']
    for pattern in patterns:
        downloader(patterns)

