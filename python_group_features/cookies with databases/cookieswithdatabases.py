#import yoloswag
from tornado import Server
import sqlite3
from template_language import *
from db import *

f = open('index.html', 'r')
index_html = f.read()
f.close()
#make variables so that later when we create a better sign up form, we'll change it to use the variables from the database
firstname,lastname, email, country, sex, age = "", "", "", "", "", 0

def createlogin(response):
    user = User.create(username, password)
    user = User.find(username)
    user = User('sam', 'password')
    lastname = user.getlastname()
    #response.write(index_html)             #print the html for the page
    conn = sqlite3.connect("database.db")   
    cursor = conn.cursor()
    if response.get_secure_cookie('tag_it'):#check if we have the tag_it cookie (are we logged in?), so the user can't log in.
        response.write('You\'re already logged in, so you cannot create a new account - YOU HAVE ONE!') #in the future make it so it gives you the option to log out(delete cookies), and list who you're logged in as - allowing the user to create an account
    else:
        response.write(index_html)          #print the submit form only if there is no log in cookie
        username = response.get_field('username')
        password = response.get_field('password')
        password_check = response.get_field('password_check')
        
        if(password_check == password and password_check is not None and username is not None):     #check if the two password fields are the same
            # SQL injection attack! vv
            cursor.execute("INSERT INTO users VALUES ('" + str(username) + "', '" + str(password) + "', '" + str(firstname) + "', '" + str(lastname) + "', '" + str(email) + "', '" + str(country) + "', '" + str(sex) + "', " + str(age) +");")
            conn.commit()
            cursor.close()
            conn.close()
            response.set_secure_cookie('tag_it', username)  #make the user log in after sign up
            response.write("Well done, you created a user: " + username) #
        elif(password_check is None and password is None):
            response.write("Please enter a username/password")
        else:
            response.write("Passwords did not match, please try again")
        

def login(response):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    if response.get_secure_cookie('tag_it'):
        response.write('You\'re already logged in')
    else:
        response.write()
        loginusername = response.get_field('username')
        loginpassword = response.get_field('password')

        cursor.execute("SELECT username, password FROM users WHERE username = '" + str(loginusername) + "'")
        fetched_cursor = cursor.fetchone()
        if (fetched_cursor is not None):
            (databaseusername,databasepassword) = fetched_cursor
            if loginusername == databaseusername:
                if loginpassword == databasepassword:
                    response.set_secure_cookie('tag_it', loginusername)
                    response.write('Well done, you are logged in as: ' + loginusername + ':' + loginpassword)
                else:
                    response.write('Incorrect Password. Try again by pressing back on your browser')
            elif loginusername != None:
                response.write('Incorrect Password. Try again by pressing back on your browser')
        else:
            response.write('Incorrect username/password combination.')
        cursor.close()
        conn.close()
        
        


server = Server()
server.register('/login', login)
server.register('/createlogin', createlogin)


server.run()



