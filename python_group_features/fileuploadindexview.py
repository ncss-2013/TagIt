from tornado import Server
import os

def home(response):
    response.write("""
<!doctype html>
    <html>
        <body>
            <p>
                   current pages avaliable are <a href = "/upload" >/upload</a> and <a href = "/index"> /index <a>
            </p>
        </body>
    <html>
                   """)

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

        with open("static/uploads/tags"+ filename.replace('.', '')+".txt", "w") as t:

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

     
server = Server()
server.register("/home", home)
server.register("/upload", upload)
server.register("/view/(.+)", view)
server.register("/index", index)
server.run()