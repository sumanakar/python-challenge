from flask import Flask, render_template, url_for, request,session,redirect
from flask.ext.pymongo import PyMongo

app=Flask(__name__)

app.config['MONGO_DBNAME']='heroku_fflrmswx'
app.config['MONGO_URI']='mongodb://sumanakar:donald77@ds241875.mlab.com:41875/heroku_fflrmswx'


mongo=PyMongo(app)

@app.route('/add')
def add():
	user=mongo.db.users
	user.insert({'name':'Sumana Kar'})
	return 'Added User!'

if __name__=='__main__':
	app.run(debug=True)