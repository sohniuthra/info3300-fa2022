
# If this code does not work, make sure that you've installed Flask
# This code should work in both Python 2 and 3
from flask import *
import json, csv
from pprint import pprint

app = Flask(__name__, static_url_path='')


@app.route('/')
def index():
    return app.send_static_file("index.html") #will look for a directory called static and find the given file there

@app.route('/css/<path:path>') #wildcard sends all css files at once
def send_css(path):
    return send_from_directory('css', path)

map = {}
with open('pittsburgh_neighborhoods.json') as f:
    map = json.load(f)

@app.route('/map')
def pghmap():
    #wraps object in json and sends to client (/map)
    return jsonify(map)


db = {} 
with open('pgh_homes.json') as f:
    homes = json.load(f)
    for home in homes:
        db[home['HouseID']] = home

# HouseID => {'HouseID','Neighborhood','Latitude','Longitude','Lot Size','Finished Size','Sale Price','Year Built','Bathrooms','Bedrooms','Description'}

outputKeys = ['HouseID','Neighborhood','Latitude','Longitude','Sale Price','Bathrooms','Bedrooms','Lot Size']

@app.route('/houses')
def houses():
    # return jsonify(db) --> too much to send

    houses = []
    priceMin = request.args.get('priceMin', None, type=float)
    priceMax = request.args.get('priceMax', None, type=float)
    
    for home in db.values():

        #do this for rest of parameters for filtering
        if priceMin is not None and home['Sale Price'] < priceMin:
            continue
        outputHome = {key: home[key] for key in outputKeys}
        houses.append(outputHome)
    return jsonify(houses)
    
# DO NOT DO THIS IN A PRODUCTION ENVIRONMENT
# ARGUABLY, THIS IS EVEN A BAD THING FOR DEVELOPING WITH FLASK
# You should never expose dev servers to the public
# Always use a bridge with a real web server if you're doing this
if __name__ == '__main__': #if running from the command line
    app.run(host='0.0.0.0',port='9999')
    
    
    
