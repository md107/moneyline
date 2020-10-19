 CREATE DATABASE MoneyLine;

 USE MoneyLine;

 CREATE TABLE users(
     user_id BIGINT AUTO_INCREMENT PRIMARY KEY,
     user_name VARCHAR(50) NULL,
     user_username VARCHAR(50) NOT NULL,
     user_password VARCHAR(50) NOT NULL,
     user_email VARCHAR(120) NOT NULL,
     date_created DATETIME NOT NULL DEFAULT NOW(),
     UNIQUE (user_id, user_username, user_email)
);

DESCRIBE users;