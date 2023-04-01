from flask import Flask, g, jsonify, request, make_response
import sqlite3

from event import EventMapper
from person import PersonMapper
from group import GroupMapper

app = Flask(__name__)

DATABASE = 'development.db'

def get_db():
    sqlite3.register_adapter(bool, int)
    sqlite3.register_converter("BOOLEAN", lambda v: bool(int(v)))

    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)

    db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def health_check():
    return jsonify({"message": "Hi Emi :)"})

def missing_parameter_error(param):
    return make_response(
        {
            "type": "https://api.designated-driver.com/errors/missing-parameter",
            "title": f"Missing parameter: {param}",
        },
        400
    )

@app.route("/events", methods=['GET', 'POST'])
def events():
    with get_db() as cursor:
        if request.method == "GET":
            person_id = request.args.get('person_id')

            if person_id:
                event = EventMapper.find_by_person(cursor, person_id)
            else:
                return missing_parameter_error("person_id")

        if request.method == "POST":
            person = request.json
            event = EventMapper.create(cursor, person)

        return jsonify(dict(event))


@app.route("/events/<event_id>/assign", methods=['GET', 'POST'])
def assign_event(event_id):
    with get_db() as cursor:
        GroupMapper.assign(cursor, event_id)


@app.route("/events/<event_id>/groups", methods=['GET'])
def groups(event_id):
    with get_db() as cursor:
        person_id = request.args.get("person_id")

        if person_id:
            groups = GroupMapper.find_by_person(cursor, person_id)
        else:
            groups = PersonMapper.retrieve_event_groups(cursor, event_id)

        return jsonify(groups)

@app.route("/people", methods=['GET', 'POST'])
def people():
    with get_db() as cursor:
        if request.method == "POST":
            person = request.json
            person = PersonMapper.create(cursor, person)

        return jsonify(dict(person))
    