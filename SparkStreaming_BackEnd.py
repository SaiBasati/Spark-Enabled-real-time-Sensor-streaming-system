import json
import datetime
from flask import Flask, jsonify
from datetime import timedelta
from kafka import KafkaProducer
from flask import make_response, request, current_app
from functools import update_wrapper
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

client2 = MongoClient('mongodb://root:root@localhost:27017/test')
db2 = client2['test']
collection3 = db2['spark']

# Encode responce in JSON
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

# To solve cross origin problem (CORS filter)
def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers
            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

# service to get temprature data
@app.route("/gettemp", methods=["GET"])
@crossdomain(origin='*')
def get_my_temp():
    obj = []
    name = request.args.get('user');
    # Find all records and return
    cursor = collection3.find({'sensorID':str(name)})
    for document in cursor:
        obj.append(str(JSONEncoder().encode(document)))
    print(obj)
    return json.dumps(obj)

# service to produce temprature data on kafka
@app.route("/start", methods=["POST"])
@crossdomain(origin='*')
def getstarted():
    name = request.form['userName'];
    print(request.form['temperature']);
    object = {"sensorID": str(name),"time":datetime.datetime.now().strftime('%a %b %d %Y %H:%M:%S'),"temperature": str(request.form['temperature']),"flag": "false"}
    print(object)
    producer = KafkaProducer(value_serializer=lambda m: json.dumps(m).encode('ascii'))
    producer.send('test',object)
    print("Generated...")
    return json.dumps(object)

if __name__ == '__main__':
    app.run( host="localhost",port=int("8083"),debug = True)
