from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Set route
@app.route('/')
def index():
    # Show Entire Collection
    mars_stuff_display = mongo.db.mars_stuff.find_one()
    print(mars_stuff_display)
    return render_template("index.html", mars_stuff_display=mars_stuff_display)

@app.route("/scrape")
def scraper():
    mars_stuff_collection = mongo.db.mars_stuff
    results_dict = scrape.scrape()
    mars_stuff_collection.update({}, results_dict, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
