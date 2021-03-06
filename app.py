import os
import pandas as pd
import json
import csv
import pymongo
from pymongo import MongoClient 

from flask import Flask, redirect, url_for, render_template, jsonify

app = Flask(__name__)
#Note: switch made to web mongoDB db in db_path & the DB name to EVData
db_path = "mongodb://abarmago:GaTech1234@evdata-shard-00-00.lcvwb.mongodb.net:27017,evdata-shard-00-01.lcvwb.mongodb.net:27017,evdata-shard-00-02.lcvwb.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-g33pj8-shard-0&authSource=admin&retryWrites=true&w=majority"
mongo = MongoClient(db_path)
db = mongo.EVData

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
    emissions = db.emissions.find()
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

@app.route("/api/transposed")
def trans():
    trans = db.transemissions.find()
    trans = pd.DataFrame(trans)
    trans ['Car Registrations'] = trans ['Car Registrations'].fillna(0)
    trans = trans.rename(columns={'Unnamed: 0':'Year'})
    trans = trans.set_index('Year')
    trans = trans.drop(columns='_id').T.to_dict()
    return jsonify(trans)

@app.route("/api/top5ev")
def top5():
    top5 = db.finaltop5ev.find()
    top5 = pd.DataFrame(top5)
    # top5 = top5.set_index('Year')
    top5 = top5.drop(columns='_id').T.to_dict()
    return jsonify(top5)

#user be warned this is 2MM rows of data and will take a long time to load
# @app.route("/api/evregistrations")
# def reg_count():
#     reg_count = db.registrationtest.find()
#     reg_count = pd.DataFrame(list(reg_count))
#     reg_count = reg_count.drop(columns='_id').T.to_dict()
#     return jsonify (reg_count)

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





if __name__ == "__main__": 
    app.run(debug=True)