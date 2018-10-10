from flask import Flask, render_template, jsonify, redirect
import pymongo
import scrape_mars
import os
from flask_pymongo import PyMongo

MONGO_URL = os.environ.get('MONGODB_URI')
if not MONGO_URL:
    MONGO_URL = "mongodb://localhost:27017/rest"

app = Flask(__name__)

app.config['MONGO_URI'] = MONGO_URL
# conn = 'mongodb://localhost:27017'
# client = pymongo.MongoClient(conn)
mongo = PyMongo(app)

# db = client.mars_db
# collection = db.mars_facts
@app.route('/scrape')
def scrape():
    mars = scrape_mars.scrape()
    # print("\n\n\n")
    print(mars['featured_image_url'])
    # collection.insert_one(mars)
    mongo.db.mars_facts.insert(mars)
    return redirect("/", code=302)

@app.route("/")
def home():
    # mars = list(db.mars_facts.find())
    mars = list(mongo.db.mars_facts.find())
    print(mars) # mars = []
    # print(mars[0]['featured_image_url'])
    if (len(mars) > 0):
        return render_template("index.html", mars = mars[-1])
    else:
        return render_template("index.html", mars={
            'news_title': '',
            'news_paragraph': '',
            'featured_image_url': '',
            'mars_weather': '',
            'mars_facts_table': '',
            'mars_hemispheres': [
                { 'title': '', 'img_url': '' },
                { 'title': '', 'img_url': '' },
                { 'title': '', 'img_url': '' },
                { 'title': '', 'img_url': '' }
            ]
        })

if __name__ == "__main__":
    app.run(debug=True)
