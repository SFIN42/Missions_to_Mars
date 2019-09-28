#!/usr/bin/env python
# coding: utf-8

# Dependencies
from bs4 import BeautifulSoup as bs
import requests
import shutil
import pandas as pd
import time
##### Import Splinter and set the chromedriver path
import splinter
from splinter import Browser

def init_browser():
    ##### Path to Chromedriver if needed "D:\GATechDA\web-scraping-challenge\Missions_to_Mars"
    executable_path = {"executable_path": "D:\GATechDA\web-scraping-challenge\Missions_to_Mars\chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_data = {}

    ##### url to nasa news
    url = 'https://mars.nasa.gov/news/'

    ##### Retrieve page with the requests module
    response = requests.get(url, headers={'Cache-Control': 'no-cache'})

    ##### Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(response.text, 'html.parser')

    ##### Examine the results, then determine element that contains sought info
    # print(soup.prettify())

    ##### Scrape the [NASA Mars News Site](https://mars.nasa.gov/news/) and collect the latest News Title and Paragraph Text.
    ##### Assign the text to variables that you can reference later.
    nasa_title = soup.find_all('div',class_="content_title")[0].text
    nasa_article = soup.find_all('div',class_="rollover_description_inner")[0].text

    ##### Removing New Line tags
    nasa_title = nasa_title.replace('\n', '')
    nasa_article = nasa_article.replace('\n', '')
    
    ##### Printing the Title & Article
    # print(nasa_title)
    # print(nasa_article)

    ##### JPL Mars Space Images - Featured Image

    ##### Path to Chromedriver if needed "D:\GATechDA\web-scraping-challenge\Missions_to_Mars"
    ##### I believe I no longer need this here since I called the browser in the code above.
    # executable_path = {"executable_path": "D:\GATechDA\web-scraping-challenge\Missions_to_Mars\chromedriver"}
    # browser = Browser("chrome", **executable_path, headless=False)

    ##### Pause for 3 seconds to allow web page to load
    pause_time = 3

    ##### wait to load page
    time.sleep(pause_time)

    ##### Pull the href; url for the most current image ; Visit the following URL
    ##### jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)

    ##### Clicks the "FULL IMAGE" button to go to the next page
    browser.click_link_by_partial_text('FULL IMAGE')

    ##### wait to load page
    time.sleep(pause_time)

    ##### Clicks the "more info" button to go to the next page
    browser.click_link_by_partial_text('more info')

    ##### wait to load page
    time.sleep(pause_time)

    ##### Design an XPATH selector to grab the current space image
    xpath = '//*[@id="page"]/section[1]/div/article/figure/a/img'

    ##### Use splinter to Click the Current Mars image to bring up the full resolution image
    results = browser.find_by_xpath(xpath)
    img = results[0]
    img.click()

    ##### wait to load page
    time.sleep(pause_time)

    ##### Scrape the browser into soup and use soup to find the full resolution space image
    ##### Save the image url to a variable called `featured_image_url`
    html = browser.html
    soup = bs(html, 'html.parser')
    featured_image_url = soup.find("img",)["src"]
    # print(featured_image_url)

    ##### wait to load page
    time.sleep(pause_time)

    ##### Use the requests library to download and save the image from the `img_url` above
    featured_image = requests.get(featured_image_url, stream=True)
    with open('img.png', 'wb') as out_file:
        shutil.copyfileobj(featured_image.raw, out_file)

    ##### Display the image with IPython.display
    from IPython.display import Image
    Image(url='img.png')

    ##### Mars Weather
    ##### Twitter address https://twitter.com/marswxreport?lang=en
    tw_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(tw_url)

    ##### Scrape the browser into soup
    ##### Retrieve page with the requests module
    response = requests.get(tw_url)

    ##### Create BeautifulSoup object; parse with 'html.parser'
    soup_mwr = bs(response.text, 'html.parser')

    ##### wait to load page
    time.sleep(pause_time)

    ##### Examine the results, then determine element that contains sought info
    # print(soup_mwr.prettify())

    ##### TEST to Pull one Tweet
    ##### test = soup.find('div', class_= "js-tweet-text-container").\
    ##### Xpath - //*[@id="stream-item-tweet-1174321649539330049"]/div[1]/div[2]/div[2]/p/text()
    # test = soup_mwr.find('div', class_="js-tweet-text-container").\
    #     find('p',class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    # print(test)

    ##### Pull Tweet Text
    ##### Examine the results, then determine element that contains sought info results are returned as an iterable list;
    ##### I used "results" to get a count of the tweets for my loop
    results = soup_mwr.find_all('div', class_="js-tweet-text-container")

    # count = 0

    ##### Create a list for the Mars Weather Report Tweets (mwr)
    mars_weather = []

    ##### Loop through returned results
    for result in results:
        
        ##### Retrieve the tweets
        mars_weather.append(result.find('p',class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text)         
        #     count = 1 + count
            
        # print(mars_weather)
        # print(count)

    ### Mars Facts 
    ##### https://space-facts.com/mars/
    sp_url = "https://space-facts.com/mars/"

    ##### Use pandas html read to read the table into pandas
    tables = pd.read_html(sp_url)
    # tables

    ##### wait to load page
    time.sleep(pause_time)

    ##### Convert Table to a Pandas DF
    marsdf = tables[0]
    marsdf.columns = ['Mars - Earth Comparison', 'Mars', 'Earth']
    # marsdf.head()

    ##### Convert Pandas DF to HTML table
    mars_html_table = marsdf.to_html()
    # mars_html_table

    ##### Remove new line characters
    mars_html_table = mars_html_table.replace('\n', '')

    ##### Mars Hemispheres ; setting up the list of dictionaries for title & img_url
    hemisphere_image_urls = []

    ##### This is the landing page. Do this same process 4 times
    ##### https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars
    mh_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(mh_url)

    ##### wait to load page
    time.sleep(pause_time)

    ##### Clicks the "Cerberus Hemisphere Enhanced" link to go to the next page
    browser.click_link_by_partial_text('Cerberus Hemisphere Enhanced')

    ##### wait to load page
    time.sleep(pause_time)

    ##### Obtains the html of the page
    response = browser.html

    ##### Create BeautifulSoup object; parse with 'html.parser'
    soup_cerb = bs(response, 'html.parser')

    ##### Don't need to print this once I have the soup. Leaving for debugging
    # print(soup_cerb.prettify())

    ##### Cerberus Hemisphere url
    image_url = soup_cerb.find('div', class_="downloads").find('ul',).find('li',).find('a',)['href']
    # image_url

    ##### Cerberus Hemisphere title
    title = soup_cerb.find('h2', class_="title").text[:-9]
    # title

    ##### Add title & url to list
    hemisphere_image_urls.append({"title": title, "image_url": image_url})

    ##### Goes back to Mars Hemispheres to select the next Hemisphere
    ##### https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars
    mh_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(mh_url)

    ##### wait to load page
    time.sleep(pause_time)

    ##### Clicks the "Schiaparelli Hemisphere Enhanced" link to go to the next page
    browser.click_link_by_partial_text('Schiaparelli Hemisphere Enhanced')

    ##### Obtains the html of the page
    response = browser.html

    ##### Create BeautifulSoup object; parse with 'html.parser'
    soup_schi = bs(response, 'html.parser')

    ##### Don't need to print this once I have the soup. Leaving for debugging
    # print(soup_schi.prettify())

    ##### Schiaparelli Hemisphere url
    schi_image_url = soup_schi.find('div', class_="downloads").find('ul',).find('li',).find('a',)['href']
    # schi_image_url

    ##### Schiaparelli Hemisphere title
    title = soup_schi.find('h2', class_="title").text[:-9]
    # title

    ##### Add title & url to list
    hemisphere_image_urls.append({"title": title, "image_url": image_url})

    ##### Goes back to Mars Hemispheres to select the next Hemisphere
    ##### https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars
    mh_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(mh_url)

    ##### wait to load page
    time.sleep(pause_time)

    ##### Clicks the "Syrtis Major Hemisphere Enhanced" link to go to the next page
    browser.click_link_by_partial_text('Syrtis Major Hemisphere Enhanced')

    ##### wait to load page
    time.sleep(pause_time)

    ##### Obtains the html of the page
    response = browser.html

    ##### Create BeautifulSoup object; parse with 'html.parser'
    soup_syrt = bs(response, 'html.parser')

    ##### Don't need to print this once I have the soup. Leaving for debugging
    # print(soup_syrt.prettify())

    ##### Syrtis Major Hemisphere url
    image_url = soup_syrt.find('div', class_="downloads").find('ul',).find('li',).find('a',)['href']
    # image_url

    ##### Syrtis Major Hemisphere title
    title = soup_syrt.find('h2', class_="title").text[:-9]
    # title

    ##### Add title & url to list
    hemisphere_image_urls.append({"title": title, "image_url": image_url})

    ##### Goes back to Mars Hemispheres to select the next Hemisphere
    ##### https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars
    mh_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(mh_url)

    ##### wait to load page
    time.sleep(pause_time)

    ##### Clicks the "Valles Marineris Hemisphere Enhanced" link to go to the next page
    browser.click_link_by_partial_text('Valles Marineris Hemisphere Enhanced')

    ##### wait to load page
    time.sleep(pause_time)

    # Obtains the html of the page
    response = browser.html

    # Create BeautifulSoup object; parse with 'html.parser'
    soup_vall = bs(response, 'html.parser')

    ##### Don't need to print this once I have the soup. Leaving for debugging
    # print(soup_vall.prettify())

    ##### Valles Marineris Hemisphere url
    image_url = soup_vall.find('div', class_="downloads").find('ul',).find('li',).find('a',)['href']
    # image_url

    ##### Valles Marineris Hemisphere title
    title = soup_vall.find('h2', class_="title").text[:-9]
    # title

    ##### Add title & url to list
    hemisphere_image_urls.append({"title": title, "image_url": image_url})

    ##### Print to see if title & url are added to the list of dictionaries
    # hemisphere_image_urls

    ##### These are the locations where information was stored

    
    
    ##### latest News Title and Paragraph Text.
    mars_data["title"] = nasa_title
    mars_data["article"] = nasa_article

    ##### Variable for feature image
    mars_data["featured_image_url"] = featured_image_url

    ##### Variable for Tweets
    mars_data["tweets"] = mars_weather[0]

    ##### Variable for Table
    mars_data["table"] = mars_html_table

    ##### Variable for Hemisphere Image & urls
    mars_data["hemispheret0"] = hemisphere_image_urls[0]['title']
    mars_data["hemisphere0"] = hemisphere_image_urls[0]['image_url']

    ##### Variable for Hemisphere Image & urls
    mars_data["hemispheret1"] = hemisphere_image_urls[1]['title']
    mars_data["hemisphere1"] = hemisphere_image_urls[1]['image_url']

    ##### Variable for Hemisphere Image & urls
    mars_data["hemispheret2"] = hemisphere_image_urls[2]['title']
    mars_data["hemisphere2"] = hemisphere_image_urls[2]['image_url']

    ##### Variable for Hemisphere Image & urls
    mars_data["hemispheret3"] = hemisphere_image_urls[3]['title']
    mars_data["hemisphere3"] = hemisphere_image_urls[3]['image_url']

    ##### Dictionary with Hemisphere Image & urls (Separated out above)
    mars_data["hemisphere_image_urls"] = hemisphere_image_urls

    ##### Close the browser after scraping
    browser.quit()

    ##### return one Python dictionary containing all of the scraped data.
    return mars_data