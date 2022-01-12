<<<<<<< Updated upstream
from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

=======
import os
import pandas as pd
import json
import csv
import pymongo
from pymongo import MongoClient 

from flask import Flask, redirect, url_for, render_template, jsonify

app = Flask(__name__)

db_path = "mongodb://localhost:27017/"
mongo = MongoClient(db_path)
db = mongo.evDB

# API Routes
@app.route("/api/energy")
def energy():
    energy = db.energy.find()
    energy = pd.DataFrame(list(energy))
    # cleaning with for loop here
    energy = energy.drop(columns='_id').T.to_dict()
    return jsonify(energy)

@app.route("/api/emissions")
def emission():
    emissions = db.emission.find()
    # print(emissions)
    emissions = pd.DataFrame(list(emissions))
    # cleaning with for loop here
    emissions = emissions.drop(columns='_id').T.to_dict()
    return jsonify(emissions)

@app.route("/api/evconsumption")
def consumption():
    consumption = db.evconsumptiontest.find()
    consumption = pd.DataFrame(list(consumption))
    consumption = consumption.drop(columns='_id').T.to_dict()
    return jsonify(consumption)

# @app.route("/api/registrationcount")
# def reg_count():
#     reg_count = db.registrationtest.find()
#     reg_count = pd.DataFrame(list(reg_count))
#     reg_count = reg_count.drop(columns='_id').T.to_dict()
#     reg_count = reg_count.group_by('Registration Valid Date').sum
#     return jsonify (reg_count)

>>>>>>> Stashed changes
#web page routes 
@app.route("/")
def home(): 
    return render_template("home.html")

@app.route("/analysis")
def analysis(): 
    return render_template("analysis.html")

@app.route("/about")
def about():
    return  render_template("about.html")
<<<<<<< Updated upstream
    
=======




>>>>>>> Stashed changes

if __name__ == "__main__": 
    app.run(debug=True)