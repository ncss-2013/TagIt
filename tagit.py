#
from tornado import Server
import os

import sqlite3

import cgitb
cgitb.enable()

f = open('index.html', 'r')
index_html = f.read()
f.close()
#make variables so that later when we create a better sign up form, we'll change it to use the variables from the database
firstname,lastname, email, country, sex, age = "", "", "", "", "", 0

def createlogin(response):
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


def login2(response):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    if response.get_secure_cookie('tag_it'):
        response.write('You\'re already logged in')
    else:
        response.write('''
        <!doctype html>
        <html>
            <head></head>
            <body>
                <form id="login" method='POST'>
                    <input type="text" name="username"> Username </input>
                    <input type="password" name="password"> Password </input>
                    <input type="submit" name="submit" value="Submit">
                </form>
            </body>
        <html>''')
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
        



def home(response):
    if response.get_secure_cookie('tag_it'):
        #Cookie exists, display the logout button
        username_from_cookie = response.get_secure_cookie('tag_it')
        response.write("Hello ")
        response.write(username_from_cookie)
        response.write('''
        <!doctype html>
        <html>
            <head></head>
            <title>Tag It</title>
            <body>
            <br />
            <button type = "button"
                    name = "logout"
                    value = "Logout"
                    onclick = "window.location.href='loggedout'">
                    Logout
                    </button>
                    <p>
                            current pages avaliable are <a href = "upload" >/upload</a>, <a href = "/stream" >the photostream</a> and <a href = "/piclist"> piclist <a>
                    </p>
            </body>
        </html>''')

    else:
        #Cookie does not exist, display the login page
        #Send the form to the '/login' page to process
        response.write('''
        <!doctype html>
        <html>
            <title>Tag it</title>
            <head></head>
            <body>
                <form action="/login" id="login" method='POST'>
                    <input type="text" name="username"> Username </input>
                    <input type="password" name="password"> Password </input>
                    <input type="submit" name="submit" value="Submit" </input>
                </form>
                Current username and password are 'chicken' and 'egg' . Working on database interaction
                <p>
                   current pages avaliable are <a href = "/piclist"> piclist <a> and <a href = "/stream" >the photostream</a>
                </p>
            </body>
        <html>''')


def upload(response):
    response.write("""
<!doctype html>
    <html>
        <head></head>
        <body>
            <a href = "/home"> Home <a>
            <form id="upload" method="post" enctype="multipart/form-data">
                <input type="file" name="upload_image"></br>
                <input type="text" name="tags"> Tags (seperated by spaces, cases are irrelevant) </input>
                <input type="submit" name="Submit" value="Upload Image"></br>
            </form>
        </body>
    <html>
""")

    # create new fields and fill them
    # with the fields of the response.get_file tuple
    # This allows us to use each individually
    
    filename, content_type, data = response.get_file('upload_image')

    #retrieve the input tags
    tags = response.get_field('tags')
    
    
    #checks if there is a file in the request
    
    if filename:
        
        #open and create a new file within
        #static folder (static is safe)
        #we are writing raw bytes to file (that's how the site will recieve them)
        
        with open("static/uploads/images/"+filename, 'wb') as f:

            #write the raw data we got from the tuple to the file
            
            f.write(data)

        with open("static/uploads/tags/"+ filename.replace('.', '')+".txt", "w") as t:

            t.write(tags)

#in the future we will need to ensure data is stored by ID, not filename
#this will prevent conflicts

           
def view(response, name):
    response.write("""
<!doctype html>
    <html>
        <body>
            <a href = "/home"> home <a>
            <div>
                <img src = "/static/uploads/images/"""+name+"""">
                <p>
                """"""
                </p>
                </div>
        </body>
    </html>
    
        
""")

def photostream(response):
    response.write("""
<!doctype html>
    <html>
        <body>
            <a href = "/home"> home <a>
            <div>""")
    for file in os.listdir("static/uploads/images"):
        response.write("""<img src = "/static/uploads/images/"""+file+""""><br>""")
    response.write("""<p>
                
            </p>
            </div>
        </body>
    </html>"""
    )
        


def piclist(response):
    response.write("""<!doctype html>
    <html>
        <body>
        <a href = "/home"> Home <a>
            <div>
                <p>""")
    for file in os.listdir("static/uploads/images"):
        response.write("<a href = /view/" + file + ">" + file +"</a></br>")
    response.write("""
                </p>
            </div>
        </body>
    <html>
""")

def login(response): #Login page
    username = response.get_field('username')
    password = response.get_field('password')
    #Here we need to connect and check with the database
    #Need to ensure against SQL injection attacks(?)
    if username == 'chicken' and password == 'egg':
        response.set_secure_cookie('tag_it', username)
        response.redirect('/home')
    else:
        response.redirect('/home')
    

def loggedout(response): #Loggedout page, delete cookies here
    response.clear_cookie('tag_it')
    response.redirect('/home')


     
server = Server()
server.register("/home", home)
server.register("/upload", upload)
server.register("/view/(.+)", view)
server.register("/piclist", piclist)
server.register('/login2', login2)
server.register('/createlogin', createlogin)
server.register('/login', login)
server.register('/loggedout', loggedout)
server.register('/stream', photostream)
server.run()
