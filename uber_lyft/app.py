# import necessary libraries
# from models import create_classes
import os
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, or_
from sqlalchemy.ext.automap import automap_base


import pickle

from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)
from flask_cors import CORS

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
CORS(app)
# ---------------------------------------------------------
# Web site

@app.route("/api/prediction/<origin>/<destination>/<weather>/<vehicleType>/<weekDay>" , methods=["GET"])
def model(origin, destination, weather, vehicleType, weekDay):
    print(origin)
    print(destination)
    print(weather)
    print(vehicleType)
    print(weekDay)
    
    #return jsonify(results)

    distance = 1.11#float(request.form["distance"])
    Monday = 1 #float(request.form["bedrooms"])
    Tuesday = 0
    Wednesday = 0
    Thursday = 0
    Friday = 0
    Saturday = 0
    Sunday = 0

    Mostly_Cloudy = 0
    Rain = 0
    Partly_Cloudy = 0 
    Clear = 1
    Overcast = 0
    Light_Rain = 0
    Foggy = 0
    Possible_Drizzle = 0
    Drizzle = 0

    UberPool = 0
    UberXL = 0
    Black = 0
    Black_SUV = 0
    WAV = 0
    UberX = 1

    Shared = 0
    LyftXL = 0
    Lux_Black = 0
    Lux_Black_XL = 0
    Lux = 0
    Lyft = 1
    
    prediction_u = 0
    prediction_l = 0

    X_u = [[distance, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday,
          UberPool, UberXL, Black, Black_SUV, WAV, UberX, Mostly_Cloudy, Rain, Partly_Cloudy, 
          Clear, Overcast, Light_Rain, Foggy, Possible_Drizzle, Drizzle]]

    X_l = [[distance, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday,
          Shared, LyftXL, Lux_Black, Lux_Black_XL, Lux, Lyft, Mostly_Cloudy, Rain, Partly_Cloudy, 
          Clear, Overcast, Light_Rain, Foggy, Possible_Drizzle, Drizzle]]
    
    print(X_u)
    print(X_l)

    filename_u = './Data/u_model.sav'
    loaded_model_u = pickle.load(open(filename_u, 'rb'))

    print(loaded_model_u.predict(X_u))
    
    prediction_u = loaded_model_u.predict(X_u)[0]

    print(prediction_u)

    filename_l = './Data/l_model.sav'
    loaded_model_l = pickle.load(open(filename_l, 'rb'))

    print(loaded_model_l.predict(X_l))
    
    prediction_l = loaded_model_l.predict(X_l)[0]

    print(prediction_l)

    type_car = 'Same price for Uber and Lyft'
    price = prediction_u
    
    if prediction_u < prediction_l:
        type_car = 'Uber'
        price = prediction_u
    else:
        type_car = 'Lyft'
        price = prediction_l

    results = {
        "type": type_car,
        "price":  "${0:,.2f}".format(price)
    }
    print(results)
    return jsonify(results)


if __name__ == "__main__":
    app.run()
