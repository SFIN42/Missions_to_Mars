from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

##### Flask app
app = Flask(__name__)

##### Use flask_pymongo to set up mongo connection ; "mongodb://127.0.0.1:27017/scrape_mars"
app.config["MONGO_URI"] = "mongodb://localhost:27017/scrape_mars"
mongo = PyMongo(app)

@app.route("/")
def index():
    # Find one record of data from the mongo database
    back_end_mars_data = mongo.db.mars_data.find_one()
    # Return template and data
    return render_template("index.html", mars_data=back_end_mars_data)    

@app.route("/scrape")
def scraper():
    mars_data_collection = mongo.db.mars_data
    # Run the scrape function
    new_mars_data = scrape_mars.scrape()
    # Update the Mongo database using update and upsert=True
    mars_data_collection.update({}, new_mars_data, upsert=True)
    # Redirect back to home page
    return redirect("/", code=302)

# @app.route("/hemisphere")
# def hemisphere():
#     # Find one record of data from the mongo database
#     mars_data.hemisphere_image_urls = mars_data.hemisphere_image_urls
#     # Return template and data
#     return render_template("index.html", mars_data=back_end_mars_data)

if __name__ == "__main__":
    app.run(debug=True)

##### mars_data is where the dictionary of data is stored in scrape_mars.py
