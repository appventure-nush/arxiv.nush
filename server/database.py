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
        
    def isStudent(self, email):
        return len(self.queryAll("SELECT email FROM Student WHERE email = %s", (email, ))) > 0
        
    def student(self, email):
        query = "SELECT email, name, gradYear, nush_sid, pfp FROM NUSHStudent NATURAL JOIN Student WHERE email = %s"
        return self.queryOne(query, (email, ))
    
    def teacher(self, email):
        return self.queryOne("SELECT * FROM Institution WHERE email = %s", (email, ))
    
    def institute(self, instId):
        return self.queryOne("SELECT * FROM Institution WHERE instId = %s", (instId, ))
    
    def projectMembers(self, pcode):
        query = "SELECT studentEmail email FROM Works_On WHERE pcode = %s"
        return [self.student(i["email"]) for i in self.queryAll(query, (pcode,))]
    
    def project(self, pcode):
        return self.queryOne("SELECT * FROM Project WHERE pcode = %s", (pcode, ))
    
    def studentProjects(self, email):
        return self.queryAll("SELECT pcode FROM Works_On WHERE email = %s", (email, ))
    
    def coauthors(self, email):
        query = "SELECT distinct other.studentEmail email FROM Works_On self, Works_On other WHERE self.pcode = other.pcode AND self.studentEmail = %s AND other.studentEmail <> self.studentEmail"
        return [self.student(i["email"]) for i in self.queryAll(query, (email,)) if self.isStudent(i["email"])]
        