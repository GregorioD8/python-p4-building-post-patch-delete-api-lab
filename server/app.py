#!/usr/bin/env python3

# Import necessary modules and functions from Flask and Flask extensions
from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

# Import the database models from a separate file called models
from models import db, Bakery, BakedGood

# Create an instance of the Flask class
app = Flask(__name__)

# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# Set up the Flask-Migrate extension for database migrations
migrate = Migrate(app, db)

# Initialize the app with the database
db.init_app(app)

# Define the route for the index page
@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

# Define the route to get a list of all bakeries
@app.route('/bakeries')
def bakeries():
    # Use a list comprehension to convert each bakery to a dictionary
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    # Create a response with the list of bakeries and a 200 OK status
    return make_response(  bakeries,   200  )

## Define a PATCH block inside of the /bakeries/<int:id> route that updates the name 
## of the bakery in the database and returns its data as JSON. As with the 
## previous POST block, the request will send data in a form. The form does 
## not need to include values for all of the bakery's attributes.

# Define the route to handle GET and PATCH requests for a specific bakery by ID
@app.route('/bakeries/<int:id>', methods=['GET', 'PATCH'])
def bakery_by_id(id):
    # Query the bakery with the given ID from the database
    bakery = Bakery.query.filter_by(id=id).first()

    if request.method == 'GET':
        # Handle GET request: retrieve the bakery
        return make_response(bakery.to_dict(), 200)

    elif request.method == 'PATCH':
        # Handle PATCH request: update the bakery
        for attr in request.form:
            setattr(bakery, attr, request.form.get(attr))
        
        # Add the updated bakery to the database session and commit it
        db.session.add(bakery)
        db.session.commit()

    # Convert the updated bakery to a dictionary
    bakery_dict = bakery.to_dict()
    return make_response( bakery_dict , 200  )

## Define a POST block inside of a /baked_goods route that creates a new baked good 
## in the database and returns its data as JSON. The request will send data in a form.

# Define the route to handle GET and POST requests for baked goods
@app.route('/baked_goods', methods=['GET', 'POST'])
def baked_goods():
    if request.method == 'GET':
        # Handle GET request: retrieve all baked goods
        baked_goods = [bg.to_dict() for bg in BakedGood.query.all()]
        return make_response(baked_goods, 200)
        
    elif request.method == 'POST':
        # Handle POST request: create a new baked good
        baked_good = BakedGood(
            name = request.form.get('name'),
            price = request.form.get('price'),
            bakery_id = request.form.get('bakery_id')

        )

        #Add the new baked good to the database session and commit it
        db.session.add(baked_good)
        db.session.commit()
        
        # Create a response with the new baked good dictionary and a 201 Created status
        return make_response(baked_good.to_dict(), 201)

## Define a DELETE block inside of a /baked_goods/<int:id> route that deletes the baked good 
## from the database and returns a JSON message confirming that the record was successfully deleted.

# Define the route to handle GET and DELETE requests for a specific baked good by ID
@app.route('/baked_goods/<int:id>', methods=['GET', 'DELETE'])
def baked_goods_by_id(id):

    # Query the baked good with the given ID from the database
    baked_good = BakedGood.query.filter_by(id=id).first()

    if request.method == 'GET':
        # Handle GET request: retrieve the baked good
        return make_response(baked_good.to_dict(), 200)
    
    elif request.method == 'DELETE':
        # Handle DELETE request: delete the baked good
        db.session.delete(baked_good)
        db.session.commit()
        return make_response({'message': 'record successfully deleted'}, 200)

# Define the route to get a list of baked goods ordered by price in descending order
@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    # Query all baked goods ordered by price in descending order
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price.desc()).all()
    # Convert each baked good to a dictionary
    baked_goods_by_price_serialized = [ bg.to_dict() for bg in baked_goods_by_price]
    # Create a response with the list of baked goods and a 200 OK status
    return make_response(baked_goods_by_price_serialized, 200)
   
# Define the route to get the most expensive baked good
@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    # Query the most expensive baked good
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    # Convert the most expensive baked good to a dictionary
    most_expensive_serialized = most_expensive.to_dict()
    # Create a response with the most expensive baked good and a 200 OK status
    return make_response( most_expensive_serialized,   200  )

if __name__ == '__main__':
    app.run(port=5555, debug=True)