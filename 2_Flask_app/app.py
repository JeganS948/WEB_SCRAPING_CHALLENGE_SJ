# Import dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from scrape_mars import scrape_mars_info

# Flask Setup
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/marsdb"
mongo = PyMongo(app)

# Flask Routes
@app.route("/")
def index():
    mars = mongo.db.mars_coll.find_one()
    return render_template("index.html", mars=mars)

# Scrape route to import scrape_mars.py with scrape f"
@app.route("/scrape")
def scrape():
    # Define collection
    mars_record = mongo.db.mars_coll

    # Run scrape f"
    x = scrape_mars_info()

    # Update the MongoDB using update and upsert=TRUE
    mars_record.update({}, x, upsert=True)

    # Redirect back to homepage
    return redirect("/")

# Define Main behaviour
if __name__=="__main__":
    app.run(debug=True)