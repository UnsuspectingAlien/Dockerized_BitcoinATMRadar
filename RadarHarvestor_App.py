import os
import sys
import time
import subprocess
from datetime import datetime
from flask import Flask,render_template,request
from urlScraper import harvestCityLinks, harvestATMLinks, removeDups, printHello
from dataCollector import collect, seleniumCollect
from detailExtractor import getDetails, buildCSV, aggregateCSV

app = Flask(__name__)
#app.config['MONGODB_DB'] = 'flask'
#app.config['SECRET_KEY'] = 'dev'

#from FlaskPersistence_models import db, Users
#from Forms import LoginForm
#db.init_app(app)

@app.route('/', methods=['GET', 'POST'])                  # at the end point /
def index():                      # call method hello
    #form = LoginForm(request.form)
	if request.method == "GET":
		return render_template('index.html')
	if request.method == "POST":
		printHello()
		return render_template('post.html')

@app.route('/scrape', methods=['POST'])
def scrape():
	if request.method == "POST":
        	param = printHello()
        	return render_template('post.html', param=param)

