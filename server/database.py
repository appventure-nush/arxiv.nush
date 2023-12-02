import base64
from datetime import date
from typing import Collection, Optional, Sequence

from sqlalchemy import label, select, tuple_, union, update
from util import many_many_map, not_none, remove_nulls, first_from_bulk, search_index
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
    stmt = select(union_std_tcr).where(union_std_tcr.c.email == email)
    pwd_in_db = db.execute(stmt).one().pwd

    if(old_pwd != pwd_in_db):
        return schemas.ChangePasswordResult(response="Current password is not correct!")
    
    if(is_student(db, email)):
        db.execute(update(models.NUSHStudent).where(models.NUSHStudent.email == email).values(pwd=new_pwd))
    else:
        db.execute(update(models.NUSHTeacher).where(models.NUSHTeacher.email == email).values(pwd=new_pwd))
    
    return schemas.ChangePasswordResult(response="Success!")
    
# ==================================== GETTER FUNCTIONALITY ====================================

# every getter has 2 versions:
# bulk_get - bulk gets schema. returns lists of tuple of (input, schema)
# get - returns schema for 1 item. Internally uses bulk_get.

# == Institution ==

def bulk_get_institutions(db: Session, inst_ids: Collection[str]) -> list[tuple[str, schemas.Institution]]:
    return [
        (inst.inst_id, schemas.Institution.model_validate(inst)) 
        for inst in db.scalars(
            select(models.Institution).filter(models.Institution.inst_id.in_(inst_ids))
    )]

def get_institution(db: Session, inst_id: str) -> schemas.Institution | None:
    return first_from_bulk(bulk_get_institutions(db, [inst_id]))

# == NUSH Teacher ==

def bulk_get_nush_teachers(db: Session, emails: Collection[str]) -> list[tuple[str, schemas.NUSHTeacher]]:
    res: list[tuple[str, schemas.NUSHTeacher]] = []

    for teacher in db.scalars(select(models.NUSHTeacher).filter(models.NUSHTeacher.email.in_(emails))):
        pfp = base64.b64encode(teacher.pfp_bytes).decode("ascii") if teacher.pfp_bytes != None else ""
        ret_teacher = schemas.NUSHTeacher.model_validate(teacher)
        ret_teacher.pfp = pfp
        res.append((teacher.email, ret_teacher))

    return res

def get_nush_teacher(db: Session, email: str) -> schemas.NUSHTeacher | None:
    return first_from_bulk(bulk_get_nush_teachers(db, [email]))

# == External Teacher ==

def bulk_get_ext_teachers(db: Session, emails: Collection[str]) -> list[tuple[str, schemas.ExternalTeacher]]:
    return [(teacher.email, schemas.ExternalTeacher.model_validate(teacher)) for teacher in db.scalars(select(models.ExternalTeacher).filter(models.ExternalTeacher.email.in_(emails)))]

def get_ext_teacher(db: Session, email: str) -> schemas.ExternalTeacher | None:
    return first_from_bulk(bulk_get_ext_teachers(db, [email]))

# == Any Teacher ==

def bulk_get_teachers(db: Session, email: Collection[str]) -> list[tuple[str, schemas.NUSHTeacher | schemas.ExternalTeacher]]:
    res: list[tuple[str, schemas.NUSHTeacher | schemas.ExternalTeacher]] = []
    res.extend(bulk_get_nush_teachers(db, email))
    res.extend(bulk_get_ext_teachers(db, email)) # assume there's no overlap
    return res
                                                                                          
def get_teacher(db: Session, email: str) -> schemas.NUSHTeacher | schemas.ExternalTeacher | None:
    return first_from_bulk(bulk_get_teachers(db, [email]))

# == NUSH Student ==

def bulk_get_nush_students(db: Session, emails: Collection[str]) -> list[tuple[str, schemas.NUSHStudent]]:
    res: list[tuple[str, schemas.NUSHStudent]] = []

    for student in db.scalars(select(models.NUSHStudent).filter(models.NUSHStudent.email.in_(emails))):
        pfp = base64.b64encode(student.pfp_bytes).decode("ascii") if student.pfp_bytes != None else ""
        ret_student = schemas.NUSHStudent.model_validate(student)
        ret_student.pfp = pfp
        res.append((student.email, ret_student))

    return res

def get_nush_student(db: Session, email: str) -> schemas.NUSHStudent | None:
    return first_from_bulk(bulk_get_nush_students(db, [email]))

# == External Student ==

def bulk_get_ext_students(db: Session, emails: Collection[str]) -> list[tuple[str, schemas.ExternalStudent]]:
    stmt = (
        select(
            models.ExternalStudent.email, 
            models.ExternalStudent.emergency_email,
            models.Student.name,
        )
        .join(models.Student)
        .filter(models.ExternalStudent.email.in_(emails))
    )
    external_students = db.execute(stmt).all()

    external_teacher_emails = [s.emergency_email for s in external_students if s.emergency_email is not None]
    external_teachers = dict(bulk_get_ext_teachers(db, external_teacher_emails))

    res: list[tuple[str, schemas.ExternalStudent]] = [(row.email, schemas.ExternalStudent.model_validate(row)) for row in external_students]

    for _, student in res:
        if student.emergency_email is not None and student.emergency_email in external_teachers:
            student.teacher_name = external_teachers[student.emergency_email].name
            student.sch_id = external_teachers[student.emergency_email].sch_id

    return res

def get_ext_student(db: Session, email: str) -> schemas.ExternalStudent | None:
    return first_from_bulk(bulk_get_ext_students(db, [email]))

# == Any Student ==

def bulk_get_students(db: Session, emails: Collection[str]) -> list[tuple[str, schemas.NUSHStudent | schemas.ExternalStudent]]:
    res: list[tuple[str, schemas.NUSHStudent | schemas.ExternalStudent]] = []
    res.extend(bulk_get_nush_students(db, emails))
    res.extend(bulk_get_ext_students(db, emails)) # assume there's no overlap
    return res

def get_student(db: Session, email: str) -> schemas.NUSHStudent | schemas.ExternalStudent | None:
    return first_from_bulk(bulk_get_students(db, [email]))

# == Research Mentor ==

def bulk_get_mentors(db: Session, emails: Collection[str]) -> list[tuple[str, schemas.ResearchMentor]]:
    stmt = (
        select(models.ResearchMentor, models.WorksAt)
        .join(models.WorksAt)
        .filter(models.ResearchMentor.email.in_(emails))
    )

    # collect them together
    last_mentor: Optional[models.ResearchMentor] = None
    res: list[tuple[str, schemas.ResearchMentor]] = []
    for row in db.execute(stmt):
        if last_mentor != row.ResearchMentor:
            last_mentor = row.ResearchMentor
            assert last_mentor != None
            res.append((last_mentor.email, schemas.ResearchMentor(
                email=last_mentor.email,
                name=last_mentor.name,
                jobs=[]
            )))
        res[-1][1].jobs.append(schemas.WorksAt.model_validate(row.WorksAt))

    return res

    
def get_mentor(db: Session, email: str) -> schemas.ResearchMentor | None:
    return first_from_bulk(bulk_get_mentors(db, [email]))

# == Research Event ==

def bulk_get_events(db: Session, event_ids: Collection[str], years: Collection[int]) -> list[tuple[int, schemas.ResearchEvent]]:
    events = db.scalars(select(models.ResearchEvent).filter(tuple_(models.ResearchEvent.event_id, models.ResearchEvent.year).in_(zip(event_ids, years)))).all()
    res: list[tuple[int, schemas.ResearchEvent]] = [(event.num_event_id, schemas.ResearchEvent.model_validate(event)) for event in events]

    idx_map = {event.num_event_id: i for i, event in enumerate(events)}

    # award types
    for award in db.scalars(select(models.AwardTypes).filter(models.AwardTypes.num_event_id.in_(idx_map.keys()))):
        res[idx_map[award.num_event_id]][1].award_types.append(award.award_type)

    # institutions
    stmt = (
        select(models.Organises.inst_id, models.Organises.num_event_id)
        .where(models.Organises.num_event_id.in_(idx_map.keys()))
    )

    inst_map = many_many_map(db.execute(stmt).tuples().all()) # inst_id -> [num_event_id]

    for inst_id, institution in bulk_get_institutions(db, inst_map.keys()):
        for num_event_id in inst_map[inst_id]:
            res[idx_map[num_event_id]][1].organisers.append(institution)

    # submissions
    stmt = (
        select(models.ResearchEventSubmission.sub_id, models.ResearchEventSubmission.num_event_id)
        .filter(models.ResearchEventSubmission.num_event_id.in_(idx_map.keys()))
    )

    sub_map = many_many_map(db.execute(stmt).tuples().all()) # sub_id -> [num_event_id]

    for sub_id, submission in bulk_get_submissions_by_sub_id(db, sub_map.keys()):
        for num_event_id in sub_map[sub_id]:
            res[idx_map[num_event_id]][1].submissions.append(submission)

    return res

def get_event(db: Session, event_id: str, year: int) -> schemas.ResearchEvent | None:
    return first_from_bulk(bulk_get_events(db, [event_id], [year]))

# == Project ==

def bulk_get_projects(db: Session, p_codes: Collection[str]) -> list[tuple[str, schemas.Project]]:
    projects = db.scalars(select(models.Project).filter(models.Project.p_code.in_(p_codes))).all()
    res: list[tuple[str, schemas.Project]] = [(project.p_code, schemas.Project.model_validate(project)) for project in projects]

    idx_map = {project.p_code: i for i, project in enumerate(projects)}

    # members
    stmt = (
        select(models.WorksOn.student_email, models.WorksOn.p_code)
        .where(models.WorksOn.p_code.in_(idx_map.keys()))
    )

    member_map = many_many_map(db.execute(stmt).tuples().all()) # student_email -> [p_code]
    students = bulk_get_students(db, member_map.keys())

    for student_email, student in students:
        for p_code in member_map[student_email]:
            res[idx_map[p_code]][1].members.append(student)

    # teacher
    teacher_map = dict(bulk_get_nush_teachers(db, [project.teacher_email for project in projects if project.teacher_email]))

    for project in projects:
        if project.teacher_email and project.teacher_email in teacher_map:
            res[idx_map[project.p_code]][1].teacher = teacher_map[project.teacher_email]

    # report pdf
    for project in projects:
        if project.report_pdf_bytes:
            res[idx_map[project.p_code]][1].report_pdf = base64.b64encode(project.report_pdf_bytes).decode("utf-8")

    # mentors
    stmt = (
        select(models.ResearchMentor.email, models.Project.p_code)
        .join(models.Mentors).join(models.Project)
        .filter(models.Project.p_code.in_(idx_map.keys()))
    )

    mentor_map = many_many_map(db.execute(stmt).tuples().all()) # email -> [p_code]
    mentors = bulk_get_mentors(db, mentor_map.keys())

    for email, mentor in mentors:
        for p_code in mentor_map[email]:
            res[idx_map[p_code]][1].mentors.append(mentor)

    return res


def get_project(db: Session, p_code: str) -> schemas.Project | None:
    return first_from_bulk(bulk_get_projects(db, [p_code]))

# == Submission ==

def bulk_get_submissions_by_sub_id(db: Session, ids: Collection[int]) -> list[tuple[int, schemas.ResearchEventSubmission]]:
    submissions = db.execute(
        select(models.ResearchEventSubmission, models.ResearchEvent)
        .join(models.ResearchEvent)
        .filter(models.ResearchEventSubmission.sub_id.in_(ids))
    ).tuples().all()
    res: list[tuple[int, schemas.ResearchEventSubmission]] = [
        (sub[0].sub_id, 
         schemas.ResearchEventSubmission(
            sub_id=sub[0].sub_id,
            num_event_id=sub[0].num_event_id,
            code=sub[0].code,
            sub_title=sub[0].sub_title,
            sub_abstract=sub[0].sub_abstract,
            event_id=sub[1].event_id,
            year=sub[1].year,
            name=sub[1].name,
            about=sub[1].about,
            is_conference=sub[1].is_conference,
            is_competition=sub[1].is_competition,
            start_date=sub[1].start_date,
            end_date=sub[1].end_date,
         )
        ) for sub in submissions
    ]

    idx_map = {sub[0].sub_id: i for i, sub in enumerate(submissions)}

    # projects
    stmt = (
        select(models.Submits.p_code, models.Submits.sub_id)
        .filter(models.Submits.sub_id.in_(idx_map.keys()))
    )

    project_map = many_many_map(db.execute(stmt).tuples().all()) # p_code -> [sub_id]
    projects = bulk_get_projects(db, project_map.keys())

    for p_code, project in projects:
        for sub_id in project_map[p_code]:
            res[idx_map[sub_id]][1].projects.append(project)

    # members
    stmt = (
        select(models.Submits.student_email, models.Submits.sub_id)
        .filter(models.Submits.sub_id.in_(idx_map.keys()))
    )

    member_map = many_many_map(db.execute(stmt).tuples().all()) # student_email -> [sub_id]
    students = bulk_get_students(db, member_map.keys())

    for student_email, student in students:
        for sub_id in member_map[student_email]:
            res[idx_map[sub_id]][1].members.append(student)

    # accomplishments
    stmt = (
        select(models.Accomplishment)
        .join(models.ResearchEventSubmission)
        .filter(models.ResearchEventSubmission.sub_id.in_(idx_map.keys()))
    )

    for acc in db.scalars(stmt):
        if acc.sub_id:
            res[idx_map[acc.sub_id]][1].accomplishments.append(schemas.Accomplishment.model_validate(acc))

    return res

def bulk_get_submissions(db: Session, event_ids: Collection[str], years: Collection[int], codes: Collection[str]) -> list[tuple[int, schemas.ResearchEventSubmission]]:
    return bulk_get_submissions_by_sub_id(db, db.scalars(
        select(models.ResearchEventSubmission.sub_id)
        .join(models.ResearchEvent)
        .filter(tuple_(models.ResearchEvent.event_id, models.ResearchEvent.year, models.ResearchEventSubmission.code).in_(zip(event_ids, years, codes)))
    ).all())

    
def get_submission(db: Session, event_id: str, year: int, code: str):
    return first_from_bulk(bulk_get_submissions(db, [event_id], [year], [code]))

def get_submission_by_sub_id(db: Session, sub_id: int):
    return first_from_bulk(bulk_get_submissions_by_sub_id(db, [sub_id]))

def get_submissions_by_email(db: Session, email: str) -> list[schemas.ResearchEventSubmission]:
    stmt = (
        select(models.Submits.sub_id)
        .where(models.Submits.student_email == email)
    )
    return list(zip(*bulk_get_submissions_by_sub_id(db, db.execute(stmt).scalars().all())))[1]


    
# ==================================== CREATE FUNCTIONALITY ====================================

def create_external_student(db: Session, email: str, name: str, teacher_email: str, teacher_name: str, inst_id: str) -> None:
    if get_nush_student(db, email): # Student is already in
        return
    
    if not get_ext_teacher(db, teacher_email): # Teacher is not in
        db.add(models.ExternalTeacher(email=teacher_email, name=teacher_name, sch_id=inst_id))
    
    db.add(models.ExternalStudent(email=email, emergency_email=teacher_email))
    db.add(models.Student(email=email, name=name))
    db.commit()

def create_submission(db: Session, num_event_id: int, code: str, sub_title: str, sub_abstract: str, p_codes: Collection[str], author_emails: Collection[str]) -> schemas.ResearchEventSubmission:
    submission = models.ResearchEventSubmission(
        num_event_id=num_event_id,
        code=code,
        sub_title=sub_title,
        sub_abstract=sub_abstract
    )

    db.add(submission)
    db.commit()
    db.refresh(submission)

    db.add_all([
        models.Submits(student_email=email, p_code=p_code, sub_id=submission.sub_id)
        for email, p_code in itertools.product(author_emails, p_codes)
    ])
    db.commit()

    return not_none(get_submission_by_sub_id(db, submission.sub_id))

def create_research_event(
    db: Session, event_id: str, year: int, name: str, start_date: date, end_date: date,
    format: str, about: str, is_competition: bool, is_conference: bool,
    organisers: Collection[str], award_types: Collection[str], conf_doi: str
) -> schemas.ResearchEvent:
    event = models.ResearchEvent(
        event_id=event_id, year=year, name=name, start_date=start_date, end_date=end_date,
        format=format, about=about, is_competition=is_competition, is_conference=is_conference,
        conf_doi=conf_doi
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    
    db.add_all([
        models.Organises(num_event_id=event.num_event_id, inst_id=inst_id)
        for inst_id in organisers
    ])
    db.add_all([
        models.AwardTypes(num_event_id=event.num_event_id, award_type=award_type)
        for award_type in award_types
    ])
    db.commit()

    return not_none(get_event(db, event_id, year))

def create_project(
    db: Session, p_code: str, year: int, dept_id: str, title: str, abstract: str, teacher_email: str, author_emails: Collection[str]
) -> schemas.Project:
    db.add(models.Project(
        p_code=p_code, year=year, dept_id=dept_id, title=title, abstract=abstract, teacher_email=teacher_email
    ))

    db.add_all([
        models.WorksOn(student_email=email, p_code=p_code)
        for email in author_emails
    ])
    
    return not_none(get_project(db, p_code))

# ==================================== UPDATE FUNCTIONALITY ====================================

def add_students_to_project(self, emails, pcode):
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
    res = get_submission(eventId, year, code)
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
    return get_event(eventId, year)

# ==================================== DELETE FUNCTIONALITY ====================================

def removeStudentFromProject(self, email, pcode):
    query = "DELETE FROM Works_On WHERE studentEmail = %s AND pcode = %s"
    execute(query, (email, pcode, ))
    return get_project(pcode)

def removeStudentFromSubmission(self, email, eventId, year, code):
    query = "DELETE FROM Submits WHERE studentEmail = %s AND eventId = %s AND year = %s AND code = %s"
    execute(query, (email, eventId, year, code, ))
    return get_submission(eventId, year, code)

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
    return [get_students_by_email(email["studentEmail"]) for email in studentEmails]

def teacherProjects(self, email):
    query = "SELECT pcode FROM Project WHERE teacherEmail = %s"
    pcodes = queryAll(query, (email, ))
    return [get_project(pcode["pcode"]) for pcode in pcodes]

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
                get_students_by_email(i.get("studentEmail", ""))
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


def projectsByMentor(self, email):
    query = "SELECT pcode FROM ResearchMentor INNER JOIN Mentors ON ResearchMentor.email = Mentors.mentorEmail WHERE email = %s"
    pcodes = queryAll(query, (email, ))
    return [get_project(pcode["pcode"]) for pcode in pcodes]

def mentorStudents(self, email):
    query = "SELECT studentEmail FROM Works_On NATURAL INNER JOIN Project NATURAL INNER JOIN Mentors WHERE mentorEmail = %s GROUP BY mentorEmail, studentEmail ORDER BY COUNT(studentEmail) DESC LIMIT 5"
    emails = queryAll(query, (email, ))
    return [get_students_by_email(email["studentEmail"]) for email in emails]

def _processSub(self, eventId, year, sub):
    if not sub: return sub
    query = "SELECT distinct pcode FROM Submits WHERE eventId = %s and year = %s and code = %s"
    pcode = queryOne(query, (eventId, year, sub["code"]))
    pcode = pcode if pcode else dict(pcode="")
    students = remove_nulls([get_students_by_email(email["studentEmail"]) for email in queryAll("SELECT distinct studentEmail FROM Submits WHERE eventId = %s and year = %s and code = %s", (eventId, year, sub["code"]))])
    return {**sub, **pcode, "members": students}

def submissions(self, eventId, year):
    query = "SELECT distinct code, subTitle title FROM Submission WHERE eventId = %s AND year = %s"
    submissions = queryAll(query, (eventId, year, ))
    return [_processSub(eventId, year, submission) for submission in submissions]

def otherProjects(self, email):
    query = "SELECT pcode FROM Project p WHERE %s <> ALL (SELECT studentEmail FROM Works_On wo where wo.pcode = p.pcode)"
    pcodes = [i["pcode"] for i in queryAll(query, (email, ))]
    random.shuffle(pcodes)
    return remove_nulls([get_project(pcode) for pcode in pcodes if pcode])

def otherEvents(self, email):
    query = "SELECT eventId, year FROM ResearchEvent re WHERE %s <> ALL (SELECT studentEmail FROM Submits s WHERE s.eventId = re.eventId AND s.year = re.year)"
    ids = queryAll(query, (email, ))
    return remove_nulls([get_event(**id) for id in ids])

def get_project_members(db: Session, p_code: str) -> list[schemas.ExternalStudent | schemas.NUSHStudent]:
    res: list[schemas.ExternalStudent | schemas.NUSHStudent] = []

    stmt = (
        select(
            models.ExternalStudent.email, 
            models.ExternalStudent.emergency_email,
            models.Student.name, 
            label("teacher_name", models.ExternalTeacher.name),
            models.ExternalTeacher.sch_id
        ).join(models.Student).join(models.WorksOn).join(models.Project).join(models.ExternalTeacher)
        .filter(models.Project.p_code == p_code)
    )
    
    for row in db.execute(stmt):
        res.append(schemas.ExternalStudent.model_validate(row))

    stmt = (
        select(
            models.NUSHStudent
        ).join(models.Student).join(models.WorksOn).join(models.Project).join(models.ExternalTeacher)
        .filter(models.Project.p_code == p_code)
    )

    for student in db.scalars(stmt):
        pfp = base64.b64encode(student.pfp_bytes).decode("ascii") if student.pfp_bytes != None else ""
        student_ret = schemas.NUSHStudent.model_validate(student)
        student_ret.pfp = pfp
        res.append(student_ret)
    
    return res

def studentProjects(self, email):
    pcodes = queryAll("SELECT pcode FROM Works_On WHERE studentEmail = %s", (email, ))
    return remove_nulls([get_project(pcode["pcode"]) for pcode in pcodes])

def coauthors(self, email):
    query = "SELECT other.studentEmail email, COUNT(pcode) num FROM Works_On self, Works_On other WHERE pcode = other.pcode AND studentEmail = %s AND other.studentEmail <> studentEmail GROUP BY other.studentEmail ORDER BY COUNT(pcode) DESC LIMIT 5"
    return [{**(i[0]), "count": i[1]} for i in [(get_nush_student(i["email"]), i["num"]) for i in queryAll(query, (email,)) if is_student(i["email"])] if i[0]]

def projectByTeacher(self, email):
    query = "SELECT pcode FROM Project WHERE teacherEmail = %s"
    codes = queryAll(query, (email, ))
    return [get_project(code) for code in codes]

def updateProject(self, pcode, title, abstract, reportPdf):
    # print(reportPdf)
    reportPdf = base64.b64decode(reportPdf) if reportPdf != None else ""
    # print(reportPdf)
    query = "UPDATE Project SET title = %s, abstract = %s, reportPdf = %s WHERE pcode = %s"
    execute(query, (title, abstract, reportPdf, pcode))
    return get_project(pcode)

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



    
    
