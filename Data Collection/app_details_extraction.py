# Packages that are being used in this snippet 

# !pip install selenium
# !apt-get update # to update ubuntu to correctly run apt install
# !apt install chromium-chromedriver
# !cp /usr/lib/chromium-browser/chromedriver /usr/bin

from selenium import webdriver
import urllib
import lxml
import re
import sys
sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')
from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
import time

chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36")
webD = webdriver.Chrome('chromedriver', chrome_options=chrome_options)

import traceback
from selenium.common.exceptions import NoSuchElementException




def get_links(playstore_links):
    
    all_links_of_apps = []
    for search_link in playstore_links:
        webD.get(search_link)
        time.sleep(1)
        webD.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        webD.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        webD.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        webD.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        webD.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        webD.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        webD.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        webD.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        webD.get_screenshot_as_file("screenshot.png")
        # from IPython.display import Image, display
        # image = Image(filename='screenshot.png')
        # display(image)
        for app in webD.find_elements_by_class_name("Vpfmgd"):
            tag_value = app.find_element_by_tag_name('a')
            link = tag_value.get_property('href')
            all_links_of_apps.append(link)

        return all_links_of_apps

def get_metadata(all_app_links):
    '''
    Now we have all the links available for the keyword. For each link there are quite a lot information. Define a dict with listing the information that you want to extract for the time being the following are the things that I am retrieving
    App name
    providers
    tags
    ads or not
    description
    rating score
    rating count
    installs
    size
    date of update
    content rating permission
    {this list can be modified}

    We manually looked in the google playstore structure of display page and got tags associated
    with all the metadata that we are trying to extract
    '''

    all_details = []
    error_log =[]
    for link in all_links_of_apps:
        xpath_dict = {
            'App_name':'//*[@id="fcxH9b"]/div[4]/c-wiz/div/div[2]/div/div/main/c-wiz[1]/c-wiz[1]/div/div[2]/div/div[1]/c-wiz[1]/h1/span',
            'providers':'//*[@id="fcxH9b"]/div[4]/c-wiz/div/div[2]/div/div/main/c-wiz[1]/c-wiz[1]/div/div[2]/div/div[1]/div[1]/div[1]/div[1]/span[1]/a',
            'tags':'//*[@id="fcxH9b"]/div[4]/c-wiz/div/div[2]/div/div/main/c-wiz[1]/c-wiz[1]/div/div[2]/div/div[1]/div[1]/div[1]/div[1]/span[2]/a',
            'ads_status':'//*[@id="fcxH9b"]/div[4]/c-wiz/div/div[2]/div/div/main/c-wiz[1]/c-wiz[1]/div/div[2]/div/div[1]/div[2]',
            'description':'//*[@id="fcxH9b"]/div[4]/c-wiz/div/div[2]/div/div/main/c-wiz[1]/c-wiz[4]/div/div[1]/div[2]/div[1]/span/div',
            'rating_score':'//*[@id="fcxH9b"]/div[4]/c-wiz/div/div[2]/div/div/main/div/div[1]/c-wiz/div[1]/div[1]',
            'rating_count':'//*[@id="fcxH9b"]/div[4]/c-wiz/div/div[2]/div/div/main/div/div[1]/c-wiz/div[1]/span/span[2]',
            'installs':'//*[@id="fcxH9b"]/div[4]/c-wiz/div/div[2]/div/div/main/c-wiz[3]/div[1]/div[2]/div/div[3]/span/div/span',
            'size':'//*[@id="fcxH9b"]/div[4]/c-wiz/div/div[2]/div/div/main/c-wiz[3]/div[1]/div[2]/div/div[2]/span/div/span',
            'date_of_update':'//*[@id="fcxH9b"]/div[4]/c-wiz/div/div[2]/div/div/main/c-wiz[3]/div[1]/div[2]/div/div[1]/span/div/span',
            'content_rating_permission':'//*[@id="fcxH9b"]/div[4]/c-wiz/div/div[2]/div/div/main/c-wiz[3]/div[1]/div[2]/div/div[6]/span/div/span/div[1]',
            'cost':'//*[@id="fcxH9b"]/div[4]/c-wiz[3]/div/div[2]/div/div/main/c-wiz[3]/div[1]/div[2]/div/div[8]/span/div/span',
        }
        selector_dict = {
            'App_name':'.AHFaub > span:nth-child(1)',
            'providers':'span.T32cc:nth-child(1) > a:nth-child(1)',
            'tags':'span.T32cc:nth-child(2) > a:nth-child(1)',
            'ads_status':'c-wiz.zQTmif:nth-child(6) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > main:nth-child(1) > c-wiz:nth-child(1) > c-wiz:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4)',
            'description':'.DWPxHb > span:nth-child(1) > div:nth-child(1)',
            'rating_score':'.BHMmbe',
            'rating_count':'.EymY4b > span:nth-child(2)',
            'installs':'div.hAyfc:nth-child(3) > span:nth-child(2) > div:nth-child(1) > span:nth-child(1)',
            'size':'div.hAyfc:nth-child(2) > span:nth-child(2) > div:nth-child(1) > span:nth-child(1)',
            'date_of_update':'.IxB2fe > div:nth-child(1) > span:nth-child(2) > div:nth-child(1) > span:nth-child(1)',
            'content_rating_permission':'.KmO8jd',
            'cost':'div.hAyfc:nth-child(8) > span:nth-child(2) > div:nth-child(1) > span:nth-child(1)',
        }
        # we can add more keywords to extract more app details
        # details_extracted = {
        #     'id':link,
        #     'search_word':'sports player' # 
        # }
        webD.get(link)

        try:
            if webD.find_element_by_css_selector("div.hAyfc:nth-child(7) > div:nth-child(1)").text == "In-app Products":
                selector_dict['cost'] = 'div.hAyfc:nth-child(7) > span:nth-child(2) > div:nth-child(1) > span:nth-child(1)'
        except:
        pass
        
        for key, xpath in xpath_dict.items():
            try:
                details_extracted[key] = webD.find_element_by_xpath(xpath).text
            except NoSuchElementException: #spelling error making this code not work as expected
                pass
                # details_extracted[key] = ''
                # error_log.append(f"{key} - {link}")
        
        for key, selector in selector_dict.items():
            if key in details_extracted:
                continue
            try:
                details_extracted[key] = webD.find_element_by_css_selector(selector).text
            except NoSuchElementException: #spelling error making this code not work as expected
                details_extracted[key] = ''
                error_log.append(f"{key} - {link}")
        
        all_details.append(details_extracted)

        return all_details

if __name__ == '__main__':

    #given are the playstore link for the apps for the keywords that we generated previously
    #in this project we are using curated 20 keywords for the further search 
    playstore_links=  ['https://play.google.com/store/search?q=golf%20GPS&c=apps','https://play.google.com/store/search?q=sports%20betting&c=apps','https://play.google.com/store/search?q=sports%20betting%20tips&c=apps','https://play.google.com/store/search?q=soccer%20betting&c=apps','https://play.google.com/store/search?q=fitivity&c=apps','https://play.google.com/store/search?q=fitness&c=apps','https://play.google.com/store/search?q=football%20betting%20tips&c=apps','https://play.google.com/store/search?q=soccer%20training&c=apps','https://play.google.com/store/search?q=sports%20leauges&c=apps','https://play.google.com/store/search?q=football%20tips&c=apps','https://play.google.com/store/search?q=NBA%20League%20Pass&c=apps','https://play.google.com/store/search?q=Fitivity%20Premium%20subscription&c=apps','https://play.google.com/store/search?q=Live%20Sports&c=apps','https://play.google.com/store/search?q=sports%20network%20Live&c=apps','https://play.google.com/store/search?q=Pro%20sports%20subscription&c=apps','https://play.google.com/store/search?q=State%20football&c=apps','https://play.google.com/store/search?q=football%20training&c=apps','https://play.google.com/store/search?q=champions%20league&c=apps','https://play.google.com/store/search?q=premier%20league&c=apps','https://play.google.com/store/search?q=sports%20player&c=apps']

    all_app_links = get_links(playstore_links)
    meta_data = get_metadata(all_app_links)
    meta_data.to_csv('save the file')



