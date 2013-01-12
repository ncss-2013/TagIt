from tornado import Server
from http.cookies import SimpleCookie

import cgitb
cgitb.enable()

def index(response): #Index
    if response.get_secure_cookie('login_cookie'):
        username_from_cookie = response.get_secure_cookie('login_cookie')
        response.write("Hello ")
        response.write(username_from_cookie)
        response.write('''
        <!doctype html>
        <html>
            <head></head>
            <title>TagIt</title>
            <body>
            <br />
            <button type = "button"
                    name = "logout"
                    value = "Logout"
                    onclick = "window.location.href='http://localhost:8888/loggedout'">
                    Logout
                    </button>
            </body>
        </html>''')

        logout = response.get_field('logout')
    else:
        response.write("Generic home page")

def login(response): #Login page
    if response.get_secure_cookie('login_cookie'):
        username_from_cookie = response.get_secure_cookie('login_cookie')
        response.write("You are already logged in, ")
        response.write(username_from_cookie)
    else: #Here we enter the link to the HTML login page
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
                <br />
                Current username and password are 'chicken' and 'egg' . Working on database interaction
                <br />
            </body>
        <html>''')
        username = response.get_field('username')
        password = response.get_field('password')

        #Here we need to connect and check with the database
        #Need to ensure against SQL injection attacks(?)
        if username == 'chicken':
            if password == 'egg':
                response.set_secure_cookie('login_cookie', username)
                response.write('Welcome back, ' + username + ".")
        elif username and not password:
            response.write('Please ensure you enter a password')
        elif not username and password:
            response.write('Please enter a username and a password')

def loggedout(response): #Loggedout page, delete cookies here
    response.clear_cookie('login_cookie')
    response.redirect('/')

def upload(response): #Image upload page
    response.write("<title>Upload an image</title>Yeah we're throwing science at walls here people")

server = Server()
server.register('/', index)
server.register('/login', login)
server.register('/loggedout', loggedout)
server.register('/upload', upload)
server.run()

#To logout user, delete their cookie and then check
#if the cookie is still there. Display page accordingly
