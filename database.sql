 CREATE DATABASE MoneyLine;

 USE MoneyLine;

 CREATE TABLE users(
     user_id BIGINT AUTO_INCREMENT PRIMARY KEY,
     user_name VARCHAR(50) DEFAULT NULL,
     user_username VARCHAR(50) NOT NULL,
     user_password VARCHAR(50) NOT NULL,
     user_email VARCHAR(120) NOT NULL,
     date_created DATETIME NOT NULL DEFAULT NOW(),
    --  privacy VARCHAR(50) NOT NULL DEFAULT 'public',
     UNIQUE (user_id, user_username, user_email)
);

CREATE TABLE threads(
    thread_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    thread_username VARCHAR(50) NOT NULL FOREIGN KEY REFERENCES users(user_username),
    thread_bodytext VARCHAR(MAX),
    thread_posted DATETIME NOT NULL DEFAULT NOW()
)

CREATE TABLE comments(
    comment_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    comment_thread_id BIGINT NOT NULL FOREIGN KEY REFERENCES threads(thread_id),
    comment_username VARCHAR(50) NOT NULL,
    comment_bodytext VARCHAR(MAX),
    comment_posted DATETIME NOT NULL DEFAULT NOW()
)

CREATE TABLE betLists(
    
)

DESCRIBE users;