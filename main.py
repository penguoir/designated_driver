from flask import Flask, g, jsonify, request
import sqlite3

app = Flask(__name__)

DATABASE = 'development.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def health_check():
    return jsonify({"message": "Hi Emi :)"})

@app.route("/events", methods=['POST'])
def events():
    if request.method == "POST":
        cursor = get_db().cursor()
        event = Event.create(cursor, {})

        return jsonify({
            id: event.id,
            destination_location: event.destination_location,
        })