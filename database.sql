CREATE USER 'csds393'@'localhost' IDENTIFIED BY 'moneyline';

GRANT ALL PRIVILEGE ON *.* TO 'csds393'@'localhost';

-- mysql -u csds393 -p

CREATE DATABASE MoneyLine;

USE MoneyLine;

SHOW DATABASES;

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

CREATE TABLE posts(
    post_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    post_username VARCHAR(50) NOT NULL,
    post_bodytext VARCHAR(10000) NOT NULL,
    post_posted DATETIME NOT NULL DEFAULT NOW()
);

CREATE TABLE comments(
    comment_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    comment_thread_id BIGINT NOT NULL FOREIGN KEY REFERENCES threads(thread_id),
    comment_username VARCHAR(50) NOT NULL,
    comment_bodytext VARCHAR(MAX),
    comment_posted DATETIME NOT NULL DEFAULT NOW()
);

CREATE TABLE betLists(
    
);

DESCRIBE users;
