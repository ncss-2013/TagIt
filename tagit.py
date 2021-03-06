#import yoloswag
from tornado import Server
import sqlite3
from template_language import *
from db import *
from functions import *
import os
import cgitb

error_dict = {
    '1':'You\'re already logged in!',
    '2':'No passwords have been entered',
    '3':'',
    '4':'Incorrect Username/Password'
    }

cgitb.enable()


def createlogin(response):
    if response.get_secure_cookie('tag_it'):#check if we have the tag_it cookie (are we logged in?), so the user can't log in.
        response.redirect('/?error=1') #in the future make it so it gives you the option to log out(delete cookies), and list who you're logged in as - allowing the user to create an account
    else:
        first_name = response.get_field('first_name')
        last_name = response.get_field('last_name')
        email = response.get_field('email')
        username = response.get_field('username')
        password = response.get_field('password')
        country = response.get_field('country')
        sex = response.get_field('sex')
        if sex not in ["M", "F"]:
            sex = None
        age = response.get_field('age')
        password_check = response.get_field('password_check')
        print(first_name, last_name, email, username, password, password_check)                      

        if(password_check == password and password_check is not None and username is not None):     #check if the two password fields are the same
            username_user = User.create(username, password, None, first_name, last_name, email, country=country, sex=sex, age=age) 
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
        if (User.find(loginusername)):
            databasepassword = User.find(loginusername).getpassword()
            if loginpassword == databasepassword:
                response.set_secure_cookie('tag_it', loginusername)
                response.redirect('/')
            else:
                response.redirect('/?error=4')
        else:
                response.redirect('/?error=4')

def index(response):
    context = make_context(response)
    context['message'] = None

    if context["is_logged_in"]:
        response.redirect('/stream')
    
    error = response.get_field('error')

    if error and error in error_dict:
        context['message'] = error_dict[error]
  
    response.write(render('template/index.html', context))


def upload(response):
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
        context = make_context(response)
        photo = Photo.create(uploader=context['username'],url=filename,caption=description,description=description)
        with open("static/uploads/images/"+str(photo.id)+".jpg" , 'wb') as f:
            #write the raw data we got from the tuple to the file
            f.write(data)
         
        #with open("static/uploads/tags/"+ filename.replace('.', '')+".txt", "w") as t:
        #    t.write(tags)
            
    response.redirect('/stream')

def photostream(response):
    photos = Photo.getallpics()
    context = make_context(response)
    context['photos'] = photos
    response.write(render('template/stream.html', context))

        
def loggedout(response): #Loggedout page, delete cookies here
    response.clear_cookie('tag_it')
    response.redirect('/')


def friends (response):
    context = make_context(response)
    response.write(render('template/friends.html',context))


##def template_sample(response):
###    context = { 'logged_in': False}
###    context = { 'name':'Smerity', 'friends':['Ruby','Casper','Ted','Asem'], 'logged_in': True}
##    context = { 'name':'Smerity', 'friends':[], 'logged_in': True}
##    response.write(render('template/workshop_example.html',context))


def profile(response, user):
    context = make_context(response)
    context['user'] = User.find(user)
    if context['user']:
        photos = Photo.getpicsbyusername(user)
        import hashlib
        context['is_friend'] = User(context['username']).isfriends(user)
        #context["user_image"] = "http://www.gravatar.com/avatar/" + hashlib.md5("smerity@smerity.com".encode("utf-8")).hexdigest() + "?s=200"
        context["user_image"] = context['user'].get_picture() + "&s=200"
        context['photos'] = photos
        response.write(render('template/profile.html', context))

def addfriend(response, other_user):
    context = make_context(response)
    if context [ 'is_logged_in' ] == True:
        # TODO: Ensure other_user is a real user
        friend = other_user
        User(context["username"]).addfriend(friend)
        response.redirect('/profile/'+friend) #profile stuff   DO NOT COMMIT
    else:
        response.redirect('/?error=6')

def friends(response):
    context = make_context(response)
    if context [ 'is_logged_in' ] == True:
        context["friends"] = User(context["username"]).listfriends()
    response.write(render('template/friends.html',context))

def delfriend(response, other_user):
    context = make_context(response)
    if context [ 'is_logged_in' ] == True:
        listfriends = User(context["username"]).listfriends()\

        friend_names = []
        for friend in listfriends:
            friend_names.append(friend.username)

        if other_user in friend_names:
            User(context["username"]).delfriend(other_user)
            response.redirect('/profile/'+other_user)
     
server = Server()
server.register("/", index)
server.register("/home", index)
server.register("/upload", upload)
server.register('/createlogin', createlogin)
server.register('/login', login)
server.register('/stream', photostream)
server.register('/profile/(.+)', profile)
##server.register('/template_sample', template_sample)
server.register('/friends', friends)
server.register('/addfriend/(.+)', addfriend)
server.register('/delfriend/(.+)', delfriend)
server.register('/logout', loggedout)
server.run()
