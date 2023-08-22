from flask import Flask, request, jsonify
from flask_cors import CORS
from database import Database

#app = Flask(__name__,static_url_path='/dist')
app = Flask(__name__)
app.secret_key = "super_secret_key"
CORS(app)
database = Database(app)


# Authentication
# ==================================================
#  /login : Login
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    return jsonify(database.login(
        data.get("email", ""), 
        data.get("password", "")
    ))

#  /register : Registration
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    print(data)
    isTeacher = data.get("isTeacher", None)
    if isTeacher is None:
        return {
            "result": False, 
            "user": None, 
            "message": "Unknown Registration Method!"
        }
    if isTeacher:
        return database.registerTeacher(
            data.get("email", ""), data.get("password", ""), 
            data.get("name", ""), data.get("deptId", ""), 
        )
    return database.registerStudent(
        data.get("email", ""), data.get("password", ""), 
        data.get("name", ""), data.get("gradYear", 0)
    )


#  /update/password : Update Password
@app.route("/update/password", methods=["POST"])
def updatePassword():
    data = request.get_json()
    return jsonify(
        database.changePassword(
            data.get("email", ""), data.get("oldPw", ""), data.get("newPw", "")
        )
    )

# ==================================================

    

# Projects
# ==================================================
#  /create/project : Project Creation
@app.route("/create/project", methods=["POST"])
def createProject():
    data = request.get_json()
    return jsonify(database.createProject(
        data.get("pcode", ""), 
        data.get("year", 0), 
        data.get("deptId", ""), 
        data.get("title", ""), 
        data.get("abstract", ""), 
        data.get("teacherEmail", ""), 
        data.get("authorEmails", [])
    ))

#  /update/project : Project Update
@app.route("/update/project", methods=["POST"])
def updateProject():
    data = request.get_json()
    res = database.updateProject(
        data.get("pcode", ""), 
        data.get("title", ""), 
        data.get("abstract", ""), 
        data.get("reportPdf", "")
    )
    return jsonify(res)

#  /delete/project : Project Deletion
@app.route("/delete/project", methods=["POST"])
def deleteProject():
    data = request.get_json()
    return jsonify(database.deleteProject(
        data.get("pcode", "")
    ))

# ==================================================


# Submissions
# ==================================================
#  /create/submission : Submission Creation
@app.route("/create/submission", methods=["POST"])
def createSubmission():
    data = request.get_json()
    return jsonify(database.createSubmission(
        data.get("eventId", ""), 
        data.get("year", 0), 
        data.get("code", ""),
        data.get("subTitle", ""), 
        data.get("subAbstract", ""),
        data.get("pcodes", []), 
        data.get("authorEmails", [])
    ))



#  /delete/submission : Submission Deletion
@app.route("/delete/submission", methods=["POST"])
def deleteSubmission():
    data = request.get_json()
    return jsonify(database.deleteSubmission(
        data.get("eventId", ""),
        data.get("year", 0), 
        data.get("code", "")
    ))



@app.route("/stats/<id>", methods=["GET"])
def stats(id):
    email = (("h1810124" if id == "" else id) + "@nushigh.edu.sg") if "@" not in id else id
    return jsonify({
        "projectStats": database.projectStats(email),
        "submissionStats": database.submissionStats(email),
        "awardStats": database.awardStats(email),
        "projectAwardStats": database.projectAwardStats(email)
    })



@app.route("/search/students", methods=["GET"])
def searchStudents():
    res = jsonify(database.searchAllStudents())
    return res

@app.route("/search/teachers", methods=["GET"])
def searchTeachers():
    res = jsonify(database.searchAllTeachers())
    return res

@app.route("/student/<id>", methods=["GET"])
def student(id):
    email = (("h1810124" if id == "" else id) + "@nushigh.edu.sg") if "@" not in id else id
    res = jsonify(database.student(email))
    return res

@app.route("/teacher/<email>", methods=["GET"])
def teacher(email):
    email = "nhscsp@nushigh.edu.sg" if email == "" else email
    # email = request.args.get("email", "nhscsp@nushigh.edu.sg", str)
    
    res = jsonify(database.teacher(email))
    return res


@app.route("/institute/<id>", methods=["GET"])
def institute(id):
    id = "NUS" if id == "" else id
    res = jsonify(database.institute(id))
    return res

@app.route("/projects/<id>", methods=["GET"])
def getProjects(id):
    if("@" not in id): id += "@nushigh.edu.sg"
    if(database.isStudent(id)): res = jsonify(database.studentProjects(id))
    elif(database.isMentor(id)): res = jsonify(database.projectsByMentor(id))
    else: res = jsonify(database.teacherProjects(id))
    return res

@app.route("/mentorStudents/<email>", methods=["GET"])
def getMentorStudents(email):
    return jsonify(database.mentorStudents(email))

@app.route("/bestStudents/<email>", methods=["GET"])
def getBestStudents(email):
    email = "nhscsp@nushigh.edu.sg" if email == "" else email
    return jsonify(database.best_students(email))

@app.route("/extTeacherStudents/<email>", methods=["GET"])
def getExtTeacherStudents(email):
    return jsonify(database.extTeacherStudents(email))
    
@app.route("/mentor/<email>", methods=["GET"])
def getMentors(email):
    return jsonify(database.mentor(email))

@app.route("/projectsByMentor/<email>", methods=["GET"])
def getMentorProjects(email):
    return jsonify(database.projectsByMentor(email))

@app.route("/event/<eventId>/<int:year>", methods=["GET"])
def getEvent(eventId, year):
    return jsonify(database.event(eventId, year))

@app.route("/events", methods=["GET"])
def getEvents():
    return jsonify(database.events())


@app.route("/otherProjects/<email>", methods=["GET"])
def getOtherProjects(email):
    return jsonify(database.otherProjects(email))
    
@app.route("/otherEvents/<email>", methods=["GET"])
def getOtherEvents(email):
    return jsonify(database.otherEvents(email))

@app.route("/project/<pcode>", methods=["GET"])
def project(pcode):
    pcode = "23.018.NUSH.CS" if pcode == "" else pcode
    res = jsonify(database.project(pcode))
    return res

@app.route("/authors/<pcode>", methods=["GET"])
def authors(pcode):
    pcode = "23.018.NUSH.CS" if pcode == "" else pcode
    res = jsonify(database.projectMembers(pcode))
    return res

@app.route("/update/student", methods=["POST"])
def updateStudent():
    data = request.get_json()
    email = data.get("sid", "")+"@nushigh.edu.sg"
    about = data.get("about", "")
    pfp = data.get("pfp", "")
    print(len(pfp))
    res = database.updateStudent(email, pfp, about)
    return jsonify(res)

@app.route("/submission/<eventId>/<year>/<code>", methods=["GET"])
def submission(eventId, year, code):
    return database.submission(eventId, year, code)

@app.route("/submissions/<pcode>", methods=["GET"])
def submissions(pcode):
    res = jsonify(database.submissionsByProject(pcode))
    return res

@app.route("/submissions/user/<email>", methods=["GET"])
def submissionsByUser(email):
    if("@" not in email): email += "@nushigh.edu.sg"
    res = jsonify(database.submissionsByUser(email))
    return res

@app.route("/submissions/all/<email>", methods=["GET"])
def getEverySubmission(email):
    if("@" not in email): email += "@nushigh.edu.sg"
    res = jsonify(database.strongSubmissions(email))
    return res

@app.route("/coauthors/<id>", methods=["GET"])
def coauthors(id):
    if(id == ""): id = "h1810124"
    res = jsonify(database.coauthors(id+"@nushigh.edu.sg"))
    return res

@app.route("/removeStudent", methods=["POST"])
def removeStudent():
    data = request.get_json()
    res = jsonify(database.removeStudentFromProject(data.get("email", ""), data.get("pcode", "")))
    return res

@app.route("/submission/remove", methods=["POST"])
def removeStudentFromSubmission():
    data = request.get_json()
    res = jsonify(database.removeStudentFromSubmission(
        data.get("email", ""), data.get("eventId", ""), data.get("year", 0), data.get("code", "")
    ))
    return res


@app.route("/addExtStudent", methods=["POST"])
def addExtStudent():
    data = request.get_json()
    database.createExternalStudent(
        data.get("email", ""), data.get("name", ""), data.get("teacherEmail", ""),
        data.get("teacherName", ""), data.get("instId", "")
    )
    return jsonify({"result": "Success"})

@app.route("/addStudents", methods=["POST"])
def addStudents():
    data = request.get_json()
    # Assume that the data is formatted as follows: {students: ["email1", "email2"], pcode: ""}
    pcode = data.get("pcode", "")
    students = [student for student in data.get("students", []) if database.student(student)]
    database.addStudentsToProject(students, pcode)
    return jsonify({"result": "Success"})

@app.route("/submissions/add", methods=["POST"])
def addStudentsToSubmission():
    data = request.get_json()
    eventId = data.get("eventId", "")
    year = data.get("year", 0)
    code = data.get("code", "")
    students = [student for student in data.get("students", []) if database.student(student)]
    database.addStudentsToSubmission(students, eventId, year, code)
    return jsonify({"result": "Success"})

@app.route("/search/schools", methods=["GET"])
def searchSchools():
    res = jsonify(database.searchSchools())
    return res

@app.route("/search/organisers", methods=["GET"])
def searchOrganisers():
    res = jsonify(database.searchOrganisers())
    return res

@app.route("/create/researchEvent", methods=["POST"])
def createEvent():
    data = request.get_json()
    return jsonify(database.createResearchEvent(
        data.get("eventId", ""), data.get("year", 0), data.get("name", ""),
        data.get("start_date", ""), data.get("end_date", ""), data.get("format", ""),
        data.get("about", ""), data.get("isCompetition", False), data.get("isConference", False),
        data.get("organisers", []), data.get("awardTypes", []), data.get("confDoi", "")
    ))


@app.route("/update/researchEvent", methods=["POST"])
def updateEvent():
    data = request.get_json()
    return jsonify(database.updateResearchEvent(
        data.get("eventId", ""), data.get("year", 0), data.get("name", ""),
        data.get("start_date", ""), data.get("end_date", ""), data.get("format", ""),
        data.get("about", ""), data.get("isCompetition", False), data.get("isConference", False),
        data.get("organisers", []), data.get("awardTypes", []), data.get("confDoi", "")
    ))

@app.route("/update/submission", methods=["POST"])
def updateSubmission():
    data = request.get_json()
    return jsonify(database.updateSubmission(
        data.get("eventId", ""), data.get("year", 0), data.get("code", ""),
        data.get("subTitle", ""), data.get("subAbstract", "")
    ))
    

# @app.route("/search/teachers", methods=["GET"])

@app.route("/search/journals", methods=["GET"])
def getJournals():
    return jsonify(database.journals())


@app.route('/')
def hello_world():
    return '<h1>Hello World!</h1>'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
