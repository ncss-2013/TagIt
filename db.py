import sqlite3
conn = sqlite3.connect("database.db")
curs = conn.cursor()

class User():
    def __init__(self, username, password, profilepicurl, firstname, lastname, email, country, sex, age):
        self.username = username
        self.password = password
        self.profilepicurl = profilepicurl
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.country = country
        self.sex = sex
        self.age = age
        
    @staticmethod        
    def create(username, password, firstname, lastname, email, country, sex, age):
        curs.execute("INSERT INTO users VALUES (?,?,' ',?,?,?,?,?,?)", (username, password, firstname, lastname, email, country, sex, age))
        conn.commit()
        return User(username)

    @staticmethod
    def find(username):
        curs.execute("SELECT * FROM users WHERE username = ?", (username,))
        username, password, profilepicurl, firstname, lastname, email, country, sex, age = curs.fetchone()
        return User(username, password, profilepicurl, firstname, lastname, email, country, sex, age)
    
    def getpassword(self):
        return self.password
    
    def getprofilepicurl(self):
        return self.profilepicurl

    def getfirstname(self):
        return self.firstname

    def getlastname(self):
        return self.lastname
    
    def getcountry(self):
        return self.country

    def getsex(self):
        return self.sex

    def getemail(self):
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
