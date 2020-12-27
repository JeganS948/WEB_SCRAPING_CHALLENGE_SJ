# Import Dependencies
from flask import flask, render_template
from flask_pymongo import flask_pymongo
import scrape_mars

# Flask Setup
app = Flask(__name__)

# PyMongo DB Setup

# Flask Routes
# Root route that will query MongoDB and pass mars data into HTML template -> index.html to display data
@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

# Scrape Route to Import `scrape_mars.py` Script & Call `scrape` Function
@app.route("/scrape")

# Define Main Behavior
if __name__ == '__main__':
    app.run(debug=True)