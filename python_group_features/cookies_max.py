from tornado import Server
from http.cookies import SimpleCookie

import cgitb
cgitb.enable()

def index(response): #Index
    if response.get_secure_cookie('login_cookie'):
        response.write("Home page for logged in user should appear here")
    else:
        response.write("Generic home page")

def login(response): #Login page
    if response.get_secure_cookie('login_cookie'):
        username_from_cookie = response.get_secure_cookie('login_cookie')
        response.write("You are already logged in, ")
        response.write(username_from_cookie)
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
        username = response.get_field('username')
        password = response.get_field('password')

        #To logout user, delete their cookie and then check
        #if the cookie is still there. Display page accordingly
        
        if username == 'chicken' :
            if password == 'egg':
                response.set_secure_cookie('login_cookie', username)
                response.write('Welcome back, ' + username + ".")
            else:
                response.write('Incorrect Password. Try again by pressing back on your browser')
        elif username != None:
            response.write('Incorrect Password. Try again by pressing back on your browser')

def upload(response): #Image upload page
    response.write("<title>Upload an image</title>Yeah we're throwing science at walls here people")

server = Server()
server.register('/', index)
server.register('/login', login)
server.register('/upload', upload)
server.run()
