import base64

from sqlalchemy import select, union, update
from util import remove_nulls
import random
import itertools
from sqlalchemy.orm import Session, Bundle
from . import models, schemas
from functools import cache

@cache
def get_default_pfp() -> bytes:
    with open("assets/default.png", "rb") as f:
        pfp = f.read()

    return pfp 
    
# ==================================== EXISTS FUNCTIONALITY ====================================
    
def is_student(db: Session, email: str) -> bool:
    return db.execute(select(models.Student).filter(models.Student.email == email)).first() != None
    
def is_mentor(db: Session, email: str) -> bool:
    return db.execute(select(models.ResearchMentor).filter(models.ResearchMentor.email == email)).first() != None
    
def is_nush_teacher(db: Session, email: str) -> bool:
    return db.execute(select(models.NUSHTeacher).filter(models.NUSHTeacher.email == email)).first() != None
    
def is_nush_student(db: Session, email: str) -> bool:
    return db.execute(select(models.NUSHStudent).filter(models.NUSHStudent.email == email)).first() != None


# ================================ AUTHENTICATION FUNCTIONALITY ================================

def student_login(db: Session, email: str, pwd: str) -> bool:
    return db.execute(select(models.NUSHStudent).filter(models.NUSHStudent.email == email, models.NUSHStudent.pwd == pwd)).first() != None

def teacher_login(db: Session, email: str, pwd: str) -> bool:
    return db.execute(select(models.NUSHTeacher).filter(models.NUSHTeacher.email == email, models.NUSHTeacher.pwd == pwd)).first() != None
    
# FIXME
def login(db: Session, email: str, password: str) -> schemas.LoginResult:
    is_student = is_nush_student(db, email)
    
    if is_student:
        is_student_auth = student_login(db, email, password)
        if is_student_auth:
            return schemas.LoginResult(result=True, user=get_nush_student(db, email), message="Logged in successfully!")
        return schemas.LoginResult(result=False, message="Incorrect password provided!")
        
    is_teacher = is_nush_teacher(db, email)

    if is_teacher:
        is_teacher_auth = teacher_login(db, email, password)
        if is_teacher_auth:
            return schemas.LoginResult(result=True, user=get_nush_teacher(db, email), message="Logged in successfully!")
        return schemas.LoginResult(result=False, message="Incorrect password provided!")
        
    return schemas.LoginResult(result=False, message="Account does not exist!")
    
def register_student(
    db: Session, email: str, password: str, name: str, grad_year: int
) -> schemas.RegisterStudentResult:
    if not(email.endswith("@nushigh.edu.sg") and email[0] == 'h' and email[1:8].isnumeric()):
        return schemas.RegisterStudentResult(result=False, error="Please give a valid email of form `hXXXXXXX@nushigh.edu.sg`.")

    # additional grad year check
    join_yr = int(email[1:3])
    join_lvl = int(email[3])
    if (grad_year % 100) != ((join_yr + 6 - join_lvl) % 100):
        return schemas.RegisterStudentResult(result=False, error="Graduation year appears invalid.")
    
    existing = is_nush_student(db, email)
    if existing:
        if(student_login(db, email, password)):
            return schemas.RegisterStudentResult(result=True, user=get_nush_student(db, email), message="Account already exists, successfully logged in with details provided.")
        return schemas.RegisterStudentResult(result=False, error="Account already exists!")
    try:
        db_nush_student = models.NUSHStudent(
            email=email, pwd=password, pfp=get_default_pfp(), grad_year=grad_year, nush_sid=email[1:8]
        )
        db_student = models.Student(email=email, name=name, nush_student=db_nush_student)
        db.add(db_student)
        db.commit()

        return schemas.RegisterStudentResult(result=True, user=get_nush_student(db, email), message="Registered Successfully!")
    except Exception as e:
        return schemas.RegisterStudentResult(result=False, error=str(e))
    
def register_teacher(
    db: Session, email: str, password: str, name: str, dept_id: str
) -> schemas.RegisterTeacherResult:
    if not(email.endswith("@nushigh.edu.sg")):
        return schemas.RegisterTeacherResult(result=False, error="Please give a valid email ending with `@nushigh.edu.sg`.")
    existing = is_nush_teacher(db, email)
    if existing:
        if(teacher_login(db, email, password)):
            return schemas.RegisterTeacherResult(result=True, user=get_nush_teacher(db, email), message="Account already exists, successfully logged in with details provided.")
        return schemas.RegisterTeacherResult(result=False, error="Account already exists!")
    try:
        db_nush_teacher = models.NUSHTeacher(
            email=email, pwd=password, name=name, pfp=get_default_pfp(), dept_id=dept_id
        )
        db.add(db_nush_teacher)
        db.commit()

        return schemas.RegisterTeacherResult(result=True, user=get_nush_teacher(db, email), message="Registered Successfully!")
    except Exception as e:
        return schemas.RegisterTeacherResult(result=False, error=str(e))

def change_password(db: Session, email: str, old_pwd: str, new_pwd: str) -> schemas.ChangePasswordResult:
    union_std_tcr = union(select(models.NUSHTeacher.email, models.NUSHTeacher.pwd), select(models.NUSHStudent.email, models.NUSHStudent.pwd)).subquery()
    stmt = select(union_std_tcr).where(union_std_tcr.c.email == "h1910090@nushigh.edu.sg")
    pwd_in_db = db.execute(stmt).one().pwd

    if(old_pwd != pwd_in_db):
        return schemas.ChangePasswordResult(response="Current password is not correct!")
    
    if(is_student(db, email)):
        db.execute(update(models.NUSHStudent).where(models.NUSHStudent.email == email).values(pwd=new_pwd))
    else:
        db.execute(update(models.NUSHTeacher).where(models.NUSHTeacher.email == email).values(pwd=new_pwd))
    
    return schemas.ChangePasswordResult(response="Success!")
    

    
# ==================================== GETTER FUNCTIONALITY ====================================

def get_institution(db: Session, inst_id: str) -> models.Institution | None:
    return db.execute(select(models.Institution).filter(models.Institution.inst_id == inst_id)).scalar_one_or_none()

def get_nush_teacher_raw(db: Session, email: str) -> models.NUSHTeacher | None:
    return db.execute(select(models.NUSHTeacher).filter(models.NUSHTeacher.email == email)).scalar_one_or_none()

def get_nush_teacher(db: Session, email: str) -> schemas.NUSHTeacher | None:
    teacher = get_nush_teacher_raw(db, email)
    if not teacher: return None
    pfp = base64.b64encode(teacher.pfp_bytes).decode("ascii") if teacher.pfp_bytes != None else ""
    ret_teacher = schemas.NUSHTeacher.model_validate(teacher)
    ret_teacher.pfp = pfp
    return ret_teacher

def get_ext_teacher(db: Session, email: str) -> models.ExternalTeacher | None:
    return db.execute(select(models.ExternalTeacher).filter(models.ExternalTeacher.email == email)).scalar_one_or_none()

def get_teacher(db: Session, email: str) -> models.NUSHTeacher | models.ExternalTeacher | None:
    if(is_nush_teacher(db, email)): return get_nush_teacher_raw(db, email)
    else: return get_ext_teacher(db, email)

def get_nush_student_raw(db: Session, email: str) -> models.NUSHStudent | None:
    return db.execute(select(models.NUSHStudent).filter(models.NUSHStudent.email == email)).scalar_one_or_none()

def get_nush_student(db: Session, email: str) -> schemas.NUSHStudent | None:
    student = get_nush_student_raw(db, email)
    if not student: return None
    pfp = base64.b64encode(student.pfp_bytes).decode("ascii") if student.pfp_bytes != None else ""
    ret_student = schemas.NUSHStudent.model_validate(student)
    ret_student.pfp = pfp
    return ret_student

def get_ext_student(db: Session, email: str) -> schemas.ExternalStudent | None:
    stmt = select(models.ExternalStudent, models.Student, models.ExternalTeacher).join(models.Student).join(models.ExternalTeacher).filter(models.ExternalStudent.email == email)
    row = db.execute(stmt).one_or_none()
    if not row:
        return None

    # we want the external teacher email and name + the institution
    return schemas.ExternalStudent(
        email=row.ExternalStudent.email,
        name=row.Student.name,
        emergency_email=row.ExternalStudent.emergency_email,
        teacher_name=row.ExternalTeacher.name,
        sch_id=row.ExternalTeacher.sch_id
    )

def get_student(db: Session, email: str) -> schemas.NUSHStudent | schemas.ExternalStudent | None:
    return get_nush_student(db, email) if is_nush_student(db, email) else get_ext_student(db, email)
    
def get_mentor(db: Session, email: str) -> schemas.ResearchMentor | None:
    mentor = db.execute(select(models.ResearchMentor).filter(models.ResearchMentor.email == email)).scalar_one_or_none()
    if not mentor:
        return None
    return schemas.ResearchMentor(
        email=mentor.email,
        name=mentor.name,
        jobs=[schemas.WorksAt.model_validate(job) for job in mentor.workplaces]
    )

def event(self, eventId, year):
    query = "SELECT * FROM ResearchEvent WHERE eventId=%s AND year=%s"
    event = queryOne(query, (eventId, year))
    event["awardTypes"] = [i["awardType"] for i in queryAll("SELECT awardType FROM AwardTypes WHERE eventId=%s AND year=%s", (eventId, year))] if(event["isCompetition"]) else []
    instIds = queryAll("SELECT instId FROM Organises WHERE eventId = %s and year = %s", (eventId, year))
    event["organisers"] = [get_institution(instId["instId"]) for instId in instIds]
    event["submissions"] = submissions(eventId, year)
    return event

def project(self, pcode):
    # print(pcode)
    project = queryOne("SELECT * FROM Project WHERE pcode = %s", (pcode, ))
    if not project: return None
    # print(project)
    project["members"] = projectMembers(pcode)
    project["teacher"] = get_nush_teacher(project["teacherEmail"])
    project["reportPdf"] = base64.b64encode(project.get("reportPdf", b'')).decode("utf-8") if project.get("reportPdf", b'') != None else ""
    project["mentors"] = mentorsByProject(pcode)
    del project["teacherEmail"]
    return project

def submission(self, eventId, year, code):
    event = queryOne("SELECT name, about, isCompetition, isConference, start_date, end_date FROM ResearchEvent WHERE eventId = %s AND year = %s", (eventId, year, ))
    submission = queryOne("SELECT * FROM Submission where eventId=%s AND year=%s AND code=%s", (eventId, year, code))    # returns None if no match found.
    if not(submission): return submission
    pcodes  = queryAll("SELECT distinct pcode FROM Submits where eventId=%s AND year=%s AND code=%s", (eventId, year, code))
    submission["projects"] = remove_nulls([project(pcode["pcode"]) for pcode in pcodes if pcode])
    authors = queryAll("SELECT distinct studentEmail FROM Submits where eventId=%s AND year=%s AND code=%s", (eventId, year, code))
    submission["members"] = remove_nulls([get_student(email["studentEmail"]) for email in authors if email])
    submission["accs"] = accBySubmission(eventId, year, code)
    return {**event, **submission}

def strongSubmissions(self, email):
    query = "SELECT distinct eventId, year, code FROM Submits WHERE studentEmail = %s"
    codes = remove_nulls(queryAll(query, (email, )))
    return remove_nulls([submission(**kw) for kw in codes])


    
# ==================================== CREATE FUNCTIONALITY ====================================

def createExternalStudent(self, email, name, teacherEmail, teacherName, instId):
    if get_nush_student(email): # Student is already in
        return
    
    if not get_ext_teacher(teacherEmail): # Teacher is not in
        execute("INSERT INTO ExternalTeacher (email, name, schId) VALUES (%s,%s, %s)", (teacherEmail, teacherName, instId))
    
    execute("INSERT INTO Student (email, name) VALUES (%s, %s)", (email, name))
    execute("INSERT INTO ExternalStudent (email, emergencyEmail) VALUES (%s, %s)", (email, teacherEmail))

def createSubmission(self, eventId, year, code, subTitle, subAbstract, pcodes, authorEmails):
    # print(eventId, year, code)
    query = "INSERT INTO Submission(eventId, year, code, subTitle, subAbstract) VALUES (%s, %s, %s, %s, %s)"
    execute(query, (eventId, year, code, subTitle, subAbstract), commit=False)
    # print(pcodes)
    # print(authorEmails)
    query = "INSERT INTO Submits(eventId, year, code, studentEmail, pcode) VALUES (%s, %s, %s, %s, %s)"
    executemany(query, [
        (eventId, year, code, email, pcode) for (email, pcode) in itertools.product(authorEmails, pcodes)
    ])
    return submission(eventId, year, code)

def createResearchEvent(
    self, eventId, year, name, start_date, end_date,
    format, about, isCompetition, isConference,
    organisers, awardTypes, confDoi
):
    query = "INSERT INTO ResearchEvent(eventId, year, name, start_date, end_date, format, about, isCompetition, isConference, confDoi) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    execute(query, (
        eventId, year, name, start_date, end_date,
        format, about, isCompetition, isConference, confDoi
    ), commit=False)
    executemany("INSERT INTO AwardTypes(eventId, year, awardType) VALUES (%s, %s, %s)", [
        (eventId, year, awardType) for awardType in awardTypes
    ], commit=False)
    executemany("INSERT INTO Organises(eventId, year, instId) VALUES (%s, %s, %s)", [
        (eventId, year, instId) for instId in organisers
    ])
    return event(eventId, year)

def createProject(
    self, pcode, year, deptId, title, abstract, teacherEmail, authorEmails
):
    query = "INSERT INTO Project(pcode, year, deptId, title, abstract, teacherEmail) VALUES (%s, %s, %s, %s, %s, %s)"
    execute(query, (
        pcode, year, deptId, title, abstract, teacherEmail
    ), commit=False)
    executemany("INSERT INTO Works_On(studentEmail, pcode) VALUES (%s, %s)", [
        (authorEmail, pcode) for authorEmail in authorEmails
    ])
    return project(pcode)

# ==================================== UPDATE FUNCTIONALITY ====================================

def addStudentsToProject(self, emails, pcode):
    emails = [email for email in emails if not queryOne("SELECT studentEmail FROM Works_On WHERE studentEmail = %s AND pcode = %s", (email, pcode))]
    executemany("INSERT INTO Works_On (studentEmail, pcode) VALUES (%s, %s)", [(email, pcode) for email in emails])

def addStudentsToSubmission(self, emails, eventId, year, code):
    pcodes = [i["pcode"] for i in remove_nulls(queryAll("SELECT distinct pcode FROM Submits WHERE eventId = %s AND year = %s AND code = %s", (eventId, year, code)))]
    print(pcodes)
    emails = [email for email in emails if not queryOne("SELECT distinct studentEmail FROM Submits WHERE studentEmail = %s AND eventId = %s AND year = %s AND code = %s", (email, eventId, year, code))]
    executemany("INSERT INTO Submits (studentEmail, pcode, eventId, year, code) VALUES (%s, %s, %s, %s, %s)", [
        (email, pcode, eventId, year, code) for email, pcode in itertools.product(emails, pcodes)
    ])

def updateSubmission(self, eventId, year, code, subTitle, subAbstract):
    print(eventId, year, code)
    query = "UPDATE Submission SET subTitle = %s, subAbstract = %s WHERE eventId = %s AND year = %s AND code = %s"
    execute(query, (subTitle, subAbstract, eventId, year, code))
    res = submission(eventId, year, code)
    print(res)
    print(repr(res))
    return res

def updateResearchEvent(
    self, eventId, year, name, start_date, end_date,
    format, about, isCompetition, isConference,
    organisers, awardTypes, confDoi
):
    query = "UPDATE ResearchEvent SET name = %s, start_date = %s, end_date = %s, format = %s, about = %s, isCompetition = %s, isConference = %s, confDoi = %s WHERE eventId = %s AND year = %s"
    execute(query, (
        name, start_date, end_date, format, about, 
        isCompetition, isConference, confDoi, eventId, year
    ), commit=False)
    execute("DELETE FROM AwardTypes WHERE eventId = %s AND year = %s", (eventId, year), commit=False)
    executemany("INSERT INTO AwardTypes(eventId, year, awardType) VALUES (%s, %s, %s)", [
        (eventId, year, awardType) for awardType in awardTypes
    ], commit=False)
    execute("DELETE FROM Organises WHERE eventId = %s AND year = %s", (eventId, year), commit=False)
    executemany("INSERT INTO Organises(eventId, year, instId) VALUES (%s, %s, %s)", [
        (eventId, year, instId) for instId in organisers
    ])
    return event(eventId, year)

# ==================================== DELETE FUNCTIONALITY ====================================

def removeStudentFromProject(self, email, pcode):
    query = "DELETE FROM Works_On WHERE studentEmail = %s AND pcode = %s"
    execute(query, (email, pcode, ))
    return project(pcode)

def removeStudentFromSubmission(self, email, eventId, year, code):
    query = "DELETE FROM Submits WHERE studentEmail = %s AND eventId = %s AND year = %s AND code = %s"
    execute(query, (email, eventId, year, code, ))
    return submission(eventId, year, code)

def deleteProject(self, pcode):
    query = "DELETE FROM Project WHERE pcode = %s"
    try:
        execute(query, (pcode,))
        return {"result": True, "message": "Project Deleted Successfully!"}
    except Exception as e:
        return {"result": False, "message": str(e)}

def deleteSubmission(self, eventId, year, code):
    query = "DELETE FROM Submission WHERE eventId = %s AND year = %s AND code = %s"
    try:
        execute(query, (eventId, year, code))
        return {"result": True, "message": "Submission Deleted Successfully!"}
    except Exception as e:
        return {"result": False, "message": str(e)}




# ==================================== SEARCH FUNCTIONALITY ====================================

def searchSchools(self):
    return queryAll("SELECT instId, name FROM Institution WHERE isSchool = TRUE")

def searchOrganisers(self):
    return queryAll("SELECT instId, name FROM Institution WHERE isOrganiser = TRUE")

def searchAllStudents(self):
    query = "SELECT email, name FROM ExternalStudent NATURAL INNER JOIN Student"
    external_students = [{**i, 'pfp': ''} for i in queryAll(query)]
    query = "SELECT email, name, pfp FROM NUSHStudent NATURAL INNER JOIN Student"
    students = queryAll(query)
    for student in students:
        if(student): student["pfp"] = base64.b64encode(student.get("pfp", b'')).decode("utf-8") if student.get("pfp", b'') != None else ""
    return list(students) + list(external_students)

def searchAllTeachers(self):
    query = "SELECT email, name, pfp FROM NUSHTeacher"
    students = queryAll(query)
    for student in students:
        if(student): student["pfp"] = base64.b64encode(student.get("pfp", b'')).decode("utf-8") if student.get("pfp", b'') != None else ""
    return students

def events(self):
    query = "SELECT eventId, year, name, about, isConference, isCompetition, start_date, end_date FROM ResearchEvent"
    return queryAll(query)

def best_students(self, email):
    query = "SELECT studentEmail FROM Works_On NATURAL INNER JOIN Project WHERE teacherEmail = %s GROUP BY teacherEmail, studentEmail ORDER BY COUNT(studentEmail) DESC LIMIT 5"
    studentEmails = queryAll(query, (email, ))
    return [get_student(email["studentEmail"]) for email in studentEmails]

def teacherProjects(self, email):
    query = "SELECT pcode FROM Project WHERE teacherEmail = %s"
    pcodes = queryAll(query, (email, ))
    return [project(pcode["pcode"]) for pcode in pcodes]

def extTeacherStudents(self, email):
    query = "SELECT email FROM ExternalStudent WHERE emergencyEmail = %s LIMIT 5"
    emails = queryAll(query, (email, ))
    return [get_ext_student(email["email"]) for email in emails]
    
def _processAcc(self, result):
    if result["isAward"]:
        return {
            "accId": result.get("accId", ""),
            "name": result.get("name", ""),
            "prize": result.get("prize", "")
        }
    else:
        return queryOne("SELECT accId, pubTitle, doi FROM Publication WHERE accId = %s", (result.get("accId", ""), ))

def accBySubmission(self, eventId, year, code):
    # print("you chose", eventId, year, code) # , pubTitle, doi
    query = "SELECT accId, isAward, name, prize FROM Accomplishment WHERE eventId = %s AND year = %s AND code = %s"
    results = queryAll(query, (eventId, year, code, ))
    return remove_nulls([_processAcc(result) for result in results])

def submissionsByProject(self, pcode):
    query = "SELECT * FROM Submits WHERE pcode = %s"
    submission_query_pairs = queryAll(query, (pcode, ))
    query = "SELECT distinct eventId, year, code, subTitle, subAbstract FROM Submits NATURAL JOIN Submission WHERE pcode = %s"
    submissions = queryAll(query, (pcode, ))
    return [
        {
            **submission, 
            "members": [
                get_student(i.get("studentEmail", ""))
                for i in submission_query_pairs 
                if i.get("eventId", "") == submission.get("eventId", "") 
                and i.get("year", 0) == submission.get("year", 0) 
                and i.get("code", "") == submission.get("code", "")
            ],
            "accs": accBySubmission(submission.get("eventId", ""), submission.get("year", 0), submission.get("code", ""))
        }
        for submission in submissions
    ]

def submissionsByUser(self, email):
    query = "SELECT * FROM Submits WHERE studentEmail = %s"
    submission_query_pairs = queryAll(query, (email, ))
    query = "SELECT distinct eventId, year, code, subTitle, subAbstract FROM Submits NATURAL JOIN Submission WHERE studentEmail = %s"
    submissions = queryAll(query, (email, ))
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
            # "accs": accBySubmission(submission.get("eventId", ""), submission.get("year", 0), submission.get("code", ""))
        }
        for submission in submissions
    ]
    
def mentorsByProject(self, pcode): 
    query = "SELECT email FROM ResearchMentor INNER JOIN Mentors ON ResearchMentor.email = Mentors.mentorEmail WHERE pcode = %s"
    emails = queryAll(query, (pcode, ))
    return [get_mentor(email["email"]) for email in emails]


def projectsByMentor(self, email):
    query = "SELECT pcode FROM ResearchMentor INNER JOIN Mentors ON ResearchMentor.email = Mentors.mentorEmail WHERE email = %s"
    pcodes = queryAll(query, (email, ))
    return [project(pcode["pcode"]) for pcode in pcodes]

def mentorStudents(self, email):
    query = "SELECT studentEmail FROM Works_On NATURAL INNER JOIN Project NATURAL INNER JOIN Mentors WHERE mentorEmail = %s GROUP BY mentorEmail, studentEmail ORDER BY COUNT(studentEmail) DESC LIMIT 5"
    emails = queryAll(query, (email, ))
    return [get_student(email["studentEmail"]) for email in emails]

def _processSub(self, eventId, year, sub):
    if not sub: return sub
    query = "SELECT distinct pcode FROM Submits WHERE eventId = %s and year = %s and code = %s"
    pcode = queryOne(query, (eventId, year, sub["code"]))
    pcode = pcode if pcode else dict(pcode="")
    students = remove_nulls([get_student(email["studentEmail"]) for email in queryAll("SELECT distinct studentEmail FROM Submits WHERE eventId = %s and year = %s and code = %s", (eventId, year, sub["code"]))])
    return {**sub, **pcode, "members": students}

def submissions(self, eventId, year):
    query = "SELECT distinct code, subTitle title FROM Submission WHERE eventId = %s AND year = %s"
    submissions = queryAll(query, (eventId, year, ))
    return [_processSub(eventId, year, submission) for submission in submissions]

def otherProjects(self, email):
    query = "SELECT pcode FROM Project p WHERE %s <> ALL (SELECT studentEmail FROM Works_On wo where wo.pcode = p.pcode)"
    pcodes = [i["pcode"] for i in queryAll(query, (email, ))]
    random.shuffle(pcodes)
    return remove_nulls([project(pcode) for pcode in pcodes if pcode])

def otherEvents(self, email):
    query = "SELECT eventId, year FROM ResearchEvent re WHERE %s <> ALL (SELECT studentEmail FROM Submits s WHERE s.eventId = re.eventId AND s.year = re.year)"
    ids = queryAll(query, (email, ))
    return remove_nulls([event(**id) for id in ids])

def projectMembers(self, pcode):
    query = "SELECT studentEmail email FROM Works_On WHERE pcode = %s"
    return [get_nush_student(i["email"]) if is_nush_student(i["email"]) else get_ext_student(i["email"]) for i in queryAll(query, (pcode,))]

def studentProjects(self, email):
    pcodes = queryAll("SELECT pcode FROM Works_On WHERE studentEmail = %s", (email, ))
    return remove_nulls([project(pcode["pcode"]) for pcode in pcodes])

def coauthors(self, email):
    query = "SELECT other.studentEmail email, COUNT(pcode) num FROM Works_On self, Works_On other WHERE pcode = other.pcode AND studentEmail = %s AND other.studentEmail <> studentEmail GROUP BY other.studentEmail ORDER BY COUNT(pcode) DESC LIMIT 5"
    return [{**(i[0]), "count": i[1]} for i in [(get_nush_student(i["email"]), i["num"]) for i in queryAll(query, (email,)) if is_student(i["email"])] if i[0]]

def projectByTeacher(self, email):
    query = "SELECT pcode FROM Project WHERE teacherEmail = %s"
    codes = queryAll(query, (email, ))
    return [project(code) for code in codes]

def updateProject(self, pcode, title, abstract, reportPdf):
    # print(reportPdf)
    reportPdf = base64.b64decode(reportPdf) if reportPdf != None else ""
    # print(reportPdf)
    query = "UPDATE Project SET title = %s, abstract = %s, reportPdf = %s WHERE pcode = %s"
    execute(query, (title, abstract, reportPdf, pcode))
    return project(pcode)

def updateStudent(self, email, pfp, about):
    pfp = base64.b64decode(pfp) if pfp != None else "" # convert base64 to bytes object if needed.
    query = "UPDATE NUSHStudent SET pfp = %s, about = %s WHERE email = %s"
    execute(query, (pfp, about, email))
    return get_nush_student(email)

def _processJourn(self, journal):
    query = "SELECT instId FROM PublishedBy WHERE issn = %s"
    instIds = [i["instId"] for i in queryAll(query, (journal["issn"], )) if i]
    institutes = remove_nulls([get_institution(instId) for instId in instIds])
    
    publications = queryAll("SELECT pubTitle title, doi, url FROM Publication where journISSN = %s", (journal["issn"], ))
    
    return {
        **journal,
        "institutes": institutes,
        "publications": publications
    }

def journals(self):
    query = "SELECT issn, name FROM Journal"
    return [_processJourn(it) for it in queryAll(query)]

# ================================== AGGREGATION FUNCTIONALITY =================================
def projectStats(self, email):
    query = "SELECT year, COUNT(pcode) count FROM Works_On NATURAL JOIN Project WHERE studentEmail = %s GROUP BY year ORDER BY year"
    stats = list(queryAll(query, (email, )))
    
    if len(stats) == 0: return stats
    minYear = min([i["year"] for i in stats])
    maxYear = max([i["year"] for i in stats])
    
    for year in range(minYear, maxYear+1):
        if any([i["year"] == year for i in stats]): continue;
        stats.append({ "year": year, "count": 0 })
    
    return sorted(stats, key=lambda i: i["year"])
        
def submissionStats(self, email):
    query = "SELECT year, COUNT(pcode) count FROM Submits WHERE studentEmail = %s GROUP BY year ORDER BY year"
    stats = list(queryAll(query, (email, )))
    if len(stats) == 0: return stats
    
    minYear = min([i["year"] for i in stats])
    maxYear = max([i["year"] for i in stats])
    
    for year in range(minYear, maxYear+1):
        if any([i["year"] == year for i in stats]): continue;
        stats.append({ "year": year, "count": 0 })
    
    return sorted(stats, key=lambda i: i["year"])

def awardStats(self, email):
    query = "SELECT year, COUNT(accId) count FROM Accomplishment NATURAL INNER JOIN Submits WHERE studentEmail = %s AND isAward = true GROUP BY year ORDER BY year"
    stats = list(queryAll(query, (email, )))
    if len(stats) == 0: return stats
    
    minYear = min([i["year"] for i in stats])
    maxYear = max([i["year"] for i in stats])
    
    for year in range(minYear, maxYear+1):
        if any([i["year"] == year for i in stats]): continue;
        stats.append({ "year": year, "count": 0 })
    
    return sorted(stats, key=lambda i: i["year"])

def projectAwardStats(self, email):
    query = "SELECT pcode, count, title, year FROM (SELECT pcode, COUNT(accId) count FROM Accomplishment NATURAL INNER JOIN Submits WHERE studentEmail = %s AND isAward = true GROUP BY pcode ORDER BY pcode) agg NATURAL INNER JOIN Project p ORDER BY year, pcode"
    stats = list(queryAll(query, (email, )))
    return stats



    
    
