from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
from flask import url_for, request,session
from flask.ext.pymongo import PyMongo
import scrape_mars


app = Flask(__name__)

app.config['MONGO_DBNAME']='heroku_fflrmswx'
app.config['MONGO_URI']='mongodb://sumanakar:donald77@ds241875.mlab.com:41875/heroku_fflrmswx'

mongo = PyMongo(app)

@app.route('/')
def index():
    mars_data = mongo.db.mars_records.find_one()

    return render_template('index.html', mars_data=mars_data)


@app.route('/scrape')
def scrape():
    mars_records = mongo.db.mars_records
    data = scrape_mars.scrape()
    mars_records.update(
        {},
        data,
        upsert=True,
    )
    new_data= mongo.db.mars_records.find_one()

    return render_template('index.html', mars_data=new_data)


if __name__ == "__main__":

    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug = True, port = 5000)