#automated scraping script 
#import dependencies

from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import requests
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo



def scrape_mars():
    #setup browser
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    #get title information from the first site
    url = "https://mars.nasa.gov/news/"
    response = requests.get(url)
    
    #create the soup object
    soup = bs(response.text)

    m_titles = soup.find_all('div', class_ = 'content_title')
    #title1 is the variable that contains the desired news headline
    title1 = m_titles[0].text

    #get paragraph information from the first site
    m_para = soup.find_all('div', class_ = 'rollover_description_inner')

    #para1 is the variable that contains the desired blurb
    para1 = m_para[0].text

    #get the image desired from the second page
    url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    browser.visit(url2)

    # Click the first link on the page
    browser.click_link_by_partial_href('images')

    html = browser.html

    ibisque = bs(html, 'html.parser')

    #return all the img tags and store in a variable
    img_url = ibisque.find_all("img")

    #url1 is the url for the desired image
    url1 = img_url[2]['src']

    #get tables from site number 3
    table_url = 'https://space-facts.com/mars/'

    mt_tables = pd.read_html(table_url)

    #save the desired table to mars_df
    mars_df = mt_tables[0]

    #write the table out to html, while getting rid of line break characters
    mars_html_t = mars_df.to_html(index = False)
    mars_html_t = mars_html_t.replace('\n', '')

    #get the martian hemisphere picture urls
    pics_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    p_urls = ['Cerberus', 'Schiaparelli', 'Syrtis', 'Valles']

    pic_urls = []

    pic_titles = []

    for p in p_urls:
        #visit the website with the pictures
        browser.visit(pics_url)
    
        # Click the first link on the page
        browser.click_link_by_partial_text(p)
    
        #Use the html in the open browser
        html3 = browser.html
    
        #create a beautiful soup object
        chilli = bs(html3, 'html.parser')
    
        #find the image url by searching for <a> tags
        im_a = chilli.find_all('a')
    
        #append the image url into the correct list
        pic_urls.append(im_a[5]['href'])
    
        #find the image title
        im_title = chilli.find('h2', class_ = 'title').text
    
        #append the title to the correct list
        pic_titles.append(im_title)
    
    #package results in a list of dictionaries 
    # pics list is the output list for the function   
    pics_list = []

    for q in range(3):
        u_dict = {}
        u_dict['title'] = pic_titles[q]
        u_dict['url'] = pic_urls[q]
        pics_list.append(u_dict)
    #close browser
    browser.quit()
    #store data in a dict
    mars_data = {
    'news_headline': title1,
    'news_blurb': para1,
    'daily_img': url1,
    'html_d_table': mars_html_t,
    'hemi_pics': pics_list   
    }
    return(mars_data)
    







