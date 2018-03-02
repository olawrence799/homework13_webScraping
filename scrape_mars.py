
# coding: utf-8

# In[68]:


import pandas as pd
import time
import collections
import pymongo
from splinter import Browser
from bs4 import BeautifulSoup


# In[69]:


def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)


# In[78]:


def scrape():
    browser = init_browser()
    scraped_data = {}
    
    mars_news_url = "https://mars.nasa.gov/news/?page=0&per_page=15&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(mars_news_url)
    
    time.sleep(2)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    news_title = soup.find('div', class_='content_title').get_text()
    news_p = soup.find('div', class_='article_teaser_body').get_text()
    scraped_data['news_title'] = news_title
    scraped_data['news_p'] = news_p
    
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)
    
    time.sleep(2)
    html_jpl = browser.html
    soup_jpl = BeautifulSoup(html_jpl, 'html.parser')
    featured_image_url = "https://www.jpl.nasa.gov" + soup_jpl.find('a', class_='button fancybox')['data-fancybox-href']
    scraped_data['featured_image_url'] = featured_image_url
    
    twitter_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(twitter_url)
    
    time.sleep(2)
    html_twitter = browser.html
    soup_twitter = BeautifulSoup(html_twitter, 'html.parser')
    mars_weather = soup_twitter.find(class_='js-tweet-text-container').find(class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').get_text()
    scraped_data['mars_weather'] = mars_weather
    
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    
    time.sleep(2)
    html_facts = browser.html
    soup_facts = BeautifulSoup(html_facts, 'html.parser')
    facts_table = soup_facts.find(id="tablepress-mars")
    
    #df = pd.read_html(str(facts_table))
    df = pd.read_html(html_facts)[0]
    #df = df[0]
    #facts = pd.Series(df[1].values, index = df[0]).to_dict()
    facts = df.to_html()
    scraped_data['facts'] = facts
    
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    
    time.sleep(2)
    html_hemispheres = browser.html
    soup_hemispheres = BeautifulSoup(html_hemispheres, 'html.parser')
    hemi_links = []
    img_links = soup_hemispheres.select("div.description")
    
    for i in img_links:
        url = "https://astrogeology.usgs.gov" + i.find('a', class_='itemLink')['href']
        hemi_links.append(url)
        
    hemi_images = []
    
    for link in hemi_links:
        titles_imgUrls = {}
        browser.visit(link)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        img_url = "https://astrogeology.usgs.gov" + soup.find(class_='wide-image')['src']
        hemi_title = browser.title.split("|")[0][:-10]
        titles_imgUrls['title'] = hemi_title
        titles_imgUrls['img_url'] = img_url
        #titles_imgUrls = collections.OrderedDict(sorted(titles_imgUrls.items()))
        hemi_images.append(titles_imgUrls)
        
    scraped_data['hemisphere_image_urls'] = hemi_images
    
    return scraped_data


# In[77]:


#scrape()

