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


# def getProjects(email):
#     projects = sqldf(
#         f"""
#         SELECT *
#         FROM projects
#         WHERE "{email}" in (
#             SELECT studentEmail
#             FROM works_on
#             WHERE works_on.pcode = projects.pcode
#         )
#         """
#     ).to_dict('records')

# @app.route("/projectsByStudent", methods=["GET"])
# def projectsByStudent():
#     email = request.args.get("email@nushigh.edu.sg", "h1810124", str)
#     res = jsonify(list(sqldf(
#         f"""
#         SELECT *
#         FROM projects NATURAL JOIN works_on
#         WHERE "{email}" in (
#             SELECT studentEmail
#             FROM works_on
#             WHERE works_on.pcode = projects.pcode
#         )
#         """
#     ).groupby(["pcode", "title", "teacherEmail", "year"]).studentEmail.agg(list).reset_index().T.to_dict().values()))
#     #res.headers.add('Access-Control-Allow-Origin', '*')
#     return res


@app.route("/student", methods=["GET"])
def student():
    id = request.args.get("id", "h1810124", str)
    res = jsonify(database.student(id))
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

@app.route("/authors", methods=["GET"])
def authors():
    pcode = request.args.get("pcode", "23.018.NUSH.CS", str)
    res = jsonify(database.projectMembers(pcode))
    return res

@app.route("/projects", methods=["GET"])
def 

@app.route("/coauthors", methods=["GET"])
def coauthors():
    email = request.args.get("email", "h1810124@nushigh.edu.sg", str)
    res = jsonify(database.coauthors(email))
    return res

@app.route('/')
def hello_world():
    return '<h1>Hello World!</h1>'


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
