import sqlite3

conn = sqlite3.connect("database.db")
curs = conn.cursor()

class User():
    def __init__(self, username):
        self.username = username
        self.password = None
        self.profilepicurl = None
        self.firstname = None
        self.lastname = None
        self.email = None
        self.country = None
        self.sex = None
        self.age = None

    @staticmethod        
    def create(username, password, firstname, lastname, email, country, sex, age):
##        curs.execute("INSERT INTO users VALUES ('" + str(username) + "', '" + str(password) + "', '" + str(None) + "', '" + str(firstname) + "', '" + str(lastname) + "', '" + str(email) + "', '" + str(country) + "', '" + str(sex) + "', " + str(age) +");")
        curs.execute("INSERT INTO users VALUES (?,?,NULL,?,?,?,?,?,?)", (username, password, firstname, lastname, email, country, sex, age))
        conn.commit()
        return User(username)

    def getpassword(self):
        #print(self.username)
        curs.execute("SELECT password FROM users WHERE username = ?", (self.username,))
        self.password = curs.fetchone()[0]
        return self.password
    
    def getprofilepicurl(self):
        curs.execute("SELECT profilepicurl FROM users WHERE username = ?", (self.username,))
        self.profilepicurl = curs.fetchone()[0]
        return self.profilepicurl

    def getfirstname(self):
        curs.execute("SELECT firstname FROM users WHERE username = ?", (self.username,))
        self.firstname = curs.fetchone()[0]
        return self.firstname

    def getlastname(self):
        curs.execute("SELECT lastname FROM users WHERE username = ?", (self.username,))
        self.lastname = curs.fetchone()[0]
        return self.lastname
    
    def getcountry(self):
        curs.execute("SELECT country FROM users WHERE username = ?", (self.username,))
        self.country = curs.fetchone()[0]
        return self.country

    def getsex(self):
        curs.execute("SELECT sex FROM users WHERE username = ?", (self.username,))
        self.sex = curs.fetchone()[0]
        return self.sex

    def getemail(self):
        curs.execute("SELECT email FROM users WHERE username = ?", (self.username,))
        self.email = curs.fetchone()[0]
        return self.email

    def setpassword(self, password):
        curs.execute("UPDATE users SET password = ? WHERE username = ?", (password, self.username))
        conn.commit()
        return

    def setemail(self, email):
        curs.execute("UPDATE users SET email = ? WHERE username = ?", (email, self.username))
        conn.commit()
        return

    def setcountry(self, location):
        curs.execute("UPDATE users SET country = ? WHERE username = ?", (country, self.username))
        conn.commit()
        return

class Photo():
    def __init__(self, id):
        self.id = id
        self.latitude = None
        self.longitude = None
        self.description = None
        self.uploader = None
        self.uploaddate = None
        self.caption = None
        self.artist = None
        self.url = None
        self.allpics = None

    @staticmethod
    def create(uploader, uploaddate, caption, artist, url, latitude=None, longitude=None, description=None):
        curs.execute("INSERT INTO photos VALUES (?,?,?,?,?,?,?,?)", (latitude, longitude, description, uploader, uploaddate, caption, artist, url))
        conn.commit()
        return
    
    def setprofilepicurl(self, profilepicurl):
        curs.execute("UPDATE users SET profilepicurl = ? WHERE id = ?", profilepicurl, self.id)
        conn.commit()
        return
    ## Do we need this?
    def getallprofilepicurl(self,):
        curs.execute("SELECT profilepicurl FROM photos WHERE id = ?", self.id)
        self.profilepicurl = curs.fetchall()

    def getlocation(self):
        curs.execute("SELECT longitude FROM photos WHERE id = ?", self.id)

    def getallphotos(self):
        curs.execute("SELECT url FROM photos WHERE id = ?", self.id)
        self.url = curs.fetch()
        return self.url

    def getallpics(self):
        curs.execute("SELECT * url FROM photos")
        self.allpics = curs.fetchall()
        return self.allpics
    
    ## RETURN LIST
##    def getpics(self, criteria, order, limit):
##        curs.execute("SELECT url FROM photos WHERE ? ORDER BY ? DESC LIMIT ?", expression, order, limit)
##        self.url = curs.fetchall()
##        return self.url
##


##testuser = User("Jess_User")
##print(testuser.getfirstname() + " " + testuser.getlastname())
##print(testuser.getpassword())
##testuser.setpassword("23456")
##print(testuser.getpassword())
