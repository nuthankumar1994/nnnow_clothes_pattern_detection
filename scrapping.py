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
import pandas as pd
import numpy as np
import csv



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
    dress_desc_list = []
    img_path_list = []
    pattern_list = []
    # try:
    #     df = pd.read_csv("data_dresses.csv", index_col=None)
    # except Exception as e:
    #     print("exception in reading csv ",e)
    #     df = pd.DataFrame(columns=('img_path', 'dress_description', 'img_link', ''), index=None)
    #     df.to_csv("data_dresses.csv",header=True)

    while True:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(15)
        img_results = driver.find_elements(
        by=By.XPATH,
        value="//img[contains(@class,'nwc-lazyimg is-loaded')]"
        )

        for img_result in img_results:
            src = img_result.get_attribute('src')
            dress_description = img_result.get_attribute('alt')
            if 'https://' in src:
                #print(src)
                link_list.append(src)
            else:
                print('Base 64 in source.')
            if dress_description not in [None,""]:
                dress_desc_list.append(dress_description)
            new_height = driver.execute_script('return document.body.scrollHeight')
        
        print("length of link list is " + str(len(link_list)))
        if new_height == privious_height:
            break
        privious_height = new_height
    print("length of img_results is " + str(len(img_results)))

    # print(link_list)
    i=1
    for link in link_list:
        file_name=str(pattern) + str(i)
        img_path = f"{pattern}/{file_name}" + ".jpg"
        img_path_list.append(img_path)
        pattern_list.append(pattern)
        try:    
            img_file=open('./content/' + pattern +'/' + file_name +'.jpg','wb')
        except:
            os.makedirs('./content/'+ pattern)
            img_file=open('./content/' + pattern +'/' + file_name +'.jpg','wb')
        img_file.write(urllib.request.urlopen(link).read())
        img_file.close()
        i+=1

    dump_dict = {'img_path': img_path_list, 'pattern': pattern_list, 'dress_description': dress_desc_list, 'image_link': link_list}
    df2 = pd.DataFrame(dump_dict)
    print(df2.head(10))
    
    df2.to_csv('data_dresses.csv', mode='a', header=False
               , index=False)



if __name__ == "__main__":
    patterns = ['Striped', 'Embroidered', 'Textured', 'Patterned%20weave', 'Checked', 'Heathered', 'Lace', 'Embellished','Appliqued', 'Dyed', 'Washed','Patterned%20knit', 'Colour%20blocked']
    for pattern in patterns:
        downloader(pattern)

