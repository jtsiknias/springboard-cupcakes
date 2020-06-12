from flask import Flask, request, render_template, flash, redirect, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from secrets import SECRET_KEY
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///cupcakes"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
connect_db(app)


@app.route("/")
def homepage():
    return render_template("index.html")


@app.route("/api/cupcakes")
def list_cupcakes():
    # all_cupcakes is a list, so can't serialize that directly. instead, serialize each cupcake via a list comprehension
    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=all_cupcakes)
