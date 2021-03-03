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
    data = mongo.db.mars_data.find_one()
    return render_template('index.html', title = data['news_headline'],  para = data['news_blurb'],
    m_url = data['daily_img'], m_html = data['html_d_table'], cerb_t = data['hemi_pics'][0]['title'], 
    cerb_url = data['hemi_pics'][0]['url'], schi_t = data['hemi_pics'][1]['title'], 
    schi_url = data['hemi_pics'][1]['url'], syr_t = data['hemi_pics'][2]['title'], syr_url = data['hemi_pics'][2]['url'],
    val_t = data['hemi_pics'][3]['title'],  val_url = data['hemi_pics'][3]['url'])

@app.route('/scrape')
def scrapie():
    mars_data = mongo.db.mars_data
    m_data  = scrape_mars.scrape_mars()
    mars_data.update({}, m_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)