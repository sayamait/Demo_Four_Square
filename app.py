# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 11:59:12 2016

@author: sayamait
"""

from flask import Flask, render_template,request
from flask_bootstrap import Bootstrap
import pandas as pd
import numpy as np
#import json
import foursquare
#import requests
#from geopy.distance import vincenty
from geopy.geocoders import Nominatim
#from time import strftime, localtime
#import simplejson, urllib
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
#from dotmap import DotMap


app = Flask(__name__)
GoogleMaps(app)
bootstrap = Bootstrap(app)


@app.route('/')
def index():    
    return render_template('index.html')
    
def hunger_index_4sqr(address):
 client_id = "CFFIHXMB5VA42LSMSQN1BMCMQRTY4YMTLUHA25JGQIYRJARR"
 client_secret = "K1Q4RVUI4XZUJFY2CDPXSJ4UES4E5TMC05GP3PYRJGVFQ2VL"
 client = foursquare.Foursquare(client_id , client_secret , redirect_uri='http://capstone-under-construction.herokuapp.com/index')
 auth_uri = client.oauth.auth_url()
 access_token = client.oauth.get_token('')
 geolocator = Nominatim()
 location = geolocator.geocode(address)
 #location= DotMap()
 #location.latitude=25.7959
 #location.longitude=-80.2870
 rsqr_data=client.venues.search(params={'query': 'food', 'll':str(location.latitude)+','+str(location.longitude), 'intent': 'checkin'})
 frsqr_data=rsqr_data['venues']
 chkin_name_data = [] 
 for i in range (0,len(frsqr_data)):
    	chkin_name_data.append((frsqr_data[i]['location']['lat'],frsqr_data[i]['location']['lng'],str(frsqr_data[i]['name'].encode('utf-8'))))
 df = pd.DataFrame(chkin_name_data)  
 return df
 
@app.route('/foursqr_analysis/', methods=['GET', 'POST'])
def api_frsqr():
 if request.method == 'POST':
  address = request.form['address']
  geolocator = Nominatim()
  location = geolocator.geocode(address)
  #location= DotMap()
  #location.latitude=25.7959
  #location.longitude=-80.2870
  thres_search=request.form['distance']
  mydf=hunger_index_4sqr(address)
  mydf1=mydf.values.tolist()
  mydf2=[tuple(l) for l in mydf1]
  sndmap = Map(
  identifier="sndmap",
  lat=location.latitude,
  lng=location.longitude,
  style="height:750px;width:750px;margin:0;",
  markers={'http://maps.google.com/mapfiles/ms/icons/green-dot.png':[(location.latitude, location.longitude, "Current Location")],
           'http://maps.google.com/mapfiles/ms/icons/blue-dot.png':mydf2}
  )
  x = pd.DataFrame(np.random.randn(20, 2))
  mydf.columns = ["Latitude", "Longitude", "Name"]
  return render_template("analysis.html", sndmap=sndmap, tables=mydf)
 return render_template("data_entry_2.html") 
 

    
if __name__ == "__main__":
    app.run(debug=True)    
    
    

       
       