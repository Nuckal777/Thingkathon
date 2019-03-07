from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from .models import Model, Apartment, Ownership, Producer, Production, Consumption
# run the app FLASK_APP=cobweb.app flask run --debugger --reload
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cobweb.db'
db = SQLAlchemy(app, model_class=Model)

#@app.route("/")
#def hello():
#    apartments = db.session.query(Apartment).count()
#    return jsonify(apartments=apartments)
def get_consumptions_by_date(date_time, consumptions):
    result = {
        "otherDate": date_time,
        "solar": 0,
        "battery": 0,
        "external": 0
    }
    for c in consumptions:
        if c.time == date_time and c.origin == "solar":
            #result.otherDate = date_time
            result["solar"] = c.energy
        elif c.time == date_time and c.origin == "battery":
            result["battery"] = c.energy
        elif c.time == date_time and c.origin == "external":
            result["external"] = c.energy

    return result

def get_profit_by_date(date_time, consumptions): 
    
    solar = 0
    battery = 0
    external = 0
    result = {
        "otherDate": date_time,
        "profit": 0
    }
    for c in consumptions:
        if c.time == date_time and c.origin == "solar":
            solar = c.price
        elif c.time == date_time and c.origin == "battery":
            battery = c.price
        elif c.time == date_time and c.origin == "external":
            external = c.price

    profit = external - battery - solar
    result["profit"] = profit
    return result

def is_exist(date_time, results):
    exist = False
    for r in results:
        if r["otherDate"] == date_time:
            exist = True
    return exist

@app.route("/apartments")
def list_apartments():
    apartments = db.session.query(Apartment)
    return jsonify([a.json() for a in apartments])


@app.route("/productions/<apartmentId>/<producerId>")
def get_ownerships(apartmentId, producerId):
    ownerships = db.session.query(Ownership)\
        .filter(Apartment.id == apartmentId)\
        .filter(Producer.id == producerId)

    productions = []
    for o in ownerships:
        productions += db.session.query(Production).filter(Production.producer_id == o.producer_id)

    return jsonify([p.json() for p in productions])


@app.route("/consumptions/<apartmentId>")
def get_consumptions(apartmentId):
    print(apartmentId)

    consumptions = db.session.query(Consumption).filter(Consumption.apartment_id == apartmentId)
    response = []

    for c in consumptions:
        if not is_exist(c.time, response):
            response.append(get_consumptions_by_date(c.time, consumptions))    

    return jsonify(response)

@app.route("/savings/<apartmentId>")
def get_savings(apartmentId):
    print(apartmentId)

    consumptions = db.session.query(Consumption).filter(Consumption.apartment_id == apartmentId)
    response = []

    for c in consumptions:
        if not is_exist(c.time, response):
            response.append(get_profit_by_date(c.time, consumptions))    

    return jsonify(response)

