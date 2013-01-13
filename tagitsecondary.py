#import yoloswag
from tornado import Server
import sqlite3
from template_language import *
from db import *

error_dict = {
    '1':'You\'re already logged in!',
    '2':'No passwords have been entered',
    '3':'',
    '4':'Incorrect Password'
    }

##f = open('template/index.html', 'rU')
##index_html = f.read()
##f.close()
#make variables so that later when we create a better sign up form, we'll change it to use the variables from the database
firstname,lastname, email, country, sex, age = "", "", "", "", "", 0

def createlogin(response):
    if response.get_secure_cookie('tag_it'):#check if we have the tag_it cookie (are we logged in?), so the user can't log in.
        response.redirect('/?error=1') #in the future make it so it gives you the option to log out(delete cookies), and list who you're logged in as - allowing the user to create an account
    else:
        username = response.get_field('username')
        password = response.get_field('password')
        password_check = response.get_field('password_check')
        email = response.get_field('email')
        first_name = response.get_field('first_name')
        last_name = response.get_field('last_name')
        
        if(password_check == password and password_check is not None and username is not None):     #check if the two password fields are the same
            username_user = User.create(username, password, first_name, last_name, email, None, None, None) 
            response.set_secure_cookie('tag_it', username)  #make the user log in after sign-up
            response.redirect('/')
        elif(password_check is None and password is None):
            response.redirect('/?error=2')
        else:
            response.redirect('/?error=3')
        
        
def index(response):
    context = {'message': None}
    error = response.get_field('error')
    
    if error and error in error_dict:
        context['message'] = error_dict[error]

    response.write(render('template/index.html', context))


def login(response):

    if response.get_secure_cookie('tag_it'):
        response.redirect('/?error=1')
    else:
        loginusername = response.get_field('username')
        loginpassword = response.get_field('password')

        databasepassword = User.find(loginusername).getpassword()
        if loginpassword == databasepassword:
            response.set_secure_cookie('tag_it', loginusername)
            response.redirect('/')
        else:
            response.redirect('/?error=4')


server = Server()
server.register('/login', login)
server.register('/register', createlogin)
server.register('/', index)


server.run()



