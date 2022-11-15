"""Flask app for Cupcakes"""

from flask import Flask, request, redirect, render_template, jsonify
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://michelle:1003866Ma@localhost/cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.app_context().push()

connect_db(app)

@app.route("/")
def homepage():
    return render_template("index.html")

@app.route("/api/cupcakes")
def list_all_cupcakes():
    """Return JSON all cupcakes"""

    cupcakes = Cupcake.query.all()
    serialized = [Cupcake.serialize_cupcake(c) for c in cupcakes]

    return jsonify(cupcakes=serialized)

@app.route("/api/cupcakes/<int:cupcake_id>")
def list_selected_cupcake(cupcake_id):
    """Return JSON selected cupcake"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = Cupcake.serialize_cupcake(cupcake)

    return jsonify(cupcake=serialized)

app.route("/api/add-cupcakes", methods=["POST"])
def create_cupcake():
    """Create cupcake and return JSON"""

    new_cupcake = Cupcake(
        flavor=request.json["flavor"],
        size=request.json["size"],
        rating=request.json["rating"],
        image=request.json["image"] or None)

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = Cupcake.serialize_cupcake(new_cupcake)

    return (jsonify(cupcake=serialized), 201)