import sqlite3
conn = sqlite3.connect("database.db")
curs = conn.cursor()

class User():
    def __init__(self, username, password=None, profilepicurl=None, firstname=None, lastname=None, email=None, country=None, sex=None, age=None):
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
        curs.execute("INSERT INTO users VALUES (?,?,NULL,?,?,?,?,?,?)", (username, password, firstname, lastname, email, country, sex, age))
        conn.commit()
        return User(username, password, firstname, lastname, email, country, sex, age)

    @staticmethod
    def find(username):
        curs.execute("SELECT * FROM users WHERE username = ?", (username,))
        result =  curs.fetchone()
        if result:
            username, password, firstname, profilepicurl, lastname, email, country, sex, age = result
            return User(username, password, profilepicurl, firstname, lastname, email, country, sex, age)
        else:
            return None
    
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

    def addfriend(self, friend):
        curs.execute("INSERT INTO friends VALUES (?,?)", (self.username, friend))
        conn.commit()
        return

    def delfriend(self, friend):
        curs.execute("DELETE FROM friends WHERE username = ? AND friend = ?", (self.username, friend))
        conn.commit()
        return

    def listfriends(self):
        curs.execute("SELECT friend FROM friends WHERE username = ?", (self.username,))
        self.friend = curs.fetchall()
        return self.friend

    def ifuserexists(self):
        result = curs.execute("SELECT COUNT(*) FROM users WHERE username = ?", (self.username,)).fetchone()[0]
        if result == "0":
            return False
        else:
            return True

    def firstnamesearch(self, firstname):
        result = curs.execute("SELECT * FROM users WHERE firstname = ?", (firstname,)).fetchall()
        return result

    def lastnamesearch(self, lastname):
        result = curs.execute("SELECT * FROM users WHERE lastname = ?", (lastname,)).fetchall()
        return result

    def lastnamesearch(self, lastname):
        result = curs.execute("SELECT * FROM users WHERE lastname = ?", (lastname,)).fetchall()
        return result

    def locationsearch(self, country):
        result = curs.execute("SELECT * FROM users WHERE country = ?", (country,)).fetchall()
        return result

    def __repr__(self):
        return "<User: {}>".format(self.username)

    def __str__(self):
        return self.__repr__()

class Photo():
    def __init__(self, id, latitude, longitude, description, uploader, uploaddate, caption, artist, url):
        self.id = id
        self.latitude = latitude
        self.longitude = longitude
        self.description = description
        self.uploader = uploader
        self.uploaddate = uploaddate
        self.caption = caption
        self.artist = artist
        self.url = url

    @staticmethod
    def create(uploader, caption, url, latitude=None, longitude=None, description=None, artist=None):
        curs.execute("INSERT INTO photos (latitude, longitude, description, uploader, uploaddate, caption, artist, url) VALUES (?,?,?,?,datetime('now'),?,?,?)",
                     (latitude, longitude, description, uploader, caption, artist, url))
        conn.commit()
        curs.execute("SELECT id FROM photos WHERE id == (SELECT max(id) FROM photos)")
        id = curs.fetchone()[0]
        return Photo.find(id)

    @staticmethod
    def find(id):
        curs.execute("SELECT * FROM photos WHERE id = ?", (id,))
        id, latitude, longitude, description, uploader, uploaddate, caption, artist, url = curs.fetchone()
        return Photo(id, latitude, longitude, description, uploader, uploaddate, caption, artist, url)
    
    def setprofilepicurl(self, profilepicurl):
        curs.execute("UPDATE users SET profilepicurl = ? WHERE id = ?", (profilepicurl, self.id))
        conn.commit()

    def getlocation(self):
        return self.location

    @staticmethod
    def getallpics(limit = None):
        if limit == None:
            curs.execute("SELECT * FROM photos")
        else:    
            curs.execute("SELECT * FROM photos LIMIT " + str(int(limit)))

        piclist = []
        for i in curs.fetchall():
            
            id, lat, long, description, uploader, uploaddate, caption, artist, url = i
            currentpicture = Photo(id, lat, long, description, uploader, uploaddate, caption, artist, url)
            piclist.append(currentpicture)
        return piclist # This will print in IDLE

    def __repr__(self):
        return "<Photo: {} ({})>".format(self.caption, self.uploader)

    def __str__(self):
        return self.__repr__()

##     RETURN LIST
##    def getpicsurl(self, criteria, order, limit):
##        curs.execute("SELECT url FROM photos WHERE ? ORDER BY ? DESC LIMIT ?", criteria, order, limit)
##        self.url = curs.fetchall()
##        return self.url




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
        curs.execute("SELECT tagid FROM tags WHERE tagid = ?", (self.tagid,))
        self.tagid = curs.fetchone()[0]
        
    def getalltagstring(self):
        pass
    
    def getallphoto(self, tagstring):
        pass



##testuser = User("Jess_User")
##print(testuser.getfirstname() + " " + testuser.getlastname())
##print(testuser.getpassword())
##testuser.setpassword("23456")
##print(testuser.getpassword())

if __name__ == "__main__":
    testuser = User.find("Jess_User")
    print(testuser)
    p = Photo.create("Smerity", "lolcats", "0.jpg")
    if not User.find("smerity"):
        u = User.create("smerity", "smurdy", None, "Stephen", "Merity", "smerity@smerity.com", None, "M", 18)
    u = User.find("smerity")
