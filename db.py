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
        self.age = 0
        
    @staticmethod        
    def create(username, password, firstname, lastname, email, country, sex, age):
        curs.execute("INSERT INTO users VALUES (?,?,' ',?,?,?,?,?,?)", (username, password, firstname, lastname, email, country, sex, age))
        conn.commit()
        return User(username)

    @staticmethod
    def find(username):
        curs.execute("SELECT * FROM users WHERE username = ?", (username))
        result =  curs.fetchone()
        if result: 
            username, password, profilepicurl, firstname, lastname, email, country, sex, age = result
            return User(username, password, profilepicurl, firstname, lastname, email, country, sex, age)
        else:
            return None
    
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

    def addfriend(self, friend):
        curs.execute("INSERT INTO friends VALUES (?,?)", (self.username, friend))
        conn.commit()
        return

    def delfriend(self, friend):
        curs.execute("DELETE FROM friends WHERE username = ? AND friend = ?", (self.username, friend))
        conn.commit()
        return

    def listfriends(self):
        curs.execute("SELECT friend FROM friends WHERE username = ?", (self.username))
        self.friend = curs.fetchall()
        return self.friend

    def ifuserexists(self):
        result = curs.execute("SELECT COUNT(*) FROM users WHERE username = ?", (self.username)).fetchone()[0]
        if result == "0":
            return False
        else:
            return True

    def firstnamesearch(self, firstname):
        result = curs.execute("SELECT * FROM users WHERE firstname = ?", (firstname)).fetchall()
        return result

    def lastnamesearch(self, lastname):
        result = curs.execute("SELECT * FROM users WHERE lastname = ?", (lastname)).fetchall()
        return result

    def lastnamesearch(self, lastname):
        result = curs.execute("SELECT * FROM users WHERE lastname = ?", (lastname)).fetchall()
        return result

    def locationsearch(self, country):
        result = curs.execute("SELECT * FROM users WHERE country = ?", (country)).fetchall()
        return result

class Photo():
    def __init__(self, id, location, description, uploader, uploaddate, caption, artist, url):
        self.id = id
        self.location = None
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
        curs.execute("UPDATE users SET profilepicurl = ? WHERE id = ?", (profilepicurl, self.id))
        conn.commit()
        return
    ## Do we need this?
    def getallprofilepicurl(self):
        curs.execute("SELECT profilepicurl FROM photos WHERE id = ?", (self.id))
        self.profilepicurl = curs.fetchall()
        return self.profilepicurl

    def getlocation(self):
        curs.execute("SELECT latitude, longitude FROM photos WHERE id = ?", (self.id))
        self.location = curs.fetchone()
        return self.location

    @staticmethod
    def getallpics():
        piclist = []
        curs.execute("SELECT * FROM photos")
        for i in curs.fetchall():
            id, lat, long, description, uploader, uploaddate, caption, artist, url = i
            currentpicture = Photo(id, (lat, long), description, uploader, uploaddate, caption, artist, url)
            piclist.append(currentpicture)
        return piclist

class Tag():
    def __init__(self, tagid):
        self.tagid = tagid
        self.tagstring = None
        self.photoid = None
        self.tagger = None

    def create(self, tagid, tagstring, photoid, tagger):
        curs.execute("INSERT INTO tags VALUES (?,?,?,?)", (tagid, tagstring, photoid, tagger))
        conn.commit()
        return

    def gettagid(self, tagid):
        curs.execute("SELECT tagid FROM tags WHERE tagid = ?", (self.tagid))
        self.tagid = curs.fetchone()[0]
        
    def getalltagstring(self):
        pass
    
    def getallphoto(self, tagstring):
        pass
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
