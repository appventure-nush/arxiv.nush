from flask_mysqldb import MySQL
import MySQLdb.cursors


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
    
    def execute(self, query, args=None):
        cur = self.cursor
        cur.execute(query, args)
    
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
        
    def isInstitute(self, email):
        return len(self.queryAll("SELECT instId FROM Institution WHERE email = %s", (email,))) > 0
        
    def isStudent(self, email):
        return len(self.queryAll("SELECT email FROM Student WHERE email = %s", (email, ))) > 0
    
    def institute(self, instId):
        return self.queryOne("SELECT * FROM Institution WHERE instId = %s", (instId, ))
        
    def student(self, email):
        query = "SELECT email, name, gradYear, nush_sid, pfp FROM NUSHStudent NATURAL INNER JOIN Student WHERE email = %s"
        return self.queryOne(query, (email, ))
    
    def ext_teacher(self, email):
        query = "SELECT * FROM ExternalTeacher WHERE email = %s"
        return self.queryOne(query, (email, ))
    
    def ext_student(self, email):
        query = "SELECT * FROM ExternalStudent NATURAL INNER JOIN Student WHERE email = %s"
        ext_student = self.queryOne(query, (email, ))
        ext_teacher = self.ext_teacher(ext_student.get("emergencyEmail", ""))
        # we want the external teacher email and name + the institution
        
        
        
    
    def teacher(self, email):
        return self.queryOne("SELECT * FROM NUSHTeacher WHERE email = %s", (email, ))
    
    def projectMembers(self, pcode):
        query = "SELECT studentEmail email FROM Works_On WHERE pcode = %s"
        return [self.student(i["email"]) for i in self.queryAll(query, (pcode,))]
    
    def project(self, pcode):
        project = self.queryOne("SELECT * FROM Project WHERE pcode = %s", (pcode, ))
        project["members"] = self.projectMembers(pcode)
        project["teacher"] = self.teacher(project["teacherEmail"])
        del project["teacherEmail"]
        return project
    
    def studentProjects(self, email):
        return self.queryAll("SELECT pcode FROM Works_On WHERE email = %s", (email, ))
    
    def coauthors(self, email):
        query = "SELECT distinct other.studentEmail email FROM Works_On self, Works_On other WHERE self.pcode = other.pcode AND self.studentEmail = %s AND other.studentEmail <> self.studentEmail"
        return [self.student(i["email"]) for i in self.queryAll(query, (email,)) if self.isStudent(i["email"])]
        