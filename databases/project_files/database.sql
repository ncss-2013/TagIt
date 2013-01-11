/*DROP TABLE IF EXISTS users;*/
CREATE TABLE users(
    username TEXT PRIMARY KEY, 
    password TEXT,
    firstname TEXT,
    lastname TEXT,
    email TEXT,
    country TEXT,
    sex BLOB,
    age INTEGER, 
    CONSTRAINT user_check UNIQUE (username,email)  
);

/*INSERT INTO users VALUES ("Caspar_User", "Caspar_password", "Caspar", "Blattmann", "casper@email.com", "Turkey", 32);
INSERT INTO users VALUES ("Jess_User", "Jess_password", "Jess", "D'Ali", "dali@email.com", "France", 18);
INSERT INTO users VALUES ("Alex_User", "Alex_password", "Alex", "Harper", "alex@email.com", "Germany", 24);*/