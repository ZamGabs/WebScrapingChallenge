from flask import Flask, render_template,redirect
from flask_pymongo import PyMongo
import scrape_mars

import sys

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:26543/MissionToMars"
mongo = PyMongo(app)


@app.route("/")
def index():
    print("I am on index.html")
  
    mars_data=mongo.db.mars_db.find_one()
 
    return render_template("index.html", data=mars_data)

@app.route("/scrape")
def scrape():     
    print("I am in scrape")
    mars_info=scrape_mars.mars_news_scrape()
    mars_info=scrape_mars.img_scrape()
    mars_info=scrape_mars.mars_weather()
    mars_info=scrape_mars.mars_facts()
    mars_info=scrape_mars.mars_hem()
    mongo.db.mars_db.update({},mars_info,upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)