#import yoloswag
from tornado import Server
import sqlite3
from template_language import *
from db import *
import os
from functions import *
import cgitb

error_dict = {
    '1':'You\'re already logged in!',
    '2':'No passwords have been entered',
    '3':'',
    '4':'Incorrect Password'
    }

cgitb.enable()

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


def index(response):
    context = make_context(response)
    context['message'] = None
    context['cookie'] = 'lol'
    error = response.get_field('error')

    if error and error in error_dict:
        context['message'] = error_dict[error]
  
    response.write(render('template/index.html', context))


def upload(response):
    response.write(create("""
{% include template/header.html %}
<p style='font-color:black;'>
            <a href = "/"> Home <a>
            <form id="upload" method="post" enctype="multipart/form-data">
                <input type="file" name="upload_image"></br>
                <input type="text" name="tags"> Tags (seperated by spaces, cases are irrelevant) </input><br>
                <input type="text" name="description" style="width:400px; height:75px;"> Description</input><BR>
                <input type="submit" name="Submit" value="Upload Image"></br>
                <a href = "/piclist"> piclist <a>
            </form>
            </p>
        </body>
    <html>
""", {}))

    # response.write(render('template/upload.html', context))

    # create new fields and fill them
    # with the fields of the response.get_file tuple
    # This allows us to use each individually
    filename, content_type, data = response.get_file('upload_image')

    #retrieve the input tags
    tags = response.get_field('tags')
    description = response.get_field('description')
    
    #checks if there is a file in the request
    # print(Photo.getnextid())
    if filename:
        #open and create a new file within
        #static folder (static is safe)
        #we are writing raw bytes to file (that's how the site will recieve them)      
        with open("static/uploads/images/"+str(Photo.getnextid()[0][0])+".jpg" , 'wb') as f:

            #write the raw data we got from the tuple to the file
            
            f.write(data)

        Photo.create("authorname","0",filename,"banksy", "static/uploads/images/"+str(Photo.getnextid()[0][0])+".jpg","1","1",description)
                     
        with open("static/uploads/tags/"+ filename.replace('.', '')+".txt", "w") as t:

            t.write(tags)

def photostream(response):
    photos = Photo(None).getallpics()
    print(photos)
    context = make_context()
    context['photos'] = photos
    response.write(render('template/stream.html', context))
        
def loggedout(response): #Loggedout page, delete cookies here
    response.clear_cookie('tag_it')
    response.redirect('/home')

def friends (response):
    context = make_context(response)
    response.write(render('template/friends.html',context))

def template_sample(response):
#    context = { 'logged_in': False}
#    context = { 'name':'Smerity', 'friends':['Ruby','Casper','Ted','Asem'], 'logged_in': True}
    context = { 'name':'Smerity', 'friends':[], 'logged_in': True}
    response.write(render('template/workshop_example.html',context))

def profile(response):
    context = make_context(response)
    response.write(render('template/profile.html', context))
     
server = Server()
server.register("/", index)
server.register("/home", index)
server.register("/upload", upload)
server.register('/createlogin', createlogin)
server.register('/login', login)
server.register('/loggedout', loggedout)
server.register('/stream', photostream)
server.register('/profile', profile)
server.register('/template_sample', template_sample)
server.register('/friends', friends)
server.register('/logout', loggedout)
server.run()
