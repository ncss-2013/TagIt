DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS photos;
CREATE TABLE users(
    username TEXT PRIMARY KEY, 
    password TEXT,
    profilepicurl TEXT,
    firstname TEXT,
    lastname TEXT,
    email TEXT,
    country TEXT,
    sex TEXT,
    age INT, 
    CONSTRAINT user_check UNIQUE (username,email),
    CONSTRAINT gender_check CHECK (sex IN ("M","F"))
);

CREATE TABLE photos (
    id INT PRIMARY KEY AUTOINCREMENT,
    latitude FLOAT,
    longitude FLOAT,
    description TEXT,
    uploader TEXT,
    uploaddate DATE(INT),
    caption TEXT,
    artist TEXT,
    friend TEXT,
    url TEXT,
    CONSTRAINTS on id
    FOREIGN KEY (uploader) REFERENCES users(username)
 );
 
 CREATE TABLE comments (
    id INT PRIMARY KEY AUTOINCREMENT,
    uploaddate DATE(INT),
    comstring TEXT,
    commenter TEXT,
    photoid INT,
    FOREIGN KEY (photoid) REFERENCES photos(id)
 );
 
 CREATE TABLE artists (
    /*(if username is null, not registered, if username not null...) registered BOOLEAN,*/
    username TEXT,
    
    FOREIGN KEY (username) REFERENCES users(username)
 );
 
 CREATE TABLE tags (
    tagid INT,
    tagstring TEXT,
    tagtype BOOLEAN,
); 
 
 
 
 
 /* CREATE TABLE comments (
    photoid INT,
    FOREIGN KEY (photoid) REFERENCES photos(id)
 */
    /*
            Photos = URL
        Photos = Location 
        Photos = Description
        Photos = Uploader
        Photos = Date 
        Photos = Caption
        Photos = Tagging of Artist
        Photos = Tagging of Friends
        Photos = ID Field
        CONSTRAINTS on ID
        FOREIGN KEY (Uploader) REFERENCES users(username)
       */
INSERT INTO users VALUES ("Caspar_User", "Caspar_password", "Caspar", "Blattmann", "casper@email.com", "Turkey", "M", 32);
INSERT INTO users VALUES ("Jess_User", "Jess_password", "Jess", "D'Ali", "dali@email.com", "France", "F", 18);
INSERT INTO users VALUES ("Alex_User", "Alex_password", "Alex", "Harper", "alex@email.com", "Germany", "M", 24);

INSERT INTO photos VALUES (1,-33.1,151.2,"blah","Caspar_User",date('now'),"blah_short","Tim","tim.com");
INSERT INTO photos VALUES (2,33,130.5,"this is a cool photo", "Jess_USer",date('now'),"sdfakasdf","Smezza","smezza.com");