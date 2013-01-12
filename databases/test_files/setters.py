def setpassword(self, password):
    curs.execute("UPDATE users SET password = {} WHERE username = {};".format(password, self.username))
    curs.commit()
    return()




def setemail(self, email):
    curs.execute("UPDATE users SET email = {} WHERE username = {};").format(email, self.username))
    curs.commit()
    return()
