from peewee import *

database = MySQLDatabase('arxiv', **{'charset': 'utf8', 'sql_mode': 'PIPES_AS_CONCAT', 'use_unicode': True, 'host': 'arxiv-nush-database-1', 'user': 'root', 'password': 'admin'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Researchevent(BaseModel):
    about = CharField(null=True)
    conf_doi = CharField(column_name='confDoi', null=True)
    end_date = DateTimeField()
    event_id = CharField(column_name='eventId')
    format = CharField(null=True)
    is_competition = IntegerField(column_name='isCompetition', constraints=[SQL("DEFAULT 0")])
    is_conference = IntegerField(column_name='isConference', constraints=[SQL("DEFAULT 0")])
    name = CharField()
    start_date = DateTimeField()
    year = IntegerField()

    class Meta:
        table_name = 'researchevent'
        indexes = (
            (('event_id', 'year'), True),
        )
        primary_key = CompositeKey('event_id', 'year')

class Submission(BaseModel):
    code = CharField()
    event = ForeignKeyField(column_name='eventId', field='event_id', model=Researchevent)
    sub_abstract = CharField(column_name='subAbstract')
    sub_title = CharField(column_name='subTitle')
    year = ForeignKeyField(backref='researchevent_year_set', column_name='year', field='year', model=Researchevent)

    class Meta:
        table_name = 'submission'
        indexes = (
            (('event', 'year', 'code'), True),
        )
        primary_key = CompositeKey('code', 'event', 'year')

class Accomplishment(BaseModel):
    acc_id = AutoField(column_name='accId')
    code = ForeignKeyField(column_name='code', field='code', model=Submission, null=True)
    event = ForeignKeyField(backref='submission_event_set', column_name='eventId', field='event', model=Submission, null=True)
    is_award = IntegerField(column_name='isAward', constraints=[SQL("DEFAULT 0")])
    name = CharField(null=True)
    prize = CharField(null=True)
    year = ForeignKeyField(backref='submission_year_set', column_name='year', field='year', model=Submission, null=True)

    class Meta:
        table_name = 'accomplishment'
        indexes = (
            (('event', 'year', 'code'), False),
        )

class Awardtypes(BaseModel):
    award_type = CharField(column_name='awardType')
    event = ForeignKeyField(column_name='eventId', field='event_id', model=Researchevent)
    year = ForeignKeyField(backref='researchevent_year_set', column_name='year', field='year', model=Researchevent)

    class Meta:
        table_name = 'awardtypes'
        indexes = (
            (('event', 'year', 'award_type'), True),
        )
        primary_key = CompositeKey('award_type', 'event', 'year')

class Department(BaseModel):
    dept_id = CharField(column_name='deptId', primary_key=True)
    name = CharField(constraints=[SQL("DEFAULT ''")])

    class Meta:
        table_name = 'department'

class Student(BaseModel):
    email = CharField(primary_key=True)
    name = CharField(null=True)

    class Meta:
        table_name = 'student'

class Institution(BaseModel):
    address = CharField(constraints=[SQL("DEFAULT ''")])
    inst_id = CharField(column_name='instId', primary_key=True)
    is_institute = IntegerField(column_name='isInstitute', constraints=[SQL("DEFAULT 0")])
    is_organiser = IntegerField(column_name='isOrganiser', constraints=[SQL("DEFAULT 0")])
    is_publisher = IntegerField(column_name='isPublisher', constraints=[SQL("DEFAULT 0")])
    is_school = IntegerField(column_name='isSchool', constraints=[SQL("DEFAULT 0")])
    name = CharField(constraints=[SQL("DEFAULT ''")])

    class Meta:
        table_name = 'institution'

class Externalteacher(BaseModel):
    email = CharField(primary_key=True)
    name = CharField(null=True)
    sch = ForeignKeyField(column_name='schId', field='inst_id', model=Institution, null=True)

    class Meta:
        table_name = 'externalteacher'

class Externalstudent(BaseModel):
    email = ForeignKeyField(column_name='email', field='email', model=Student, primary_key=True)
    emergency_email = ForeignKeyField(column_name='emergencyEmail', field='email', model=Externalteacher, null=True)

    class Meta:
        table_name = 'externalstudent'

class Journal(BaseModel):
    issn = AutoField()
    name = CharField()

    class Meta:
        table_name = 'journal'

class Nushteacher(BaseModel):
    dept = ForeignKeyField(column_name='deptId', field='dept_id', model=Department, null=True)
    email = CharField(primary_key=True)
    is_admin = IntegerField(column_name='isAdmin', constraints=[SQL("DEFAULT 0")])
    is_mentor = IntegerField(column_name='isMentor', constraints=[SQL("DEFAULT 0")])
    name = CharField(constraints=[SQL("DEFAULT ''")])
    pfp = TextField(null=True)
    pwd = CharField(null=True)

    class Meta:
        table_name = 'nushteacher'

class Project(BaseModel):
    abstract = CharField(null=True)
    dept = ForeignKeyField(column_name='deptId', field='dept_id', model=Department, null=True)
    pcode = CharField(primary_key=True)
    report_pdf = TextField(column_name='reportPdf', null=True)
    teacher_email = ForeignKeyField(column_name='teacherEmail', field='email', model=Nushteacher, null=True)
    title = CharField()
    year = IntegerField(null=True)

    class Meta:
        table_name = 'project'

class Researchmentor(BaseModel):
    email = CharField(primary_key=True)
    name = CharField(null=True)

    class Meta:
        table_name = 'researchmentor'

class Mentors(BaseModel):
    mentor_email = ForeignKeyField(column_name='mentorEmail', field='email', model=Researchmentor)
    pcode = ForeignKeyField(column_name='pcode', field='pcode', model=Project)

    class Meta:
        table_name = 'mentors'
        primary_key = False

class Nushstudent(BaseModel):
    about = CharField(null=True)
    email = ForeignKeyField(column_name='email', field='email', model=Student, primary_key=True)
    grad_year = IntegerField(column_name='gradYear', null=True)
    nush_sid = CharField(null=True)
    pfp = TextField(null=True)
    pwd = CharField(null=True)

    class Meta:
        table_name = 'nushstudent'

class Organises(BaseModel):
    event = ForeignKeyField(column_name='eventId', field='event_id', model=Researchevent)
    inst = ForeignKeyField(column_name='instId', field='inst_id', model=Institution)
    year = ForeignKeyField(backref='researchevent_year_set', column_name='year', field='year', model=Researchevent)

    class Meta:
        table_name = 'organises'
        indexes = (
            (('event', 'year', 'inst'), True),
        )
        primary_key = CompositeKey('event', 'inst', 'year')

class Projectcontinuation(BaseModel):
    next_pcode = ForeignKeyField(column_name='nextPcode', field='pcode', model=Project)
    prev_pcode = ForeignKeyField(backref='project_prev_pcode_set', column_name='prevPcode', field='pcode', model=Project)

    class Meta:
        table_name = 'projectcontinuation'
        primary_key = False

class Publication(BaseModel):
    acc = ForeignKeyField(column_name='accId', field='acc_id', model=Accomplishment, primary_key=True)
    doi = CharField(null=True)
    is_journal = IntegerField(column_name='isJournal', constraints=[SQL("DEFAULT 0")])
    journ_issn = ForeignKeyField(column_name='journISSN', field='issn', model=Journal, null=True)
    pub_title = CharField(column_name='pubTitle')
    url = CharField(null=True)

    class Meta:
        table_name = 'publication'

class Publishedby(BaseModel):
    inst = ForeignKeyField(column_name='instId', field='inst_id', model=Institution)
    issn = ForeignKeyField(column_name='issn', field='issn', model=Journal)

    class Meta:
        table_name = 'publishedby'
        indexes = (
            (('issn', 'inst'), True),
        )
        primary_key = CompositeKey('inst', 'issn')

class Submits(BaseModel):
    code = ForeignKeyField(column_name='code', field='code', model=Submission)
    event = ForeignKeyField(backref='submission_event_set', column_name='eventId', field='event', model=Submission)
    pcode = ForeignKeyField(column_name='pcode', field='pcode', model=Project)
    student_email = ForeignKeyField(column_name='studentEmail', field='email', model=Student)
    year = ForeignKeyField(backref='submission_year_set', column_name='year', field='year', model=Submission)

    class Meta:
        table_name = 'submits'
        indexes = (
            (('event', 'year', 'code'), False),
            (('student_email', 'pcode', 'event', 'year', 'code'), True),
        )
        primary_key = CompositeKey('code', 'event', 'pcode', 'student_email', 'year')

class WorksAt(BaseModel):
    dept = CharField(null=True)
    inst = ForeignKeyField(column_name='instId', field='inst_id', model=Institution)
    mentor_email = ForeignKeyField(column_name='mentorEmail', field='email', model=Researchmentor)
    office_addr = CharField(column_name='officeAddr', null=True)
    role = CharField(null=True)

    class Meta:
        table_name = 'works_at'
        indexes = (
            (('mentor_email', 'inst'), True),
        )
        primary_key = CompositeKey('inst', 'mentor_email')

class WorksOn(BaseModel):
    pcode = ForeignKeyField(column_name='pcode', field='pcode', model=Project)
    student_email = ForeignKeyField(column_name='studentEmail', field='email', model=Student)

    class Meta:
        table_name = 'works_on'
        indexes = (
            (('student_email', 'pcode'), True),
        )
        primary_key = CompositeKey('pcode', 'student_email')

