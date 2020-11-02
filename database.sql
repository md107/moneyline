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
    about_me VARCHAR(140) DEFAULT NULL
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
    comment_thread_id BIGINT NOT NULL,
    comment_username VARCHAR(50) NOT NULL,
    comment_bodytext VARCHAR(10000),
    comment_posted DATETIME NOT NULL DEFAULT NOW()
);

CREATE TABLE allBets (
    bet_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    team1 VARCHAR(500) NOT NULL,
    team2 VARCHAR(500) NOT NULL,
    odd VARCHAR(500)
);

CREATE TABLE betLists(
    bet_id BIGINT,
    user_id BIGINT,
    username VARCHAR(50)
);

DESCRIBE users;
