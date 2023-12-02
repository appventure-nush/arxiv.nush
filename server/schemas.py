from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import date

class NUSHStudent(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    email: str
    pwd: Optional[str]
    pfp: Optional[str] = ""
    about: Optional[str]
    grad_year: Optional[int]
    nush_sid: Optional[str]

class NUSHTeacher(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: str
    pwd: Optional[str]
    name: str
    pfp: Optional[str] = ""
    is_admin: bool
    is_mentor: bool
    dept_id: Optional[str]

class ExternalTeacher(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: str
    name: Optional[str]
    sch_id: Optional[str]

class ExternalStudent(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: str
    name: Optional[str]
    emergency_email: Optional[str]
    teacher_name: Optional[str] = None
    sch_id: Optional[str] = None

class Accomplishment(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    acc_id: int
    is_award: bool
    name: Optional[str]
    prize: Optional[str]
    sub_id: Optional[int]

class ResearchEventSubmission(BaseModel):
    sub_id: int
    num_event_id: int
    code: str
    sub_title: str
    sub_abstract: str

    event_id: str
    year: int
    name: str
    about: Optional[str]
    start_date: date
    end_date: date
    is_competition: bool
    is_conference: bool

    projects: list["Project"] = []
    members: list[NUSHStudent | ExternalStudent] = []
    accomplishments: list[Accomplishment] = []

class AwardTypes(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    num_event_id: int
    award_type: str

class Institution(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    inst_id: str
    name: str
    address: str
    is_school: bool
    is_institute: bool
    is_organiser: bool
    is_publisher: bool

class ResearchEvent(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    num_event_id: int
    event_id: str
    year: int
    name: str
    about: Optional[str]
    start_date: date
    end_date: date
    format: Optional[str]
    is_competition: bool
    is_conference: bool
    conf_doi: Optional[str]

    submissions: list[ResearchEventSubmission] = []
    award_types: list[str] = []
    organisers: list[Institution] = []

class WorksAt(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    mentor_email: str 
    inst_id: str
    dept: Optional[str] 
    role: Optional[str]
    office_addr: Optional[str]
class ResearchMentor(BaseModel):
    email: str
    name: Optional[str]

    jobs: list[WorksAt]

class Project(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    p_code: str
    title: str
    abstract: Optional[str]
    report_pdf: str = ""
    year: Optional[int]
    dept_id: Optional[str]

    members: list[NUSHStudent | ExternalStudent] = []
    teacher: NUSHTeacher = NUSHTeacher(email="", pwd="", name="", is_admin=False, is_mentor=False, dept_id="") # (dummy)
    mentors: list[ResearchMentor] = []

class LoginResult(BaseModel):
    result: bool
    user: Optional[NUSHTeacher | NUSHStudent] = None
    message: str

class RegisterStudentResult(BaseModel):
    result: bool
    user: Optional[NUSHStudent] = None
    message: Optional[str] = None
    error: Optional[str] = None

class RegisterTeacherResult(BaseModel):
    result: bool
    user: Optional[NUSHTeacher] = None
    message: Optional[str] = None
    error: Optional[str] = None

class ChangePasswordResult(BaseModel):
    response: str

