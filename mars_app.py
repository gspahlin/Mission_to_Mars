from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import requests
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

#set up mongodb connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route('/')
def index():
    mars_data = mars_data.mongo.db.find_one()
    return render_template('index.html', title = mars_data['news_headline'],  para = mars_data['news_blurb'],
    m_url = mars_data['daily_img'], m_html = mars_data['html_d_table'], cerb_t = mars_data['hemi_pics'][0]['title'], 
    cerb_url = mars_data['hemi_pics'][0]['url'], schi_t = mars_data['hemi_pics'][1]['title'], 
    schi_url = mars_data['hemi_pics'][1]['url'], syr_t = mars_data['hemi_pics'][2]['title'], syr_url = mars_data['hemi_pics'][2]['url'],
    val_t = mars_data['hemi_pics'][3]['title'],  val_url = mars_data['hemi_pics'][3]['url'])

@app.route('/scrape')
def scrapie():
    mars_data  = scrape_mars.scrape_mars()
    mars_data.update({}, mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)