from typing import Optional
from sqlalchemy import ForeignKey, MetaData, UniqueConstraint, create_engine, Index
from sqlalchemy.sql.expression import false
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker
from sqlalchemy.dialects.postgresql import BIGINT, VARCHAR, BOOLEAN, DATE, INTEGER, BYTEA
from datetime import date

engine = create_engine('postgresql+asyncpg://postgres:admin@database/arxiv')
metadata_obj = MetaData(schema="arxiv")

class Base(DeclarativeBase):
    metadata = metadata_obj

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
class ResearchEvent(Base):
    __tablename__ = 'researchevent'
    
    num_event_id: Mapped[int] = mapped_column("numeventid", BIGINT, primary_key=True)
    event_id: Mapped[str] = mapped_column("eventid", VARCHAR(15))
    year: Mapped[int] = mapped_column("year", INTEGER)
    name: Mapped[str] = mapped_column("name", VARCHAR(100))
    about: Mapped[Optional[str]] = mapped_column("about", VARCHAR(5000))
    start_date: Mapped[date] = mapped_column("start_date", DATE)
    end_date: Mapped[date] = mapped_column("end_date", DATE)
    format: Mapped[Optional[str]] = mapped_column("format", VARCHAR(10))
    is_competition: Mapped[bool] = mapped_column("iscompetition", BOOLEAN, server_default=false(), default=False)
    is_conference: Mapped[bool] = mapped_column("isconference", BOOLEAN, server_default=false(), default=False) 
    conf_doi: Mapped[Optional[str]] = mapped_column("confdoi", VARCHAR(200))

    submissions: Mapped[list["Submission"]] = relationship(back_populates="event", cascade="all, delete-orphan", passive_deletes=True)
    award_types: Mapped[list["AwardTypes"]] = relationship(back_populates="event", cascade="all, delete-orphan", passive_deletes=True)
    organisers: Mapped[list["Organises"]] = relationship(back_populates="event", cascade="all, delete-orphan", passive_deletes=True)

    __table_args__ = (UniqueConstraint('eventid', 'year', name='idx_16464_eventid_2'),)

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
class Submission(Base):
    __tablename__ = 'submission'

    sub_id: Mapped[int] = mapped_column("subid", BIGINT, primary_key=True)
    num_event_id: Mapped[int] = mapped_column("numeventid", ForeignKey("researchevent.numeventid", name="submission_ibfk_1", onupdate="CASCADE", ondelete="CASCADE"))
    code: Mapped[str] = mapped_column("code", VARCHAR(20))
    sub_title: Mapped[str] = mapped_column("subtitle", VARCHAR(200))
    sub_abstract: Mapped[str] = mapped_column("subabstract", VARCHAR(2000))

    event: Mapped[ResearchEvent] = relationship("ResearchEvent", back_populates="submissions")

    accomplishments: Mapped[list["Accomplishment"]] = relationship("Accomplishment", back_populates="submission")
    submits: Mapped[list["Submits"]] = relationship("Submits", back_populates="submission", cascade="all, delete-orphan", passive_deletes=True)

    __table_args__ = (UniqueConstraint('numeventid', 'code', name='idx_16479_numeventid'),)

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
class Accomplishment(Base):
    __tablename__ = 'accomplishment'

    acc_id: Mapped[int] = mapped_column("accid", INTEGER, primary_key=True)
    is_award: Mapped[bool] = mapped_column("isaward", BOOLEAN, server_default=false(), default=False)
    name: Mapped[Optional[str]] = mapped_column("name", VARCHAR(100))
    prize: Mapped[Optional[str]] = mapped_column("prize", VARCHAR(100))
    sub_id: Mapped[Optional[int]] = mapped_column("subid", ForeignKey("submission.subid", name="accomplishment_ibfk_1", onupdate="CASCADE", ondelete="SET NULL"))

    submission: Mapped[Submission] = relationship("Submission", back_populates="accomplishments")
    publication: Mapped["Publication"] = relationship("Publication", back_populates="accomplishment", cascade="all, delete-orphan", passive_deletes=True)

    __table_args__ = (Index('idx_16386_subid', 'subid'),)

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
class AwardTypes(Base):
    __tablename__ = 'awardtypes'

    id: Mapped[int] = mapped_column("id", BIGINT, primary_key=True)
    num_event_id: Mapped[int] = mapped_column("numeventid", ForeignKey("researchevent.numeventid", name="awardtypes_ibfk_1", onupdate="CASCADE", ondelete="CASCADE"))
    award_type: Mapped[str] = mapped_column("awardtype", VARCHAR(100))

    event: Mapped[ResearchEvent] = relationship("ResearchEvent", back_populates="award_types")

    __table_args__ = (UniqueConstraint('numeventid', 'awardtype', name='idx_16391_numeventid'),)

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
class Department(Base):
    __tablename__ = 'department'

    dept_id: Mapped[str] = mapped_column("deptid", VARCHAR(2), primary_key=True)
    name: Mapped[str] = mapped_column("name", VARCHAR(50), server_default="", default="")

    teachers: Mapped[list["NUSHTeacher"]] = relationship("NUSHTeacher", back_populates="department")
    projects: Mapped[list["Project"]] = relationship("Project", back_populates="department")

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
class Student(Base):
    __tablename__ = 'student'

    email: Mapped[str] = mapped_column("email", VARCHAR(255), primary_key=True)
    name: Mapped[Optional[str]] = mapped_column("name", VARCHAR(100))

    external_student: Mapped["ExternalStudent"] = relationship("ExternalStudent", back_populates="student", cascade="all, delete-orphan", passive_deletes=True)
    nush_student: Mapped["NUSHStudent"] = relationship("NUSHStudent", back_populates="student", cascade="all, delete-orphan", passive_deletes=True)
    submits: Mapped[list["Submits"]] = relationship("Submits", back_populates="student", cascade="all, delete-orphan", passive_deletes=True)
    projects: Mapped[list["WorksOn"]] = relationship("WorksOn", back_populates="student", cascade="all, delete-orphan", passive_deletes=True)

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
class Institution(Base):
    __tablename__ = 'institution'

    inst_id: Mapped[str] = mapped_column("instid", VARCHAR(10), primary_key=True)
    name: Mapped[str] = mapped_column("name", VARCHAR(100), server_default="", default="")
    address: Mapped[str] = mapped_column("address", VARCHAR(150), server_default="", default="")
    is_school: Mapped[bool] = mapped_column("isschool", BOOLEAN, server_default=false(), default=False)
    is_institute: Mapped[bool] = mapped_column("isinstitute", BOOLEAN, server_default=false(), default=False)
    is_organiser: Mapped[bool] = mapped_column("isorganiser", BOOLEAN, server_default=false(), default=False)
    is_publisher: Mapped[bool] = mapped_column("ispublisher", BOOLEAN, server_default=false(), default=False)

    teachers: Mapped[list["ExternalTeacher"]] = relationship("ExternalTeacher", back_populates="institution")
    events: Mapped[list["Organises"]] = relationship("Organises", back_populates="institution", cascade="all, delete-orphan", passive_deletes=True)
    publishes: Mapped[list["PublishedBy"]] = relationship("PublishedBy", back_populates="institution", cascade="all, delete-orphan", passive_deletes=True)
    members: Mapped[list["WorksAt"]] = relationship("WorksAt", back_populates="institution", cascade="all, delete-orphan", passive_deletes=True)

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
class ExternalTeacher(Base):
    __tablename__ = 'externalteacher'

    email: Mapped[str] = mapped_column("email", VARCHAR(255), primary_key=True)
    name: Mapped[Optional[str]] = mapped_column("name", VARCHAR(100))
    sch_id: Mapped[Optional[str]] = mapped_column("schid", ForeignKey("institution.instid", name="externalteacher_ibfk_1", onupdate="CASCADE", ondelete="SET NULL"))

    institution: Mapped[Institution] = relationship("Institution", back_populates="teachers")
    students: Mapped[list["ExternalStudent"]] = relationship("ExternalStudent", back_populates="teacher")

    __table_args__ = (Index('idx_16404_schid', 'schid'),)

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
class ExternalStudent(Base):
    __tablename__ = 'externalstudent'

    email: Mapped[str] = mapped_column("email", ForeignKey("student.email", name="externalstudent_ibfk_1", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
    emergency_email: Mapped[Optional[str]] = mapped_column("emergencyemail", ForeignKey("externalteacher.email", name="externalstudent_ibfk_2", onupdate="CASCADE", ondelete="SET NULL"))

    student: Mapped[Student] = relationship("Student", back_populates="external_student")
    teacher: Mapped[ExternalTeacher] = relationship("ExternalTeacher", back_populates="students")

    __table_args__ = (Index('idx_16399_emergencyemail', 'emergencyemail'),)

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
class Journal(Base):
    __tablename__ = 'journal'

    issn: Mapped[int] = mapped_column("issn", INTEGER, autoincrement=False, primary_key=True)
    name: Mapped[str] = mapped_column("name", VARCHAR(100))

    publications: Mapped[list["Publication"]] = relationship("Publication", back_populates="journal", cascade="all, delete-orphan", passive_deletes=True)
    publishers: Mapped[list["PublishedBy"]] = relationship("PublishedBy", back_populates="journal", cascade="all, delete-orphan", passive_deletes=True)

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
class ResearchMentor(Base):
    __tablename__ = 'researchmentor'

    email: Mapped[str] = mapped_column("email", VARCHAR(255), primary_key=True)
    name: Mapped[Optional[str]] = mapped_column("name", VARCHAR(100))

    projects: Mapped[list["Mentors"]] = relationship("Mentors", back_populates="mentor", cascade="all, delete-orphan", passive_deletes=True)
    workplaces: Mapped[list["WorksAt"]] = relationship("WorksAt", back_populates="mentor", cascade="all, delete-orphan", passive_deletes=True)

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
class NUSHTeacher(Base):
    __tablename__ = 'nushteacher'

    email: Mapped[str] = mapped_column("email", VARCHAR(255), primary_key=True)
    pwd: Mapped[Optional[str]] = mapped_column("pwd", VARCHAR(20))
    name: Mapped[str] = mapped_column("name", VARCHAR(100), server_default="", default="")
    pfp_bytes: Mapped[Optional[bytes]] = mapped_column("pfp", BYTEA)
    is_admin: Mapped[bool] = mapped_column("isadmin", BOOLEAN, server_default=false(), default=False)
    is_mentor: Mapped[bool] = mapped_column("ismentor", BOOLEAN, server_default=false(), default=False)
    dept_id: Mapped[Optional[str]] = mapped_column("deptid", ForeignKey("department.deptid", name="nushteacher_ibfk_1", onupdate="CASCADE", ondelete="SET NULL"))

    department: Mapped[Department] = relationship("Department", back_populates="teachers")
    projects: Mapped[list["Project"]] = relationship("Project", back_populates="teacher")

    __table_args__ = (Index('idx_16429_deptid', 'deptid'),)

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
class Project(Base):
    __tablename__ = 'project'

    p_code: Mapped[str] = mapped_column("pcode", VARCHAR(20), primary_key=True)
    title: Mapped[str] = mapped_column("title", VARCHAR(200))
    abstract: Mapped[Optional[str]] = mapped_column("abstract", VARCHAR(2000))
    report_pdf: Mapped[Optional[bytes]] = mapped_column("reportpdf", BYTEA)
    year: Mapped[Optional[int]] = mapped_column("year", INTEGER)
    dept_id: Mapped[Optional[str]] = mapped_column("deptid", ForeignKey("department.deptid", name="project_ibfk_1", onupdate="CASCADE", ondelete="SET NULL"))
    teacher_email: Mapped[Optional[str]] = mapped_column("teacheremail", ForeignKey("nushteacher.email", name="project_ibfk_2", onupdate="CASCADE", ondelete="SET NULL"))

    department: Mapped[Department] = relationship("Department", back_populates="projects")
    teacher: Mapped[NUSHTeacher] = relationship("NUSHTeacher", back_populates="projects")

    mentors: Mapped[list["Mentors"]] = relationship("Mentors", back_populates="project", cascade="all, delete-orphan", passive_deletes=True)
    continuations: Mapped[list["ProjectContinuation"]] = relationship("ProjectContinuation", foreign_keys="[ProjectContinuation.prev_p_code]", back_populates="prev_project", cascade="all, delete-orphan", passive_deletes=True)
    prev_projects: Mapped[list["ProjectContinuation"]] = relationship("ProjectContinuation", foreign_keys="[ProjectContinuation.next_p_code]", back_populates="next_project", cascade="all, delete-orphan", passive_deletes=True)
    submits: Mapped[list["Submits"]] = relationship("Submits", back_populates="project", cascade="all, delete-orphan", passive_deletes=True)
    students: Mapped[list["WorksOn"]] = relationship("WorksOn", back_populates="project", cascade="all, delete-orphan", passive_deletes=True)

    __table_args__ = (Index('idx_16442_deptid', 'deptid'), Index('idx_16442_teacheremail', 'teacheremail'),)

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
class Mentors(Base):
    __tablename__ = 'mentors'

    id: Mapped[int] = mapped_column("id", BIGINT, primary_key=True)
    mentor_email: Mapped[str] = mapped_column("mentoremail", ForeignKey("researchmentor.email", name="mentors_ibfk_2", onupdate="CASCADE", ondelete="CASCADE"))
    p_code: Mapped[str] = mapped_column("pcode", ForeignKey("project.pcode", name="mentors_ibfk_1", onupdate="CASCADE", ondelete="CASCADE"))

    project: Mapped[Project] = relationship("Project", back_populates="mentors")
    mentor: Mapped[ResearchMentor] = relationship("ResearchMentor", back_populates="projects")

    __table_args__ = (UniqueConstraint('pcode', 'mentoremail', name='idx_16420_pcode_2'), Index('idx_16420_mentoremail', 'mentoremail'),)

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
class NUSHStudent(Base):
    __tablename__ = 'nushstudent'

    email: Mapped[str] = mapped_column("email", ForeignKey("student.email", name="nushstudent_ibfk_1", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
    pwd: Mapped[Optional[str]] = mapped_column("pwd", VARCHAR(20))
    pfp_bytes: Mapped[Optional[bytes]] = mapped_column("pfp", BYTEA)
    about: Mapped[Optional[str]] = mapped_column("about", VARCHAR(1000))
    grad_year: Mapped[Optional[int]] = mapped_column("gradyear", INTEGER)
    nush_sid: Mapped[Optional[str]] = mapped_column("nush_sid", VARCHAR(8))

    student: Mapped[Student] = relationship("Student", back_populates="nush_student")

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
class Organises(Base):
    __tablename__ = 'organises'

    id: Mapped[int] = mapped_column("id", BIGINT, primary_key=True)
    num_event_id: Mapped[int] = mapped_column("numeventid", ForeignKey("researchevent.numeventid", name="organises_ibfk_3", onupdate="CASCADE", ondelete="CASCADE"))
    inst_id: Mapped[str] = mapped_column("instid", ForeignKey("institution.instid", name="organises_ibfk_2", onupdate="CASCADE", ondelete="CASCADE"))

    event: Mapped[ResearchEvent] = relationship("ResearchEvent", back_populates="organisers")
    institution: Mapped[Institution] = relationship("Institution", back_populates="events")

    __table_args__ = (UniqueConstraint('numeventid', 'instid', name='idx_16438_numeventid'), Index('idx_16438_instid', 'instid'),)

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
class ProjectContinuation(Base):
    __tablename__ = 'projectcontinuation'

    id: Mapped[int] = mapped_column("id", BIGINT, primary_key=True)
    prev_p_code: Mapped[str] = mapped_column("prevpcode", ForeignKey("project.pcode", name="projectcontinuation_ibfk_1", onupdate="CASCADE", ondelete="CASCADE"))
    next_p_code: Mapped[str] = mapped_column("nextpcode", ForeignKey("project.pcode", name="projectcontinuation_ibfk_2", onupdate="CASCADE", ondelete="CASCADE"))

    prev_project: Mapped[Project] = relationship("Project", foreign_keys=[prev_p_code], back_populates="continuations")
    next_project: Mapped[Project] = relationship("Project", foreign_keys=[next_p_code], back_populates="prev_projects")

    __table_args__ = (UniqueConstraint('prevpcode', 'nextpcode', name='idx_16448_prevpcode_2'), Index('idx_16448_nextpcode', 'nextpcode'),)

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
class Publication(Base):
    __tablename__ = 'publication'

    acc_id: Mapped[int] = mapped_column("accid", ForeignKey("accomplishment.accid", name="publication_ibfk_1", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
    pub_title: Mapped[str] = mapped_column("pubtitle", VARCHAR(200))
    doi: Mapped[Optional[str]] = mapped_column("doi", VARCHAR(200))
    is_journal: Mapped[bool] = mapped_column("isjournal", BOOLEAN, server_default=false(), default=False)
    url: Mapped[Optional[str]] = mapped_column("url", VARCHAR(300))
    journ_issn: Mapped[Optional[int]] = mapped_column("journissn", ForeignKey("journal.issn", name="publication_ibfk_2", onupdate="CASCADE", ondelete="CASCADE"))

    accomplishment: Mapped[Accomplishment] = relationship("Accomplishment", back_populates="publication")
    journal: Mapped[Journal] = relationship("Journal", back_populates="publications")

    __table_args__ = (Index('idx_16452_journissn', 'journissn'),)

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
class PublishedBy(Base):
    __tablename__ = 'publishedby'

    id: Mapped[int] = mapped_column("id", BIGINT, primary_key=True)
    issn: Mapped[int] = mapped_column("issn", ForeignKey("journal.issn", name="publishedby_ibfk_1", onupdate="CASCADE", ondelete="CASCADE"))
    inst_id: Mapped[str] = mapped_column("instid", ForeignKey("institution.instid", name="publishedby_ibfk_2", onupdate="CASCADE", ondelete="CASCADE"))

    journal: Mapped[Journal] = relationship("Journal", back_populates="publishers")
    institution: Mapped[Institution] = relationship("Institution", back_populates="publishes")

    __table_args__ = (UniqueConstraint('issn', 'instid', name='idx_16459_issn_2'), Index('idx_16459_instid', 'instid'),)

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
class Submits(Base):
    __tablename__ = 'submits'

    id: Mapped[int] = mapped_column("id", BIGINT, primary_key=True)
    student_email: Mapped[str] = mapped_column("studentemail", ForeignKey("student.email", name="submits_ibfk_1", onupdate="CASCADE", ondelete="CASCADE"))
    p_code: Mapped[str] = mapped_column("pcode", ForeignKey("project.pcode", name="submits_ibfk_2", onupdate="CASCADE", ondelete="CASCADE"))
    sub_id: Mapped[int] = mapped_column("subid", ForeignKey("submission.subid", name="submits_ibfk_3", onupdate="CASCADE", ondelete="CASCADE"))

    student: Mapped[Student] = relationship("Student", back_populates="submits")
    project: Mapped[Project] = relationship("Project", back_populates="submits")
    submission: Mapped[Submission] = relationship("Submission", back_populates="submits")

    __table_args__ = (UniqueConstraint('studentemail', 'pcode', 'subid', name='idx_16486_studentemail_2'), Index('idx_16486_pcode', 'pcode'), Index('idx_16486_subid', 'subid'),)

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
class WorksAt(Base):
    __tablename__ = 'works_at'

    id: Mapped[int] = mapped_column("id", BIGINT, primary_key=True)
    mentor_email: Mapped[str] = mapped_column("mentoremail", ForeignKey("researchmentor.email", name="works_at_ibfk_1", onupdate="CASCADE", ondelete="CASCADE"))
    inst_id: Mapped[str] = mapped_column("instid", ForeignKey("institution.instid", name="works_at_ibfk_2", onupdate="CASCADE", ondelete="CASCADE"))
    dept: Mapped[Optional[str]] = mapped_column("dept", VARCHAR(100))
    role: Mapped[Optional[str]] = mapped_column("role", VARCHAR(100))
    office_addr: Mapped[Optional[str]] = mapped_column("officeaddr", VARCHAR(100))

    mentor: Mapped[ResearchMentor] = relationship("ResearchMentor", back_populates="workplaces")
    institution: Mapped[Institution] = relationship("Institution", back_populates="members")

    __table_args__ = (UniqueConstraint('mentoremail', 'instid', name='idx_16491_mentoremail'), Index('idx_16491_instid', 'instid'),)

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
class WorksOn(Base):
    __tablename__ = 'works_on'

    id: Mapped[int] = mapped_column("id", BIGINT, primary_key=True)
    student_email: Mapped[str] = mapped_column("studentemail", ForeignKey("student.email", name="works_on_ibfk_2", onupdate="CASCADE", ondelete="CASCADE"))
    p_code: Mapped[str] = mapped_column("pcode", ForeignKey("project.pcode", name="works_on_ibfk_1", onupdate="CASCADE", ondelete="CASCADE"))

    project: Mapped[Project] = relationship("Project", back_populates="students")
    student: Mapped[Student] = relationship("Student", back_populates="projects")

    __table_args__ = (UniqueConstraint('studentemail', 'pcode', name='idx_16498_studentemail'), Index('idx_16498_pcode', 'pcode'),)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)