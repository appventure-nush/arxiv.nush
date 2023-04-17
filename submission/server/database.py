from flask_mysqldb import MySQL
import MySQLdb.cursors
import base64
from util import convertB64toBytes, removeNulls
import random
import itertools


class Database:
    def __init__(self, app):
        app.config['MYSQL_HOST'] = 'localhost'
        app.config['MYSQL_USER'] = 'root'
        app.config['MYSQL_PASSWORD'] = 'admin'
        app.config['MYSQL_DB'] = 'arxiv'
        self.app = app
        self.mysql = MySQL(app)

    @property
    def connection(self):
        return self.mysql.connection

    @property
    def cursor(self):
        return self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    def execute(self, query, args=None, commit=True):
        cur = self.cursor
        cur.execute(query, args)
        if(commit): self.connection.commit()
        
    def executemany(self, query, args=None, commit=True):
        cur = self.cursor
        cur.executemany(query, args)
        if(commit): self.connection.commit()
    
    def queryAll(self, query, args=None):
        cur = self.cursor
        cur.execute(query, args)
        return cur.fetchall()
    
    def queryOne(self, query, args=None):
        cur = self.cursor
        cur.execute(query, args)
        return cur.fetchone()

    def close(self):
        self.connection.close()
        
    @property
    def pfp(self):
        with open("assets/default.png", "rb") as f:
            pfp = f.read()
        return pfp 
    
    
    
    
    # ==================================== EXISTS FUNCTIONALITY ====================================
    
    def isInstitute(self, email):
        return len(self.queryAll("SELECT instId FROM Institution WHERE email = %s", (email,))) > 0
        
    def isStudent(self, email):
        return len(self.queryAll("SELECT email FROM Student WHERE email = %s", (email, ))) > 0
        
    def isMentor(self, email):
        return len(self.queryAll("SELECT email FROM ResearchMentor WHERE email = %s", (email, ))) > 0
        
    def isNUSHTeacher(self, email):
        return len(self.queryAll("SELECT email FROM NUSHTeacher WHERE email = %s", (email, ))) > 0
        
    def isNUSHStudent(self, email):
        return len(self.queryAll("SELECT email FROM NUSHStudent WHERE email = %s", (email, ))) > 0
    
    
    
    # ================================ AUTHENTICATION FUNCTIONALITY ================================
    
    def studentLogin(self, email, pwd):
        query = "SELECT email FROM NUSHStudent WHERE email = %s and pwd = %s"
        return bool(self.queryOne(query, (email, pwd)))
    
    def teacherLogin(self, email, pwd):
        query = "SELECT email FROM NUSHTeacher WHERE email = %s and pwd = %s"
        return bool(self.queryOne(query, (email, pwd)))
        
    def login(self, email, password):
        isStudent = self.isNUSHStudent(email)
        isStudentAuth = self.studentLogin(email, password)
        isTeacher = self.isNUSHTeacher(email)
        isTeacherAuth = self.teacherLogin(email, password)
        
        if isStudent and isStudentAuth:
            return {
                "result": True, "user": self.NUSHStudent(email),
                "message": "Logged In Successfully!"
            }
        if isStudent and not isStudentAuth:
            return {
                "result": False, "user": None,
                "message": "Incorrect Password Provided!"
            }
        if isTeacher and isTeacherAuth:
            return {
                "result": True, "user": self.NUSHTeacher(email),
                "message": "Logged In Successfully!"
            }
        if isTeacher and not isTeacherAuth:
            return {
                "result": False, "user": None,
                "message": "Incorrect Password Provided!"
            }
        return {
            'result': False, "user": None,
            "message": "Account does not exist!"
        }
        
    def registerStudent(
        self, email, password, name, gradYear
    ):
        if not(email.endswith("@nushigh.edu.sg") and email[0] == 'h' and email[1:8].isnumeric()):
            return {
                "result": False, "user": None,
                "message": "Please give a valid email of form `hXXXXXXX@nushigh.edu.sg`."
            }
        existing = self.isNUSHStudent(email)
        if existing:
            if(self.studentLogin(email, password)):
                return {
                    "result": True, "user": self.NUSHStudent(email),
                    "message": "Account already exists, successfully logged in with details provided."
                }
            return {
                "result": False, "user": self.login(email, password),
                "message": "Account already exists!"
            }
        try:
            self.execute("INSERT INTO Student(email, name) VALUES (%s, %s)", (email, name), commit=False)
            self.execute("INSERT INTO NUSHStudent(email, pwd, pfp, gradYear, nush_sid) VALUES (%s, %s, %s, %s, %s)", (
                email, password, self.pfp, gradYear, email[:8]
            ))
            return {
                "result": True, "user": self.NUSHStudent(email), 
                "message": "Registered Successfully!"
            }
        except Exception as e:
            return {
                "result": False, "user": None,
                "message": str(e)
            }
        
    def registerTeacher(
        self, email, password, name, deptId
    ):
        if not(email.endswith("@nushigh.edu.sg")):
            return {
                "result": False, "user": None,
                "message": "Please give a valid email ending with `@nushigh.edu.sg`."
            }
        existing = self.isNUSHTeacher(email)
        if existing:
            if(self.teacherLogin(email, password)):
                return {
                    "result": True, "user": self.NUSHStudent(email),
                    "message": "Account already exists, successfully logged in with details provided."
                }
            return {
                "result": False, "user": self.login(email, password),
                "message": "Account already exists!"
            }
        try:
            self.execute("INSERT INTO NUSHTeacher(email, pwd, name, pfp, isAdmin, isMentor, deptId) VALUES (%s, %s, %s, %s, %s, %s, %s)", (
                email, password, name, self.pfp, False, False, deptId
            ))
            return {
                "result": True, "user": self.NUSHTeacher(email), "message": "Registered Successfully!"
            }
        except Exception as e:
            return {"result": False, "error": str(e)}
    
    def changePassword(self, email, oldPw, newPw):
        oldPwd = self.queryOne("SELECT pwd FROM ((SELECT email, pwd FROM NUSHStudent) UNION (SELECT email, pwd FROM NUSHTeacher)) everyone WHERE email = %s", (email, )).get("pwd", "")
        if(oldPw != oldPwd):
            return {"response": "Current Password is not correct!"}
        if(self.isStudent(email)):
            self.execute("UPDATE NUSHStudent SET pwd = %s WHERE email = %s", (newPw, email))
        else:
            self.execute("UPDATE NUSHTeacher SET pwd = %s WHERE email = %s", (newPw, email))
        return {"response": "Success!"}
        
    
        
    # ==================================== GETTER FUNCTIONALITY ====================================
    
    def institute(self, instId):
        return self.queryOne("SELECT * FROM Institution WHERE instId = %s", (instId, ))
    
    def NUSHTeacher(self, email):
        teacher = self.queryOne("SELECT email, name, pfp, isAdmin, deptId FROM NUSHTeacher WHERE email = %s", (email, ))
        if(teacher): teacher["pfp"] = base64.b64encode(teacher.get("pfp", b'')).decode("utf-8") if teacher.get("pfp", b'') != None else ""
        return teacher
    
    def ext_teacher(self, email):
        query = "SELECT email, name, schId FROM ExternalTeacher WHERE email = %s"
        return self.queryOne(query, (email, ))
    
    def teacher(self, email):
        if(self.isNUSHTeacher(email)): return self.NUSHTeacher(email)
        else: return self.ext_teacher(email)
    
    def NUSHStudent(self, email):
        query = "SELECT email, name, about, gradYear, nush_sid, pfp FROM NUSHStudent NATURAL INNER JOIN Student WHERE email = %s"
        student = self.queryOne(query, (email, ))
        if(student): student["pfp"] = base64.b64encode(student.get("pfp", b'')).decode("utf-8") if student.get("pfp", b'') != None else ""
        return student
    
    def ext_student(self, email):
        query = "SELECT email, name, emergencyEmail FROM ExternalStudent NATURAL INNER JOIN Student WHERE email = %s"
        ext_student = self.queryOne(query, (email, ))
        if(ext_student):
            ext_teacher = self.ext_teacher(ext_student.get("emergencyEmail", ""))
            # we want the external teacher email and name + the institution
            return {
                **ext_student,
                "teacherName": ext_teacher.get("name", ""),
                "schId": ext_teacher.get("schId", "")
            }
        return ext_student
    
    def student(self, email):
        return self.NUSHStudent(email) if self.isNUSHStudent(email) else self.ext_student(email)
        
    def mentor(self, email):
        query = "SELECT email, name FROM ResearchMentor where email = %s"
        mentor = self.queryOne(query, (email,))
        query = "SELECT * FROM Works_At NATURAL INNER JOIN Institution WHERE mentorEmail = %s"
        jobs = self.queryAll(query, (email, ))
        return { **mentor, "jobs": jobs }
    
    def event(self, eventId, year):
        query = "SELECT * FROM ResearchEvent WHERE eventId=%s AND year=%s"
        event = self.queryOne(query, (eventId, year))
        event["awardTypes"] = [i["awardType"] for i in self.queryAll("SELECT awardType FROM AwardTypes WHERE eventId=%s AND year=%s", (eventId, year))] if(event["isCompetition"]) else []
        instIds = self.queryAll("SELECT instId FROM Organises WHERE eventId = %s and year = %s", (eventId, year))
        event["organisers"] = [self.institute(instId["instId"]) for instId in instIds]
        event["submissions"] = self.submissions(eventId, year)
        return event

    def project(self, pcode):
        # print(pcode)
        project = self.queryOne("SELECT * FROM Project WHERE pcode = %s", (pcode, ))
        if not project: return None
        # print(project)
        project["members"] = self.projectMembers(pcode)
        project["teacher"] = self.NUSHTeacher(project["teacherEmail"])
        project["reportPdf"] = base64.b64encode(project.get("reportPdf", b'')).decode("utf-8") if project.get("reportPdf", b'') != None else ""
        project["mentors"] = self.mentorsByProject(pcode)
        del project["teacherEmail"]
        return project
    
    def submission(self, eventId, year, code):
        event = self.queryOne("SELECT name, about, isCompetition, isConference, start_date, end_date FROM ResearchEvent WHERE eventId = %s AND year = %s", (eventId, year, ))
        submission = self.queryOne("SELECT * FROM Submission where eventId=%s AND year=%s AND code=%s", (eventId, year, code))    # returns None if no match found.
        if not(submission): return submission
        pcodes  = self.queryAll("SELECT distinct pcode FROM Submits where eventId=%s AND year=%s AND code=%s", (eventId, year, code))
        submission["projects"] = removeNulls([self.project(pcode["pcode"]) for pcode in pcodes if pcode])
        authors = self.queryAll("SELECT distinct studentEmail FROM Submits where eventId=%s AND year=%s AND code=%s", (eventId, year, code))
        submission["members"] = removeNulls([self.student(email["studentEmail"]) for email in authors if email])
        submission["accs"] = self.accBySubmission(eventId, year, code)
        return {**event, **submission}
    
    def strongSubmissions(self, email):
        query = "SELECT distinct eventId, year, code FROM Submits WHERE studentEmail = %s"
        codes = removeNulls(self.queryAll(query, (email, )))
        return removeNulls([self.submission(**kw) for kw in codes])
    
    
        
    # ==================================== CREATE FUNCTIONALITY ====================================
    
    def createExternalStudent(self, email, name, teacherEmail, teacherName, instId):
        if self.NUSHStudent(email): # Student is already in
            return
        
        if not self.ext_teacher(teacherEmail): # Teacher is not in
            self.execute("INSERT INTO ExternalTeacher (email, name, schId) VALUES (%s,%s)", (teacherEmail, teacherName, instId))
        
        self.execute("INSERT INTO Student (email, name) VALUES (%s, %s)", (email, name))
        self.execute("INSERT INTO ExternalStudent (email, emergencyEmail) VALUES (%s, %s)", (email, teacherEmail))
    
    def createSubmission(self, eventId, year, code, subTitle, subAbstract, pcodes, authorEmails):
        # print(eventId, year, code)
        query = "INSERT INTO Submission(eventId, year, code, subTitle, subAbstract) VALUES (%s, %s, %s, %s, %s)"
        self.execute(query, (eventId, year, code, subTitle, subAbstract), commit=False)
        # print(pcodes)
        # print(authorEmails)
        query = "INSERT INTO Submits(eventId, year, code, studentEmail, pcode) VALUES (%s, %s, %s, %s, %s)"
        self.executemany(query, [
            (eventId, year, code, email, pcode) for (email, pcode) in itertools.product(authorEmails, pcodes)
        ])
        return self.submission(eventId, year, code)
    
    def createResearchEvent(
        self, eventId, year, name, start_date, end_date,
        format, about, isCompetition, isConference,
        organisers, awardTypes, confDoi
    ):
        query = "INSERT INTO ResearchEvent(eventId, year, name, start_date, end_date, format, about, isCompetition, isConference, confDoi) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        self.execute(query, (
            eventId, year, name, start_date, end_date,
            format, about, isCompetition, isConference, confDoi
        ), commit=False)
        self.executemany("INSERT INTO AwardTypes(eventId, year, awardType) VALUES (%s, %s, %s)", [
            (eventId, year, awardType) for awardType in awardTypes
        ], commit=False)
        self.executemany("INSERT INTO Organises(eventId, year, instId) VALUES (%s, %s, %s)", [
            (eventId, year, instId) for instId in organisers
        ])
        return self.event(eventId, year)
    
    def createProject(
        self, pcode, year, deptId, title, abstract, teacherEmail, authorEmails
    ):
        query = "INSERT INTO Project(pcode, year, deptId, title, abstract, teacherEmail) VALUES (%s, %s, %s, %s, %s, %s)"
        self.execute(query, (
            pcode, year, deptId, title, abstract, teacherEmail
        ), commit=False)
        self.executemany("INSERT INTO Works_On(studentEmail, pcode) VALUES (%s, %s)", [
            (authorEmail, pcode) for authorEmail in authorEmails
        ])
        return self.project(pcode)

    # ==================================== UPDATE FUNCTIONALITY ====================================
    
    def addStudentsToProject(self, emails, pcode):
        emails = [email for email in emails if not self.queryOne("SELECT studentEmail FROM Works_On WHERE studentEmail = %s AND pcode = %s", (email, pcode))]
        self.executemany("INSERT INTO Works_On (studentEmail, pcode) VALUES (%s, %s)", [(email, pcode) for email in emails])
    
    def addStudentsToSubmission(self, emails, eventId, year, code):
        pcodes = [i["pcode"] for i in removeNulls(self.queryAll("SELECT distinct pcode FROM Submits WHERE eventId = %s AND year = %s AND code = %s", (eventId, year, code)))]
        print(pcodes)
        emails = [email for email in emails if not self.queryOne("SELECT distinct studentEmail FROM Submits WHERE studentEmail = %s AND eventId = %s AND year = %s AND code = %s", (email, eventId, year, code))]
        self.executemany("INSERT INTO Submits (studentEmail, pcode, eventId, year, code) VALUES (%s, %s, %s, %s, %s)", [
            (email, pcode, eventId, year, code) for email, pcode in itertools.product(emails, pcodes)
        ])
    
    def updateSubmission(self, eventId, year, code, subTitle, subAbstract):
        print(eventId, year, code)
        query = "UPDATE Submission SET subTitle = %s, subAbstract = %s WHERE eventId = %s AND year = %s AND code = %s"
        self.execute(query, (subTitle, subAbstract, eventId, year, code))
        res = self.submission(eventId, year, code)
        print(res)
        print(repr(res))
        return res
    
    def updateResearchEvent(
        self, eventId, year, name, start_date, end_date,
        format, about, isCompetition, isConference,
        organisers, awardTypes, confDoi
    ):
        query = "UPDATE ResearchEvent SET name = %s, start_date = %s, end_date = %s, format = %s, about = %s, isCompetition = %s, isConference = %s, confDoi = %s WHERE eventId = %s AND year = %s"
        self.execute(query, (
            name, start_date, end_date, format, about, 
            isCompetition, isConference, confDoi, eventId, year
        ), commit=False)
        self.execute("DELETE FROM AwardTypes WHERE eventId = %s AND year = %s", (eventId, year), commit=False)
        self.executemany("INSERT INTO AwardTypes(eventId, year, awardType) VALUES (%s, %s, %s)", [
            (eventId, year, awardType) for awardType in awardTypes
        ], commit=False)
        self.execute("DELETE FROM Organises WHERE eventId = %s AND year = %s", (eventId, year), commit=False)
        self.executemany("INSERT INTO Organises(eventId, year, instId) VALUES (%s, %s, %s)", [
            (eventId, year, instId) for instId in organisers
        ])
        return self.event(eventId, year)

    # ==================================== DELETE FUNCTIONALITY ====================================
    
    def removeStudentFromProject(self, email, pcode):
        query = "DELETE FROM Works_On WHERE studentEmail = %s AND pcode = %s"
        self.execute(query, (email, pcode, ))
        return self.project(pcode)

    def removeStudentFromSubmission(self, email, eventId, year, code):
        query = "DELETE FROM Submits WHERE studentEmail = %s AND eventId = %s AND year = %s AND code = %s"
        self.execute(query, (email, eventId, year, code, ))
        return self.submission(eventId, year, code)

    def deleteProject(self, pcode):
        query = "DELETE FROM Project WHERE pcode = %s"
        try:
            self.execute(query, (pcode,))
            return {"result": True, "message": "Project Deleted Successfully!"}
        except Exception as e:
            return {"result": False, "message": str(e)}

    def deleteSubmission(self, eventId, year, code):
        query = "DELETE FROM Submission WHERE eventId = %s AND year = %s AND code = %s"
        try:
            self.execute(query, (eventId, year, code))
            return {"result": True, "message": "Submission Deleted Successfully!"}
        except Exception as e:
            return {"result": False, "message": str(e)}

    

    
    # ==================================== SEARCH FUNCTIONALITY ====================================
    
    def searchSchools(self):
        return self.queryAll("SELECT instId, name FROM Institution WHERE isSchool = TRUE")
    
    def searchOrganisers(self):
        return self.queryAll("SELECT instId, name FROM Institution WHERE isOrganiser = TRUE")
    
    def searchAllStudents(self):
        query = "SELECT email, name FROM ExternalStudent NATURAL INNER JOIN Student"
        external_students = [{**i, 'pfp': ''} for i in self.queryAll(query)]
        query = "SELECT email, name, pfp FROM NUSHStudent NATURAL INNER JOIN Student"
        students = self.queryAll(query)
        for student in students:
            if(student): student["pfp"] = base64.b64encode(student.get("pfp", b'')).decode("utf-8") if student.get("pfp", b'') != None else ""
        return list(students) + list(external_students)
    
    def searchAllTeachers(self):
        query = "SELECT email, name, pfp FROM NUSHTeacher"
        students = self.queryAll(query)
        for student in students:
            if(student): student["pfp"] = base64.b64encode(student.get("pfp", b'')).decode("utf-8") if student.get("pfp", b'') != None else ""
        return students
    
    def events(self):
        query = "SELECT eventId, year, name, about, isConference, isCompetition, start_date, end_date FROM ResearchEvent"
        return self.queryAll(query)
    
    def best_students(self, email):
        query = "SELECT studentEmail FROM Works_On NATURAL INNER JOIN Project WHERE teacherEmail = %s GROUP BY teacherEmail, studentEmail ORDER BY COUNT(studentEmail) DESC LIMIT 5"
        studentEmails = self.queryAll(query, (email, ))
        return [self.student(email["studentEmail"]) for email in studentEmails]
    
    def teacherProjects(self, email):
        query = "SELECT pcode FROM Project WHERE teacherEmail = %s"
        pcodes = self.queryAll(query, (email, ))
        return [self.project(pcode["pcode"]) for pcode in pcodes]
    
    def extTeacherStudents(self, email):
        query = "SELECT email FROM ExternalStudent WHERE emergencyEmail = %s LIMIT 5"
        emails = self.queryAll(query, (email, ))
        return [self.ext_student(email["email"]) for email in emails]
        
    def _processAcc(self, result):
        if result["isAward"]:
            return {
                "accId": result.get("accId", ""),
                "name": result.get("name", ""),
                "prize": result.get("prize", "")
            }
        else:
            return self.queryOne("SELECT accId, pubTitle, doi FROM Publication WHERE accId = %s", (result.get("accId", ""), ))
    
    def accBySubmission(self, eventId, year, code):
        # print("you chose", eventId, year, code) # , pubTitle, doi
        query = "SELECT accId, isAward, name, prize FROM Accomplishment WHERE eventId = %s AND year = %s AND code = %s"
        results = self.queryAll(query, (eventId, year, code, ))
        return removeNulls([self._processAcc(result) for result in results])
    
    def submissionsByProject(self, pcode):
        query = "SELECT * FROM Submits WHERE pcode = %s"
        submission_query_pairs = self.queryAll(query, (pcode, ))
        query = "SELECT distinct eventId, year, code, subTitle, subAbstract FROM Submits NATURAL JOIN Submission WHERE pcode = %s"
        submissions = self.queryAll(query, (pcode, ))
        return [
            {
                **submission, 
                "members": [
                    self.student(i.get("studentEmail", ""))
                    for i in submission_query_pairs 
                    if i.get("eventId", "") == submission.get("eventId", "") 
                    and i.get("year", 0) == submission.get("year", 0) 
                    and i.get("code", "") == submission.get("code", "")
                ],
                "accs": self.accBySubmission(submission.get("eventId", ""), submission.get("year", 0), submission.get("code", ""))
            }
            for submission in submissions
        ]
    
    def submissionsByUser(self, email):
        query = "SELECT * FROM Submits WHERE studentEmail = %s"
        submission_query_pairs = self.queryAll(query, (email, ))
        query = "SELECT distinct eventId, year, code, subTitle, subAbstract FROM Submits NATURAL JOIN Submission WHERE studentEmail = %s"
        submissions = self.queryAll(query, (email, ))
        return [
            {
                **submission,
                "projects": [
                    i.get("pcode", "")
                    for i in submission_query_pairs 
                    if i.get("eventId", "") == submission.get("eventId", "") 
                    and i.get("year", 0) == submission.get("year", 0) 
                    and i.get("code", "") == submission.get("code", "")
                ],
                # "accs": self.accBySubmission(submission.get("eventId", ""), submission.get("year", 0), submission.get("code", ""))
            }
            for submission in submissions
        ]
        
    def mentorsByProject(self, pcode): 
        query = "SELECT email FROM ResearchMentor INNER JOIN Mentors ON ResearchMentor.email = Mentors.mentorEmail WHERE pcode = %s"
        emails = self.queryAll(query, (pcode, ))
        return [self.mentor(email["email"]) for email in emails]
    
    
    def projectsByMentor(self, email):
        query = "SELECT pcode FROM ResearchMentor INNER JOIN Mentors ON ResearchMentor.email = Mentors.mentorEmail WHERE email = %s"
        pcodes = self.queryAll(query, (email, ))
        return [self.project(pcode["pcode"]) for pcode in pcodes]
    
    def mentorStudents(self, email):
        query = "SELECT studentEmail FROM Works_On NATURAL INNER JOIN Project NATURAL INNER JOIN Mentors WHERE mentorEmail = %s GROUP BY mentorEmail, studentEmail ORDER BY COUNT(studentEmail) DESC LIMIT 5"
        emails = self.queryAll(query, (email, ))
        return [self.student(email["studentEmail"]) for email in emails]
    
    def _processSub(self, eventId, year, sub):
        if not sub: return sub
        query = "SELECT distinct pcode FROM Submits WHERE eventId = %s and year = %s and code = %s"
        pcode = self.queryOne(query, (eventId, year, sub["code"]))
        pcode = pcode if pcode else dict(pcode="")
        students = removeNulls([self.student(email["studentEmail"]) for email in self.queryAll("SELECT distinct studentEmail FROM Submits WHERE eventId = %s and year = %s and code = %s", (eventId, year, sub["code"]))])
        return {**sub, **pcode, "members": students}
    
    def submissions(self, eventId, year):
        query = "SELECT distinct code, subTitle title FROM Submission WHERE eventId = %s AND year = %s"
        submissions = self.queryAll(query, (eventId, year, ))
        return [self._processSub(eventId, year, submission) for submission in submissions]
    
    def otherProjects(self, email):
        query = "SELECT pcode FROM Project p WHERE %s <> ALL (SELECT studentEmail FROM Works_On wo where wo.pcode = p.pcode)"
        pcodes = [i["pcode"] for i in self.queryAll(query, (email, ))]
        random.shuffle(pcodes)
        return removeNulls([self.project(pcode) for pcode in pcodes if pcode])
    
    def otherEvents(self, email):
        query = "SELECT eventId, year FROM ResearchEvent re WHERE %s <> ALL (SELECT studentEmail FROM Submits s WHERE s.eventId = re.eventId AND s.year = re.year)"
        ids = self.queryAll(query, (email, ))
        return removeNulls([self.event(**id) for id in ids])
    
    def projectMembers(self, pcode):
        query = "SELECT studentEmail email FROM Works_On WHERE pcode = %s"
        return [self.NUSHStudent(i["email"]) if self.isNUSHStudent(i["email"]) else self.ext_student(i["email"]) for i in self.queryAll(query, (pcode,))]
    
    def studentProjects(self, email):
        pcodes = self.queryAll("SELECT pcode FROM Works_On WHERE studentEmail = %s", (email, ))
        return removeNulls([self.project(pcode["pcode"]) for pcode in pcodes])
    
    def coauthors(self, email):
        query = "SELECT other.studentEmail email, COUNT(self.pcode) num FROM Works_On self, Works_On other WHERE self.pcode = other.pcode AND self.studentEmail = %s AND other.studentEmail <> self.studentEmail GROUP BY other.studentEmail ORDER BY COUNT(self.pcode) DESC LIMIT 5"
        return [{**(i[0]), "count": i[1]} for i in [(self.NUSHStudent(i["email"]), i["num"]) for i in self.queryAll(query, (email,)) if self.isStudent(i["email"])] if i[0]]
    
    def projectByTeacher(self, email):
        query = "SELECT pcode FROM Project WHERE teacherEmail = %s"
        codes = self.queryAll(query, (email, ))
        return [self.project(code) for code in codes]
    
    def updateProject(self, pcode, title, abstract, reportPdf):
        # print(reportPdf)
        reportPdf = convertB64toBytes(reportPdf) if reportPdf != None else ""
        # print(reportPdf)
        query = "UPDATE Project SET title = %s, abstract = %s, reportPdf = %s WHERE pcode = %s"
        self.execute(query, (title, abstract, reportPdf, pcode))
        return self.project(pcode)
    
    def updateStudent(self, email, pfp, about):
        pfp = convertB64toBytes(pfp) if pfp != None else "" # convert base64 to bytes object if needed.
        query = "UPDATE NUSHStudent SET pfp = %s, about = %s WHERE email = %s"
        self.execute(query, (pfp, about, email))
        return self.NUSHStudent(email)
    
    def _processJourn(self, journal):
        query = "SELECT instId FROM PublishedBy WHERE issn = %s"
        instIds = [i["instId"] for i in self.queryAll(query, (journal["issn"], )) if i]
        institutes = removeNulls([self.institute(instId) for instId in instIds])
        
        publications = self.queryAll("SELECT pubTitle title, doi, url FROM Publication where journISSN = %s", (journal["issn"], ))
        
        return {
            **journal,
            "institutes": institutes,
            "publications": publications
        }
    
    def journals(self):
        query = "SELECT issn, name FROM Journal"
        return [self._processJourn(it) for it in self.queryAll(query)]
    
    # ================================== AGGREGATION FUNCTIONALITY =================================
    def projectStats(self, email):
        query = "SELECT year, COUNT(pcode) count FROM Works_On NATURAL JOIN Project WHERE studentEmail = %s GROUP BY year ORDER BY year"
        stats = list(self.queryAll(query, (email, )))
        
        if len(stats) == 0: return stats
        minYear = min([i["year"] for i in stats])
        maxYear = max([i["year"] for i in stats])
        
        for year in range(minYear, maxYear+1):
            if any([i["year"] == year for i in stats]): continue;
            stats.append({ "year": year, "count": 0 })
        
        return sorted(stats, key=lambda i: i["year"])
            
    def submissionStats(self, email):
        query = "SELECT year, COUNT(pcode) count FROM Submits WHERE studentEmail = %s GROUP BY year ORDER BY year"
        stats = list(self.queryAll(query, (email, )))
        if len(stats) == 0: return stats
        
        minYear = min([i["year"] for i in stats])
        maxYear = max([i["year"] for i in stats])
        
        for year in range(minYear, maxYear+1):
            if any([i["year"] == year for i in stats]): continue;
            stats.append({ "year": year, "count": 0 })
        
        return sorted(stats, key=lambda i: i["year"])
    
    def awardStats(self, email):
        query = "SELECT year, COUNT(accId) count FROM Accomplishment NATURAL INNER JOIN Submits WHERE studentEmail = %s AND isAward = true GROUP BY year ORDER BY year"
        stats = list(self.queryAll(query, (email, )))
        if len(stats) == 0: return stats
        
        minYear = min([i["year"] for i in stats])
        maxYear = max([i["year"] for i in stats])
        
        for year in range(minYear, maxYear+1):
            if any([i["year"] == year for i in stats]): continue;
            stats.append({ "year": year, "count": 0 })
        
        return sorted(stats, key=lambda i: i["year"])
    
    def projectAwardStats(self, email):
        query = "SELECT pcode, count, title, year FROM (SELECT pcode, COUNT(accId) count FROM Accomplishment NATURAL INNER JOIN Submits WHERE studentEmail = %s AND isAward = true GROUP BY pcode ORDER BY pcode) agg NATURAL INNER JOIN Project p ORDER BY year, pcode"
        stats = list(self.queryAll(query, (email, )))
        return stats
    
    
    
        
        