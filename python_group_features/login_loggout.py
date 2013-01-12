from tornado import Server
from http.cookies import SimpleCookie

import cgitb
cgitb.enable()

def index(response): #Index
    if response.get_secure_cookie('login_cookie'):
        #Cookie exists, display the logout button
        username_from_cookie = response.get_secure_cookie('login_cookie')
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
            </body>
        <html>''')

def login(response): #Login page
    username = response.get_field('username')
    password = response.get_field('password')
    #Here we need to connect and check with the database
    #Need to ensure against SQL injection attacks(?)
    if username == 'chicken' and password == 'egg':
        response.set_secure_cookie('login_cookie', username)
        response.redirect('/')
    else:
        response.redirect('/')
    

def loggedout(response): #Loggedout page, delete cookies here
    response.clear_cookie('login_cookie')
    response.redirect('/')

server = Server()
server.register('/', index)
server.register('/login', login)
server.register('/loggedout', loggedout)
server.run()

#Yeah we're just throwing science at walls here people"
