DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS photos;
DROP TABLE IF EXISTS artists;
DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS tags;
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
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    latitude FLOAT,
    longitude FLOAT,
    description TEXT,
    uploader TEXT,
    uploaddate DATETIME,
    caption TEXT,
    artist TEXT,
    url TEXT,
    FOREIGN KEY (uploader) REFERENCES users(username)
 );
 
 CREATE TABLE comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uploaddate DATETIME,
    comstring TEXT,
    commenter TEXT,
    photoid INTEGER,
    FOREIGN KEY (photoid) REFERENCES photos(id)
 );
 
 CREATE TABLE artists (
    /*(if username is null, not registered, if username not null...) registered BOOLEAN,*/
    username TEXT,
    FOREIGN KEY (username) REFERENCES users(username)
 );
 
 CREATE TABLE tags (
    tagid INTEGER PRIMARY KEY AUTOINCREMENT,
    tagstring TEXT,
    id INTEGER
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
INSERT INTO users VALUES ("Caspar_User", "Caspar_password", "test.com", "Caspar", "Blattmann", "casper@email.com", "Turkey", "M", 32);
INSERT INTO users VALUES ("Jess_User", "Jess_password", "test.com", "Jess", "D'Ali", "dali@email.com", "France", "F", 18);
INSERT INTO users VALUES ("Alex_User", "Alex_password", "test.com", "Alex", "Harper", "alex@email.com", "Germany", "M", 24);

INSERT INTO photos VALUES (1,-33.1,151.2,"blah","Caspar_User",datetime('now'),"blah_short","Tim", "tim.com");
INSERT INTO photos VALUES (2,33,130.5,"this is a cool photo", "Jess_USer",datetime('now'),"sdfakasdf","Smezza", "smezza.com");



/* how to load sql up
login
cd ncss133/databases/project_files/
sqlite3 database.db
.read database.sql */
