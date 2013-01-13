#import yoloswag
from tornado import Server
import sqlite3
from template_language import *
from db import *
import os
import cgitb

error_dict = {
    '1':'You\'re already logged in!',
    '2':'No passwords have been entered',
    '3':'',
    '4':'Incorrect Password'
    }

cgitb.enable()


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
    context = {'message': None}
    error = response.get_field('error')

    if error and error in error_dict:
        context['message'] = error_dict[error]
  
    response.write(render('template/index.html', context))


def upload(response):
    response.write("""
<!doctype html>
    <html>
        <head></head>
        <body>
            <a href = "/"> Home <a>
            <form id="upload" method="post" enctype="multipart/form-data">
                <input type="file" name="upload_image"></br>
                <input type="text" name="tags"> Tags (seperated by spaces, cases are irrelevant) </input><br>
                <input type="text" name="description" style="width:400px; height:75px;"> Description</input><BR>
                <input type="submit" name="Submit" value="Upload Image"></br>
                <a href = "/piclist"> piclist <a>
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

    description = response.get_field('description')
    
    
    #checks if there is a file in the request
    print(db.Photo.getnextid())
    if filename:
        
        #open and create a new file within
        #static folder (static is safe)
        #we are writing raw bytes to file (that's how the site will recieve them)

        
        
        with open("static/uploads/images/"+str(db.Photo.getnextid()[0][0])+".jpg" , 'wb') as f:

            #write the raw data we got from the tuple to the file
            
            f.write(data)

        db.Photo.create("authorname","0",filename,"banksy", "static/uploads/images/"+str(db.Photo.getnextid()[0][0])+".jpg","1","1",description)
                     
        with open("static/uploads/tags/"+ filename.replace('.', '')+".txt", "w") as t:

            t.write(tags)

#in the future we will need to ensure data is stored by ID, not filename
#this will prevent conflicts

           
def view(response, name):
    response.write("""
<!doctype html>
    <html>
        <body>
            <a href = "/"> Home <a>
            <div>
                <img src = "/static/uploads/images/"""+name+"""">
                </br>
                <a href = "/piclist"> piclist <a>
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
            <div>"""+
#this will eventualy allow parameters
    getallpics()
                
    +"</p></div></body></html>"
    )
        


def piclist(response):
    response.write("""<!doctype html>
    <html>
        <body>
        <a href = "/"> Home <a>
            <div>
                <p>""")
    for file in os.listdir("static/uploads/images"):
        response.write('<a href="/view/' + file + '"><img border=0 height=50 width=50 src="/static/uploads/images/'+file+'"</a></br>')
    response.write("""
                </p>
            </div>
        </body>
    <html>
""")

def loggedout(response): #Loggedout page, delete cookies here
    response.clear_cookie('tag_it')
    response.redirect('/home')

def friends (response):
    context = {}
    response.write(render('template/friends.html',context))

def template_sample(response):
#    context = { 'logged_in': False}
#    context = { 'name':'Smerity', 'friends':['Ruby','Casper','Ted','Asem'], 'logged_in': True}
    context = { 'name':'Smerity', 'friends':[], 'logged_in': True}
    response.write(render('template/workshop_example.html',context))
     
server = Server()
server.register("/", index)
server.register("/upload", upload)
server.register("/view/(.+)", view)
server.register("/piclist", piclist)
#server.register('/login2', login2)
server.register('/createlogin', createlogin)
server.register('/login', login)
server.register('/loggedout', loggedout)
server.register('/stream', photostream)
server.register('/template_sample', template_sample)
server.register('/friends', friends)
server.run()
