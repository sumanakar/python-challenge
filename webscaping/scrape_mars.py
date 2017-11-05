# Dependencies
from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
import time
import os
import pandas as pd
import numpy as np
import tweepy

def scrape():

    
    # create surf_data dict that we can insert into mongo
    mars_data = {}
    
    #Step1: Information about Mars

    # URL of page to be scraped
    url_mission ="https://mars.nasa.gov/news"
    # Retrieve page with the requests module
    response_mission = requests.get(url_mission)

    # Create BeautifulSoup object; parse with 'lxml'
    soup_mission = BeautifulSoup(response_mission.text, 'lxml')

    # results are returned as an iterable list
    results=soup_mission.find_all('div', class_='slide')

    #declare empty list to contain the result

    title_record=[]
    text_record=[]

    for result in results:
        
        news_title=result.find('div', class_='content_title').text
        news_title=news_title.strip('\n')
        news_text=result.find('div', class_='rollover_description_inner').text
        news_text=news_text.strip('\n')
        title_record.append(news_title)
        text_record.append(news_text)
        
    mars_data["title_mars"]=title_record[0]
    mars_data["text_mars"]=text_record[0]

    #step 2: scrap for the featured image

    browser = Browser('chrome', headless=False)

    # URL of page to be scraped
    url_images="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    browser.visit(url_images)

    # Click the full image button
    full_image = browser.find_link_by_partial_text('FULL IMAGE')

    #Click the more info button
    full_image.click()
    more_info = browser.find_link_by_partial_text('more info').first

    while not more_info.visible:
        time.sleep(5)

    more_info.click()

    #parse the kink for the image
    image_elem = browser.find_by_tag('article').find_by_tag('img')
    content=image_elem.outer_html

    #parse the current html page to get the src of the image

    soup_main_image = BeautifulSoup(content, 'lxml')
    results_image=soup_main_image.find('img',class_="main_image",attrs={'src':True})

    #Image url
    featured_image_url="https://www.jpl.nasa.gov"+results_image['src']

    mars_data["image_url"]=featured_image_url

    # Twitter API Credentials

    #all the values of api keys

    if os.path.isfile("apikey.csv"):
        key_df=pd.read_csv("apikey.csv")
        consumer_key=key_df.loc[0,'consumer_key']
        consumer_secret=key_df.loc[0,'consumer_secret']
        access_token=key_df.loc[0,'access_token']
        access_token_secret=key_df.loc[0,'access_token_secret']

    else:
        consumer_key=input("Enter the consumer_key: ")
        consumer_secret=input("Enter the consumer_secret: ")
        access_token=input("Enter the access_token: ")
        access_token_secret=input("Enter the access_token_secret: ")
        data = [{'consumer_key': consumer_key,'consumer_secret':consumer_secret,'access_token':access_token,'access_token_secret':access_token_secret}]
        df = pd.DataFrame(data)
        df.to_csv('apikey.csv', index=False)
        print("file do not exist,creating..")
        

    # Use Tweepy to Authenticate our access
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

    #Step:3-get tweet mention from timeline for Mars Weather

    weather_tweets = api.user_timeline("@MarsWxReport")

    mars_data["weather"]=weather_tweets[0]['text']


    # Step 4: Mars Facts

    # define the dataframe

    mars_df=pd.DataFrame(columns=["Description","Value"])
    #scrap the website for the Mars fact

    # URL of page to be scraped
    url_fact ="https://space-facts.com/mars/"

    # Retrieve page with the requests module
    response_facts = requests.get(url_fact)

    # Create BeautifulSoup object; parse with 'lxml'
    soup_fact = BeautifulSoup(response_facts.text, 'lxml')

    # results are returned as an iterable list
    table=soup_fact.find('table', id='tablepress-mars')

    tr_tag=table.find_all('tr')

    for item in tr_tag:
    
        col1_value=item.find('td',class_='column-1').text
        col2_value=item.find('td',class_='column-2').text 
        #Entering the values in dataframe
        mars_df = mars_df.append([{"Description":col1_value,
                                "Value":col2_value}],ignore_index=True)

    mars_data["fact"]=mars_df.to_html(index=False,header=False)



    #scrap the website for the Mars Hemisphere

    list=[]
    hemisphere_urls={}
    hemisphere_image_urls=[]

    # URL of page to be scraped

    url_hemis ="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    # Retrieve page with the requests module
    response_hemis = requests.get(url_hemis)

    # Create BeautifulSoup object; parse with 'lxml'
    soup_hemis = BeautifulSoup(response_hemis.text, 'lxml')

    # results are returned as an iterable list
    links=soup_hemis.find_all('a', class_='item product-item',attrs={'href':True})

    for link in links:
        
        list.append("https://astrogeology.usgs.gov"+link['href'])

    for item in list:
        
        # Retrieve page with the requests module
        response_list = requests.get(item)

        # Create BeautifulSoup object; parse with 'lxml'
        soup_list = BeautifulSoup(response_list.text, 'lxml')

        # results are returned as an iterable list
        image_hemis_url=soup_list.find('img', class_='wide-image',attrs={'src':True})
        hemis_url="https://astrogeology.usgs.gov"+image_hemis_url['src']
        title_of_url=soup_list.find('h2', class_='title').text
        hemisphere_urls={"title":title_of_url,"img_url":hemis_url}
        hemisphere_image_urls.append(hemisphere_urls)

    mars_data["hem_image"]=hemisphere_image_urls

    return mars_data
