from flask import Flask, request, jsonify, session
import pandas as pd
from flask_cors import CORS
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from database import Database

app = Flask(__name__)
app.secret_key = "super_secret_key"
CORS(app)
database = Database(app)





@app.route("/student/<id>", methods=["GET"])
def student(id):
    email = ("h1810124" if id == "" else id) + "@nushigh.edu.sg"
    res = jsonify(database.student(email))
    return res

@app.route("/teacher", methods=["GET"])
def teacher():
    email = request.args.get("email", "nhscsp@nushigh.edu.sg", str)
    res = jsonify(database.teacher(email))
    return res

@app.route("/institute", methods=["GET"])
def institute():
    id = request.args.get("id", "NUS", str)
    res = jsonify(database.institute(id))
    return res

@app.route("/authors/<pcode>", methods=["GET"])
def authors(pcode):
    pcode = "23.018.NUSH.CS" if pcode == "" else pcode
    res = jsonify(database.projectMembers(pcode))
    return res

# @app.route("/projects", methods=["GET"])
# def projects():
    

@app.route("/coauthors/<id>", methods=["GET"])
def coauthors(id):
    if(id == ""): id = "h1810124"
    res = jsonify(database.coauthors(id+"@nushigh.edu.sg"))
    return res

@app.route('/')
def hello_world():
    return '<h1>Hello World!</h1>'


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
