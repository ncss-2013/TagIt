
def getcountry(self):
    curs.execute("SELECT country FROM users WHERE username = '{}'".format(self.username))
    slef.country = curs.fetchone()[0]
    return self.country

def getsex(self):
    curs.execute("SELECT sex FROM users WHERE username = '{}'".format(self.username))
    slef.sex = curs.fetchone()[0]
    return self.sex
                 
def getcountry(self):
    curs.execute("SELECT age FROM users WHERE username = '{}'".format(self.username))
    slef.age = curs.fetchone()[0]
    return self.age

def getemail(self):
    curs.execute("SELECT email FROM users WHERE username = '{}'".format(self.username))
    slef.email = curs.fetchone()[0]
    return self.email
