#
from tornado import Server
import os
from http.cookies import SimpleCookie

import cgitb
cgitb.enable()

def home(response):
##    response.write("""
##<!doctype html>
##    <html>
##        <body>
##            <p>
##                   current pages avaliable are <a href = "/upload" >/upload</a> and <a href = "/index"> /index <a>
##            </p>
##        </body>
##    <html>
##                   """)
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
                    onclick = "window.location.href='http://localhost:8888/loggedout'">
                    Logout
                    </button>
                    <p>
                            current pages avaliable are <a href = "/upload" >/upload</a>, <a href = "/stream" >the photostream</a> and <a href = "/index"> /index <a>
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
                   current pages avaliable are <a href = "/index"> /index <a> and <a href = "/stream" >the photostream</a>
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
        


def index(response):
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
server.register("/index", index)
server.register('/login', login)
server.register('/loggedout', loggedout)
server.register('/stream', photostream)
server.run()
