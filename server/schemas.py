from typing import Optional
from pydantic import BaseModel, ConfigDict

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

class ExternalStudent(BaseModel):
    email: str
    name: Optional[str]
    emergency_email: Optional[str]
    teacher_name: Optional[str]
    sch_id: Optional[str]

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

class Institution(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    inst_id: str
    name: str
    address: str
    is_school: bool
    is_institute: bool
    is_organiser: bool
    is_publisher: bool
