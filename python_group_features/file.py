from tornado import Server

def home(response):
    response.write("butts")

def upload(response):
    response.write("""
<!doctype html>
    <html>
        <head></head>
        <body>
            <form id="login" method="post" enctype="multipart/form-data">
                <input type="file" name="upload_image"></br>
                <input type="submit" name="Submit" value="Upload Image"></br>
            </form>
        </body>
    <html>
""")
    
    filename, content_type, data = response.get_file('upload_image')
    if filename:        
        with open("/static/"+filename, 'wb') as f:
            f.write(data)

           
def view(response):
    response.write("""
<!doctype html>
    <html>
        <body>
            <div>
                <img src = "/static/nyan2.gif">
                </div>
        </body>
    </html>
    
        
""")
     
server = Server()
server.register("/upload", upload)
server.register("/view", view)
server.run()
