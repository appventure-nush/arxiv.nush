from flask import Flask, request, jsonify
import pandas as pd
from pandasql import sqldf
from flask_cors import CORS

nush_students = pd.read_csv("data/nush_students.csv")
nush_teachers = pd.read_csv("data/nush_teachers.csv")
projects = pd.read_csv("data/projects.csv")
works_on = pd.read_csv("data/works_on.csv")

app = Flask(__name__)
app.secret_key = "super_secret_key"
CORS(app)


def getStudentDetails(email):
    res = sqldf(
        f"""
        SELECT *
        FROM nush_students
        WHERE email = '{email}'
        """
    ).iloc[0].to_dict()
    res["graduationYear"] = int(res["graduationYear"])
    return res

def getProjects(email):
    projects = sqldf(
        f"""
        SELECT *
        FROM projects
        WHERE "{email}" in (
            SELECT studentEmail
            FROM works_on
            WHERE works_on.pcode = projects.pcode
        )
        """
    ).to_dict('records')

@app.route("/projectsByStudent", methods=["GET"])
def projectsByStudent():
    email = request.args.get("email@nushigh.edu.sg", "h1810124", str)
    res = jsonify(list(sqldf(
        f"""
        SELECT *
        FROM projects NATURAL JOIN works_on
        WHERE "{email}" in (
            SELECT studentEmail
            FROM works_on
            WHERE works_on.pcode = projects.pcode
        )
        """
    ).groupby(["pcode", "title", "teacherEmail", "year"]).studentEmail.agg(list).reset_index().T.to_dict().values()))
    #res.headers.add('Access-Control-Allow-Origin', '*')
    return res


@app.route("/student", methods=["GET"])
def student():
    email = request.args.get("email", "h1810124@nushigh.edu.sg", str)
    
    res = jsonify(getStudentDetails(email))
    #res.headers.add('Access-Control-Allow-Origin', '*')
    return res


@app.route("/teacher", methods=["GET"])
def teacher():
    email = request.args.get("email", "nhscsp@nushigh.edu.sg", str)
    res = sqldf(
        f"""
        SELECT *
        FROM nush_teachers
        WHERE email = '{email}'
        """
    ).iloc[0].to_dict()
    res = jsonify(res)
    #res.headers.add('Access-Control-Allow-Origin', '*')
    return res


@app.route('/')
def hello_world():
    return '<h1>Hello World!</h1>'


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
