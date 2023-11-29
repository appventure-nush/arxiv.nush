# generated from pwiz, manually checked
# comments are generated from \dt

from peewee import *

database = PostgresqlDatabase('arxiv', **{'host': 'database', 'user': 'postgres', 'password': 'admin'})

class BaseModel(Model):
    class Meta:
        database = database

"""
Table "arxiv.researchevent"
    Column     |          Type           | Collation | Nullable |                      Default                      
---------------+-------------------------+-----------+----------+---------------------------------------------------
 numeventid    | bigint                  |           | not null | nextval('researchevent_numeventid_seq'::regclass)
 eventid       | character varying(15)   |           | not null | 
 year          | integer                 |           | not null | 
 name          | character varying(100)  |           | not null | 
 about         | character varying(5000) |           |          | 
 start_date    | date                    |           | not null | 
 end_date      | date                    |           | not null | 
 format        | character varying(10)   |           |          | 
 iscompetition | boolean                 |           | not null | false
 isconference  | boolean                 |           | not null | false
 confdoi       | character varying(200)  |           |          | 
Indexes:
    "idx_16464_primary" PRIMARY KEY, btree (numeventid)
    "idx_16464_eventid_2" UNIQUE, btree (eventid, year)
Referenced by:
    TABLE "awardtypes" CONSTRAINT "awardtypes_ibfk_1" FOREIGN KEY (numeventid) REFERENCES researchevent(numeventid) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE "organises" CONSTRAINT "organises_ibfk_3" FOREIGN KEY (numeventid) REFERENCES researchevent(numeventid) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE "submission" CONSTRAINT "submission_ibfk_1" FOREIGN KEY (numeventid) REFERENCES researchevent(numeventid) ON UPDATE CASCADE ON DELETE CASCADE
"""
class ResearchEvent(BaseModel):
    about = CharField(max_length=5000, null=True)
    conf_DOI = CharField(column_name='confdoi', max_length=200, null=True)
    end_date = DateField()
    event_id = CharField(column_name='eventid', max_length=15)
    event_format = CharField(column_name='format', null=True, max_length=10)
    is_competition = BooleanField(column_name="iscompetition", default=False)
    is_conference = BooleanField(column_name="isconference", default=False)
    name = CharField(max_length=100)
    num_event_id = BigAutoField(column_name='numeventid')
    start_date = DateField()
    year = IntegerField()

    class Meta:
        table_name = 'researchevent'
        indexes = (
            (('eventid', 'year'), True),
        )
        schema = 'arxiv'


"""
Table "arxiv.submission"
   Column    |          Type           | Collation | Nullable |                  Default                  
-------------+-------------------------+-----------+----------+-------------------------------------------
 subid       | bigint                  |           | not null | nextval('submission_subid_seq'::regclass)
 numeventid  | bigint                  |           | not null | 
 code        | character varying(20)   |           | not null | 
 subtitle    | character varying(200)  |           | not null | 
 subabstract | character varying(2000) |           | not null | 
Indexes:
    "idx_16479_primary" PRIMARY KEY, btree (subid)
    "idx_16479_numeventid" UNIQUE, btree (numeventid, code)
Foreign-key constraints:
    "submission_ibfk_1" FOREIGN KEY (numeventid) REFERENCES researchevent(numeventid) ON UPDATE CASCADE ON DELETE CASCADE
Referenced by:
    TABLE "accomplishment" CONSTRAINT "accomplishment_ibfk_1" FOREIGN KEY (subid) REFERENCES submission(subid) ON UPDATE CASCADE ON DELETE SET NULL
    TABLE "submits" CONSTRAINT "submits_ibfk_3" FOREIGN KEY (subid) REFERENCES submission(subid) ON UPDATE CASCADE ON DELETE CASCADE
"""
class Submission(BaseModel):
    code = CharField(max_length=20)
    num_event_id = ForeignKeyField(column_name='numeventid', field='numeventid', model=ResearchEvent)
    sub_abstract = CharField(column_name='subabstract', max_length=2000)
    sub_id = BigAutoField(column_name='subid')
    sub_title = CharField(column_name='subtitle', max_length=200)

    class Meta:
        table_name = 'submission'
        indexes = (
            (('numeventid', 'code'), True),
        )
        schema = 'arxiv'

"""
Table "arxiv.accomplishment"
 Column  |          Type          | Collation | Nullable | Default 
---------+------------------------+-----------+----------+---------
 accid   | integer                |           | not null | 
 isaward | boolean                |           | not null | false
 name    | character varying(100) |           |          | 
 prize   | character varying(100) |           |          | 
 subid   | bigint                 |           |          | 
Indexes:
    "idx_16386_primary" PRIMARY KEY, btree (accid)
    "idx_16386_subid" btree (subid)
Foreign-key constraints:
    "accomplishment_ibfk_1" FOREIGN KEY (subid) REFERENCES submission(subid) ON UPDATE CASCADE ON DELETE SET NULL
Referenced by:
    TABLE "publication" CONSTRAINT "publication_ibfk_1" FOREIGN KEY (accid) REFERENCES accomplishment(accid) ON UPDATE CASCADE ON DELETE CASCADE

"""
class Accomplishment(BaseModel):
    acc_id = AutoField(column_name='accid')
    is_award = BooleanField(column_name='isaward', default=False)
    name = CharField(max_length=100, null=True)
    prize = CharField(max_length=100, null=True)
    sub_id = ForeignKeyField(column_name='subid', field='subid', model=Submission, null=True)

    class Meta:
        table_name = 'accomplishment'
        schema = 'arxiv'

"""
Table "arxiv.awardtypes"
   Column   |          Type          | Collation | Nullable |                Default                 
------------+------------------------+-----------+----------+----------------------------------------
 id         | bigint                 |           | not null | nextval('awardtypes_id_seq'::regclass)
 numeventid | bigint                 |           | not null | 
 awardtype  | character varying(100) |           | not null | 
Indexes:
    "idx_16391_primary" PRIMARY KEY, btree (id)
    "idx_16391_numeventid" UNIQUE, btree (numeventid, awardtype)
Foreign-key constraints:
    "awardtypes_ibfk_1" FOREIGN KEY (numeventid) REFERENCES researchevent(numeventid) ON UPDATE CASCADE ON DELETE CASCADE
"""
class AwardTypes(BaseModel):
    award_type = CharField(max_length=100, column_name='awardtype')
    id = BigAutoField()
    num_event_id = ForeignKeyField(column_name='numeventid', field='numeventid', model=ResearchEvent)

    class Meta:
        table_name = 'awardtypes'
        indexes = (
            (('numeventid', 'awardtype'), True),
        )
        schema = 'arxiv'

"""
Table "arxiv.department"
 Column |         Type          | Collation | Nullable |        Default        
--------+-----------------------+-----------+----------+-----------------------
 deptid | character(2)          |           | not null | 
 name   | character varying(50) |           | not null | ''::character varying
Indexes:
    "idx_16395_primary" PRIMARY KEY, btree (deptid)
Referenced by:
    TABLE "nushteacher" CONSTRAINT "nushteacher_ibfk_1" FOREIGN KEY (deptid) REFERENCES department(deptid) ON UPDATE CASCADE ON DELETE SET NULL
    TABLE "project" CONSTRAINT "project_ibfk_1" FOREIGN KEY (deptid) REFERENCES department(deptid) ON UPDATE CASCADE ON DELETE SET NULL
"""
class Department(BaseModel):
    dept_id = FixedCharField(max_length=2, column_name='deptid', primary_key=True)
    name = CharField(max_length=50, default='')

    class Meta:
        table_name = 'department'
        schema = 'arxiv'

"""
Table "arxiv.student"
 Column |          Type          | Collation | Nullable | Default 
--------+------------------------+-----------+----------+---------
 email  | character varying(255) |           | not null | 
 name   | character varying(100) |           |          | 
Indexes:
    "idx_16475_primary" PRIMARY KEY, btree (email)
Referenced by:
    TABLE "externalstudent" CONSTRAINT "externalstudent_ibfk_1" FOREIGN KEY (email) REFERENCES student(email) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE "nushstudent" CONSTRAINT "nushstudent_ibfk_1" FOREIGN KEY (email) REFERENCES student(email) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE "submits" CONSTRAINT "submits_ibfk_1" FOREIGN KEY (studentemail) REFERENCES student(email) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE "works_on" CONSTRAINT "works_on_ibfk_2" FOREIGN KEY (studentemail) REFERENCES student(email) ON UPDATE CASCADE ON DELETE CASCADE
"""
class Student(BaseModel):
    email = CharField(max_length=255, primary_key=True)
    name = CharField(max_length=100, null=True)

    class Meta:
        table_name = 'student'
        schema = 'arxiv'

"""
Table "arxiv.institution"
   Column    |          Type          | Collation | Nullable |        Default        
-------------+------------------------+-----------+----------+-----------------------
 instid      | character varying(10)  |           | not null | 
 name        | character varying(100) |           | not null | ''::character varying
 address     | character varying(150) |           | not null | ''::character varying
 isschool    | boolean                |           | not null | false
 isinstitute | boolean                |           | not null | false
 isorganiser | boolean                |           | not null | false
 ispublisher | boolean                |           | not null | false
Indexes:
    "idx_16407_primary" PRIMARY KEY, btree (instid)
Referenced by:
    TABLE "externalteacher" CONSTRAINT "externalteacher_ibfk_1" FOREIGN KEY (schid) REFERENCES institution(instid) ON UPDATE CASCADE ON DELETE SET NULL
    TABLE "organises" CONSTRAINT "organises_ibfk_2" FOREIGN KEY (instid) REFERENCES institution(instid) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE "publishedby" CONSTRAINT "publishedby_ibfk_2" FOREIGN KEY (instid) REFERENCES institution(instid) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE "works_at" CONSTRAINT "works_at_ibfk_2" FOREIGN KEY (instid) REFERENCES institution(instid) ON UPDATE CASCADE ON DELETE CASCADE
"""
class Institution(BaseModel):
    address = CharField(max_length=150, default='')
    inst_id = CharField(max_length=10, primary_key=True, column_name='instid')
    is_institute = BooleanField(default=False, column_name='isinstitute')
    is_organiser = BooleanField(default=False, column_name='isorganiser')
    is_publisher = BooleanField(default=False, column_name='ispublisher')
    is_school = BooleanField(default=False, column_name='isschool')
    name = CharField(max_length=100, default='')

    class Meta:
        table_name = 'institution'
        schema = 'arxiv'

"""
Table "arxiv.externalteacher"
 Column |          Type          | Collation | Nullable | Default 
--------+------------------------+-----------+----------+---------
 email  | character varying(255) |           | not null | 
 name   | character varying(100) |           |          | 
 schid  | character varying(10)  |           |          | 
Indexes:
    "idx_16404_primary" PRIMARY KEY, btree (email)
    "idx_16404_schid" btree (schid)
Foreign-key constraints:
    "externalteacher_ibfk_1" FOREIGN KEY (schid) REFERENCES institution(instid) ON UPDATE CASCADE ON DELETE SET NULL
Referenced by:
    TABLE "externalstudent" CONSTRAINT "externalstudent_ibfk_2" FOREIGN KEY (emergencyemail) REFERENCES externalteacher(email) ON UPDATE CASCADE ON DELETE SET NULL
"""
class ExternalTeacher(BaseModel):
    email = CharField(max_length=255, primary_key=True)
    name = CharField(max_length=100, null=True)
    sch_id = ForeignKeyField(column_name='schid', field='instid', model=Institution, null=True)

    class Meta:
        table_name = 'externalteacher'
        schema = 'arxiv'

"""
Table "arxiv.externalstudent"
     Column     |          Type          | Collation | Nullable | Default 
----------------+------------------------+-----------+----------+---------
 email          | character varying(255) |           | not null | 
 emergencyemail | character varying(255) |           |          | 
Indexes:
    "idx_16399_primary" PRIMARY KEY, btree (email)
    "idx_16399_emergencyemail" btree (emergencyemail)
Foreign-key constraints:
    "externalstudent_ibfk_1" FOREIGN KEY (email) REFERENCES student(email) ON UPDATE CASCADE ON DELETE CASCADE
    "externalstudent_ibfk_2" FOREIGN KEY (emergencyemail) REFERENCES externalteacher(email) ON UPDATE CASCADE ON DELETE SET NULL
"""
class ExternalStudent(BaseModel):
    email = ForeignKeyField(column_name='email', field='email', model=Student, primary_key=True)
    emergency_email = ForeignKeyField(column_name='emergencyemail', field='email', model=ExternalTeacher, null=True)

    class Meta:
        table_name = 'externalstudent'
        schema = 'arxiv'

"""
Table "arxiv.journal"
 Column |          Type          | Collation | Nullable | Default 
--------+------------------------+-----------+----------+---------
 issn   | integer                |           | not null | 
 name   | character varying(100) |           | not null | 
Indexes:
    "idx_16416_primary" PRIMARY KEY, btree (issn)
Referenced by:
    TABLE "publication" CONSTRAINT "publication_ibfk_2" FOREIGN KEY (journissn) REFERENCES journal(issn) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE "publishedby" CONSTRAINT "publishedby_ibfk_1" FOREIGN KEY (issn) REFERENCES journal(issn) ON UPDATE CASCADE ON DELETE CASCADE
"""
class Journal(BaseModel):
    issn = IntegerField(primary_key=True)
    name = CharField(max_length=100)

    class Meta:
        table_name = 'journal'
        schema = 'arxiv'

"""
Table "arxiv.researchmentor"
 Column |          Type          | Collation | Nullable | Default 
--------+------------------------+-----------+----------+---------
 email  | character varying(255) |           | not null | 
 name   | character varying(100) |           |          | 
Indexes:
    "idx_16472_primary" PRIMARY KEY, btree (email)
Referenced by:
    TABLE "mentors" CONSTRAINT "mentors_ibfk_2" FOREIGN KEY (mentoremail) REFERENCES researchmentor(email) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE "works_at" CONSTRAINT "works_at_ibfk_1" FOREIGN KEY (mentoremail) REFERENCES researchmentor(email) ON UPDATE CASCADE ON DELETE CASCADE
"""
class ResearchMentor(BaseModel):
    email = CharField(max_length=255, primary_key=True)
    name = CharField(max_length=100, null=True)

    class Meta:
        table_name = 'researchmentor'
        schema = 'arxiv'

"""
Table "arxiv.nushteacher"
  Column  |          Type          | Collation | Nullable |        Default        
----------+------------------------+-----------+----------+-----------------------
 email    | character varying(255) |           | not null | 
 pwd      | character varying(20)  |           |          | 
 name     | character varying(100) |           | not null | ''::character varying
 pfp      | bytea                  |           |          | 
 isadmin  | boolean                |           | not null | false
 ismentor | boolean                |           | not null | false
 deptid   | character(2)           |           |          | 
Indexes:
    "idx_16429_primary" PRIMARY KEY, btree (email)
    "idx_16429_deptid" btree (deptid)
Foreign-key constraints:
    "nushteacher_ibfk_1" FOREIGN KEY (deptid) REFERENCES department(deptid) ON UPDATE CASCADE ON DELETE SET NULL
Referenced by:
    TABLE "project" CONSTRAINT "project_ibfk_2" FOREIGN KEY (teacheremail) REFERENCES nushteacher(email) ON UPDATE CASCADE ON DELETE SET NULL
"""
class NUSHTeacher(BaseModel):
    dept_id = ForeignKeyField(column_name='deptid', field='deptid', model=Department, null=True)
    email = CharField(max_length=255, primary_key=True)
    is_admin = BooleanField(column_name="isadmin", default=False)
    is_mentor = BooleanField(column_name="ismentor", default=False)
    name = CharField(max_length=100, default='')
    pfp = BlobField(null=True)
    pwd = CharField(max_length=20, null=True)

    class Meta:
        table_name = 'nushteacher'
        schema = 'arxiv'

"""
Table "arxiv.project"
    Column    |          Type           | Collation | Nullable | Default 
--------------+-------------------------+-----------+----------+---------
 pcode        | character varying(20)   |           | not null | 
 title        | character varying(200)  |           | not null | 
 abstract     | character varying(2000) |           |          | 
 reportpdf    | bytea                   |           |          | 
 year         | integer                 |           |          | 
 deptid       | character(2)            |           |          | 
 teacheremail | character varying(255)  |           |          | 
Indexes:
    "idx_16442_primary" PRIMARY KEY, btree (pcode)
    "idx_16442_deptid" btree (deptid)
    "idx_16442_teacheremail" btree (teacheremail)
Foreign-key constraints:
    "project_ibfk_1" FOREIGN KEY (deptid) REFERENCES department(deptid) ON UPDATE CASCADE ON DELETE SET NULL
    "project_ibfk_2" FOREIGN KEY (teacheremail) REFERENCES nushteacher(email) ON UPDATE CASCADE ON DELETE SET NULL
Referenced by:
    TABLE "mentors" CONSTRAINT "mentors_ibfk_1" FOREIGN KEY (pcode) REFERENCES project(pcode) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE "projectcontinuation" CONSTRAINT "projectcontinuation_ibfk_1" FOREIGN KEY (prevpcode) REFERENCES project(pcode) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE "projectcontinuation" CONSTRAINT "projectcontinuation_ibfk_2" FOREIGN KEY (nextpcode) REFERENCES project(pcode) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE "submits" CONSTRAINT "submits_ibfk_2" FOREIGN KEY (pcode) REFERENCES project(pcode) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE "works_on" CONSTRAINT "works_on_ibfk_1" FOREIGN KEY (pcode) REFERENCES project(pcode) ON UPDATE CASCADE ON DELETE CASCADE
"""
class Project(BaseModel):
    abstract = CharField(max_length=2000, null=True)
    dept_id = ForeignKeyField(column_name='deptid', field='deptid', model=Department, null=True)
    project_code = CharField(column_name='pcode', primary_key=True, max_length=20)
    report_pdf = BlobField(null=True, column_name='reportpdf')
    teacher_email = ForeignKeyField(column_name='teacheremail', field='email', model=NUSHTeacher, null=True)
    title = CharField(max_length=200)
    year = IntegerField(null=True)

    class Meta:
        table_name = 'project'
        schema = 'arxiv'

"""
Table "arxiv.mentors"
   Column    |          Type          | Collation | Nullable |               Default               
-------------+------------------------+-----------+----------+-------------------------------------
 id          | bigint                 |           | not null | nextval('mentors_id_seq'::regclass)
 mentoremail | character varying(255) |           | not null | 
 pcode       | character varying(20)  |           | not null | 
Indexes:
    "idx_16420_primary" PRIMARY KEY, btree (id)
    "idx_16420_mentoremail" btree (mentoremail)
    "idx_16420_pcode_2" UNIQUE, btree (pcode, mentoremail)
Foreign-key constraints:
    "mentors_ibfk_1" FOREIGN KEY (pcode) REFERENCES project(pcode) ON UPDATE CASCADE ON DELETE CASCADE
    "mentors_ibfk_2" FOREIGN KEY (mentoremail) REFERENCES researchmentor(email) ON UPDATE CASCADE ON DELETE CASCADE
"""
class Mentors(BaseModel):
    id = BigAutoField()
    mentor_email = ForeignKeyField(column_name='mentoremail', field='email', model=ResearchMentor)
    project_code = ForeignKeyField(column_name='pcode', field='pcode', model=Project)

    class Meta:
        table_name = 'mentors'
        indexes = (
            (('pcode', 'mentoremail'), True),
        )
        schema = 'arxiv'

"""
Table "arxiv.nushstudent"
  Column  |          Type           | Collation | Nullable | Default 
----------+-------------------------+-----------+----------+---------
 email    | character varying(255)  |           | not null | 
 pwd      | character varying(20)   |           |          | 
 pfp      | bytea                   |           |          | 
 about    | character varying(1000) |           |          | 
 gradyear | integer                 |           |          | 
 nush_sid | character varying(8)    |           |          | 
Indexes:
    "idx_16424_primary" PRIMARY KEY, btree (email)
Foreign-key constraints:
    "nushstudent_ibfk_1" FOREIGN KEY (email) REFERENCES student(email) ON UPDATE CASCADE ON DELETE CASCADE
"""
class NUSHStudent(BaseModel):
    about = CharField(max_length=255, null=True)
    email = ForeignKeyField(column_name='email', field='email', model=Student, primary_key=True)
    grad_year = IntegerField(column_name='gradyear', null=True)
    nush_student_id = CharField(column_name='nush_sid', max_length=8, null=True)
    pfp = BlobField(null=True)
    pwd = CharField(max_length=20, null=True)

    class Meta:
        table_name = 'nushstudent'
        schema = 'arxiv'

"""
Table "arxiv.organises"
   Column   |         Type          | Collation | Nullable |                Default                
------------+-----------------------+-----------+----------+---------------------------------------
 id         | bigint                |           | not null | nextval('organises_id_seq'::regclass)
 numeventid | bigint                |           | not null | 
 instid     | character varying(10) |           | not null | 
Indexes:
    "idx_16438_primary" PRIMARY KEY, btree (id)
    "idx_16438_instid" btree (instid)
    "idx_16438_numeventid" UNIQUE, btree (numeventid, instid)
Foreign-key constraints:
    "organises_ibfk_2" FOREIGN KEY (instid) REFERENCES institution(instid) ON UPDATE CASCADE ON DELETE CASCADE
    "organises_ibfk_3" FOREIGN KEY (numeventid) REFERENCES researchevent(numeventid) ON UPDATE CASCADE ON DELETE CASCADE
"""
class Organises(BaseModel):
    id = BigAutoField()
    inst_id = ForeignKeyField(column_name='instid', field='instid', model=Institution)
    num_event_id = ForeignKeyField(column_name='numeventid', field='numeventid', model=ResearchEvent)

    class Meta:
        table_name = 'organises'
        indexes = (
            (('numeventid', 'instid'), True),
        )
        schema = 'arxiv'

"""
Table "arxiv.projectcontinuation"
  Column   |         Type          | Collation | Nullable |                     Default                     
-----------+-----------------------+-----------+----------+-------------------------------------------------
 id        | bigint                |           | not null | nextval('projectcontinuation_id_seq'::regclass)
 prevpcode | character varying(20) |           | not null | 
 nextpcode | character varying(20) |           | not null | 
Indexes:
    "idx_16448_primary" PRIMARY KEY, btree (id)
    "idx_16448_nextpcode" btree (nextpcode)
    "idx_16448_prevpcode_2" UNIQUE, btree (prevpcode, nextpcode)
Foreign-key constraints:
    "projectcontinuation_ibfk_1" FOREIGN KEY (prevpcode) REFERENCES project(pcode) ON UPDATE CASCADE ON DELETE CASCADE
    "projectcontinuation_ibfk_2" FOREIGN KEY (nextpcode) REFERENCES project(pcode) ON UPDATE CASCADE ON DELETE CASCADE
"""
class ProjectContinuation(BaseModel):
    id = BigAutoField()
    next_project_code = ForeignKeyField(column_name='nextpcode', field='pcode', model=Project)
    prev_project_code = ForeignKeyField(backref='project_prev_code_set', column_name='prevpcode', field='pcode', model=Project)

    class Meta:
        table_name = 'projectcontinuation'
        indexes = (
            (('prevpcode', 'nextpcode'), True),
        )
        schema = 'arxiv'

"""
Table "arxiv.publication"
  Column   |          Type          | Collation | Nullable | Default 
-----------+------------------------+-----------+----------+---------
 accid     | integer                |           | not null | 
 pubtitle  | character varying(200) |           | not null | 
 doi       | character varying(200) |           |          | 
 isjournal | boolean                |           | not null | false
 url       | character varying(300) |           |          | 
 journissn | integer                |           |          | 
Indexes:
    "idx_16452_primary" PRIMARY KEY, btree (accid)
    "idx_16452_journissn" btree (journissn)
Foreign-key constraints:
    "publication_ibfk_1" FOREIGN KEY (accid) REFERENCES accomplishment(accid) ON UPDATE CASCADE ON DELETE CASCADE
    "publication_ibfk_2" FOREIGN KEY (journissn) REFERENCES journal(issn) ON UPDATE CASCADE ON DELETE CASCADE
"""
class Publication(BaseModel):
    acc_id = ForeignKeyField(column_name='accid', field='accid', model=Accomplishment, primary_key=True)
    doi = CharField(max_length=200, null=True)
    is_journal = BooleanField(column_name="isjournal", default=False)
    journal_issn = ForeignKeyField(column_name='journissn', field='issn', model=Journal, null=True)
    title = CharField(max_length=200, column_name='pubtitle')
    url = CharField(max_length=300, null=True)

    class Meta:
        table_name = 'publication'
        schema = 'arxiv'

"""
Table "arxiv.publishedby"
 Column |         Type          | Collation | Nullable |                 Default                 
--------+-----------------------+-----------+----------+-----------------------------------------
 id     | bigint                |           | not null | nextval('publishedby_id_seq'::regclass)
 issn   | integer               |           | not null | 
 instid | character varying(10) |           | not null | 
Indexes:
    "idx_16459_primary" PRIMARY KEY, btree (id)
    "idx_16459_instid" btree (instid)
    "idx_16459_issn_2" UNIQUE, btree (issn, instid)
Foreign-key constraints:
    "publishedby_ibfk_1" FOREIGN KEY (issn) REFERENCES journal(issn) ON UPDATE CASCADE ON DELETE CASCADE
    "publishedby_ibfk_2" FOREIGN KEY (instid) REFERENCES institution(instid) ON UPDATE CASCADE ON DELETE CASCADE
"""
class PublishedBy(BaseModel):
    id = BigAutoField()
    inst_id = ForeignKeyField(column_name='instid', field='instid', model=Institution)
    issn = ForeignKeyField(column_name='issn', field='issn', model=Journal)

    class Meta:
        table_name = 'publishedby'
        indexes = (
            (('issn', 'instid'), True),
        )
        schema = 'arxiv'

"""
Table "arxiv.submits"
    Column    |          Type          | Collation | Nullable |               Default               
--------------+------------------------+-----------+----------+-------------------------------------
 id           | bigint                 |           | not null | nextval('submits_id_seq'::regclass)
 studentemail | character varying(255) |           | not null | 
 pcode        | character varying(20)  |           | not null | 
 subid        | bigint                 |           | not null | 
Indexes:
    "idx_16486_primary" PRIMARY KEY, btree (id)
    "idx_16486_pcode" btree (pcode)
    "idx_16486_studentemail_2" UNIQUE, btree (studentemail, pcode, subid)
    "idx_16486_subid" btree (subid)
Foreign-key constraints:
    "submits_ibfk_1" FOREIGN KEY (studentemail) REFERENCES student(email) ON UPDATE CASCADE ON DELETE CASCADE
    "submits_ibfk_2" FOREIGN KEY (pcode) REFERENCES project(pcode) ON UPDATE CASCADE ON DELETE CASCADE
    "submits_ibfk_3" FOREIGN KEY (subid) REFERENCES submission(subid) ON UPDATE CASCADE ON DELETE CASCADE
"""
class Submits(BaseModel):
    id = BigAutoField()
    project_code = ForeignKeyField(column_name='pcode', field='pcode', model=Project)
    student_email = ForeignKeyField(column_name='studentemail', field='email', model=Student)
    sub_id = ForeignKeyField(column_name='subid', field='subid', model=Submission)

    class Meta:
        table_name = 'submits'
        indexes = (
            (('studentemail', 'pcode', 'subid'), True),
        )
        schema = 'arxiv'

"""
Table "arxiv.works_at"
   Column    |          Type          | Collation | Nullable |               Default                
-------------+------------------------+-----------+----------+--------------------------------------
 id          | bigint                 |           | not null | nextval('works_at_id_seq'::regclass)
 mentoremail | character varying(255) |           | not null | 
 instid      | character varying(10)  |           | not null | 
 dept        | character varying(100) |           |          | 
 role        | character varying(100) |           |          | 
 officeaddr  | character varying(100) |           |          | 
Indexes:
    "idx_16491_primary" PRIMARY KEY, btree (id)
    "idx_16491_instid" btree (instid)
    "idx_16491_mentoremail" UNIQUE, btree (mentoremail, instid)
Foreign-key constraints:
    "works_at_ibfk_1" FOREIGN KEY (mentoremail) REFERENCES researchmentor(email) ON UPDATE CASCADE ON DELETE CASCADE
    "works_at_ibfk_2" FOREIGN KEY (instid) REFERENCES institution(instid) ON UPDATE CASCADE ON DELETE CASCADE
"""
class WorksAt(BaseModel):
    dept = CharField(max_length=100, null=True)
    id = BigAutoField()
    inst_id = ForeignKeyField(column_name='instid', field='instid', model=Institution)
    mentor_email = ForeignKeyField(column_name='mentoremail', field='email', model=ResearchMentor)
    office_addr = CharField(column_name='officeaddr', max_length=100, null=True)
    role = CharField(max_length=100, null=True)

    class Meta:
        table_name = 'works_at'
        indexes = (
            (('mentoremail', 'instid'), True),
        )
        schema = 'arxiv'

"""
Table "arxiv.works_on"
    Column    |          Type          | Collation | Nullable |               Default                
--------------+------------------------+-----------+----------+--------------------------------------
 id           | bigint                 |           | not null | nextval('works_on_id_seq'::regclass)
 studentemail | character varying(255) |           | not null | 
 pcode        | character varying(20)  |           | not null | 
Indexes:
    "idx_16498_primary" PRIMARY KEY, btree (id)
    "idx_16498_pcode" btree (pcode)
    "idx_16498_studentemail" UNIQUE, btree (studentemail, pcode)
Foreign-key constraints:
    "works_on_ibfk_1" FOREIGN KEY (pcode) REFERENCES project(pcode) ON UPDATE CASCADE ON DELETE CASCADE
    "works_on_ibfk_2" FOREIGN KEY (studentemail) REFERENCES student(email) ON UPDATE CASCADE ON DELETE CASCADE
"""
class WorksOn(BaseModel):
    id = BigAutoField()
    project_code = ForeignKeyField(column_name='pcode', field='pcode', model=Project)
    student_email = ForeignKeyField(column_name='studentemail', field='email', model=Student)

    class Meta:
        table_name = 'works_on'
        indexes = (
            (('studentemail', 'pcode'), True),
        )
        schema = 'arxiv'

