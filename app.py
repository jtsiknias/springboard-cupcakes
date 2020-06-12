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
    # all_cupcakes is a list, so can't serialize that directly. instead, serialize each cupcake via a list comprehension.
    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=all_cupcakes)


@app.route("/api/cupcakes/<int:id>")
def list_single_cupcake(id):
    """Respond with info about a single cupcake. 404 if id does not exist in table."""
    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cupcake.serialize())


@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    """Creates a new cupcake"""
    new_cupcake = Cupcake(
        flavor=request.json["flavor"], size=request.json["size"], rating=request.json["rating"], image=request.json["image"] or None)

    db.session.add(new_cupcake)
    db.session.commit()
    response_json = jsonify(cupcake=new_cupcake.serialize())
    # return tuple with status code as second argument
    return (response_json, 201)


@app.route("/api/cupcakes/<int:id>", methods=["PATCH"])
def update_cupcake(id):
    """Update part (or all) of an existing cupcake. Respond with JSON of the newly-updated cupcake, like this: {cupcake: {id, flavor, size, rating, image}}."""
    cupcake = Cupcake.query.get_or_404(id)
    cupcake.flavor = request.json.get("flavor", cupcake.flavor)
    cupcake.size = request.json.get("size", cupcake.size)
    cupcake.rating = request.json.get("rating", cupcake.rating)
    cupcake.image = request.json.get("image", cupcake.image)
    db.session.commit()
    return jsonify(cupcake=cupcake.serialize())


@app.route("/api/cupcakes/<int:id>", methods=["DELETE"])
def delete_cupcake(id):
    """Raises a 404 if the cupcake cannot be found. Delete cupcake with the id passed in the URL. Respond with JSON like {message: "Deleted"}."""
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="Deleted")
