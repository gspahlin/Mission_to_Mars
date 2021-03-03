# mission_to_mars

Description: In this challenge I performed various webscraping tasks related to the planet Mars. These were worked out using a Jupyter notebook. 
Once all of the tasks were complete I automated this using a python app. The python app was then called into a flask app which has an html front end. 
clicking the "scrape" button refreshes the data, displays what was scraped (or provides download links), and uploads the data into a dedicated mongo database. 

Files:

Web_scraping_HW.ipynb - The initial scraping tasks

scrape_mars.py - a scripted version of the scraping tasks in callable function form

mars_app.py - the flask app backend for the mars data website

app_screenshot.jpg - a picture of the front end running. 

Folders:

templates - contains index.html, the html document which codes the front end, and a css stlyesheet for bootstrap. 
