from tornado import Server

def index(response, args):
    if response.get_secure_cookie(args):
        response.write("You're logged in!")
    else:
        response.write("You aren't logged in. :(")

def login(response):
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
        username = response.get_field('username')
        password = response.get_field('password')
        
        if username == 'chicken' :
            if password == 'egg':
                response.set_secure_cookie('tag_it', username)
                response.write('Well done, you are logged in as: ' + username + ':' + password)
            else:
                response.write('Incorrect Password. Try again by pressing back on your browser')
        elif username != None:
            response.write('Incorrect Password. Try again by pressing back on your browser')

def logout(response):
    if response.get_secure_cookie('tag_it', username):
        ##################CLEARCOOKIES##################
        self.clear_cookie("tag_it", username)
    else:
        response.write("you have made no changes")

server = Server()
server.register('/profile/(.+)', index, username)
server.register('/login/', login)
server.register('/logout/', logout)

server.run()
