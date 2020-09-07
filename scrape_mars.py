#!/usr/bin/env python
# coding: utf-8

from splinter import Browser
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs


# In[ ]:

def scrape():

    #Scrape first news title and news paragraph
    url = 'https://mars.nasa.gov/news'

    response = requests.get(url)
    soup = bs(response.text, 'html.parser')

    news_title = soup.find(class_='content_title').text.strip()
    news_p = soup.find(class_='rollover_description_inner').text.strip()


    # In[ ]:


    #Get URL for featured image
    JPL_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    executable_path = {'executable_path':'c:/bin/chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless = False)

    browser.visit(JPL_url)
    time.sleep(1)

    html = browser.html
    soup = bs(html, 'html.parser')

    relative_image_url = soup.find(class_='button fancybox')["data-fancybox-href"]

    browser.quit()


    # In[ ]:


    #Combine relative url with base url
    featured_image_url = 'https://www.jpl.nasa.gov' + relative_image_url


    # In[ ]:


    #Scrape Mars facts table
    facts_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(facts_url)

    #Save to dataframe
    facts_df = tables[0]

    #Set index
    facts_df.set_index(0, inplace=True)

    #Convert dataframe to HTML
    facts_df.to_html('mars_facts.html')


    # In[ ]:


    #Get hemisphere images
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    base_url = 'https://astrogeology.usgs.gov'

    #Get links to open individual hemisphere pages
    executable_path = {'executable_path':'c:/bin/chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless = False)

    browser.visit(hemi_url)
    time.sleep(1)

    html = browser.html
    soup = bs(html, 'html.parser')

    results = soup.find_all(class_='description')
    link_list = []
    for result in results:
        link = base_url + result.find('a')['href']
        link_list.append(link)
        
    browser.quit()


    # In[ ]:


    #Loop through links to get titles and img urls
    title_list = []
    img_list = []

    for link in link_list:
        executable_path = {'executable_path':'c:/bin/chromedriver.exe'}
        browser = Browser('chrome', **executable_path, headless = False)

        browser.visit(link)
        time.sleep(1)
        
        html = browser.html
        soup = bs(html, 'html.parser')
        
        #Get title
        title = soup.find(class_='title').text.strip()
        #Remove "Enhanced" from title
        title = title.replace('Enhanced','')
        #Remove space at end of title
        title = title.strip()
        title_list.append(title)
        #Get image url
        img = soup.find(class_='downloads')
        img_url = img.find('a')['href']
        img_list.append(img_url)
        
        browser.quit()


    # In[ ]:


    #Convert title list & link list to dictionary
    hemisphere_image_urls = [{'title':title_list[i], 'img_url':img_list[i]} for i in range(len(img_list))]
    hemisphere_image_urls

    #Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    return mars_data
