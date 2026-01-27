CREATE DATABASE pm;
USE pm;

CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(50),
  email VARCHAR(100),
  password VARCHAR(100),
  role VARCHAR(20)
);

CREATE TABLE projects (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100),
  status VARCHAR(20)
);

CREATE TABLE tasks (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(100),
  description TEXT,
  status VARCHAR(20),
  project_id INT,
  assigned_user_id INT
);

INSERT INTO users VALUES
(1,'Admin','admin@pm.com','admin123','manager'),
(2,'Bob','bob@pm.com','bob123','employee'),
(3,'Charlie','charlie@pm.com','charlie123','employee');

INSERT INTO projects VALUES
(1,'Website Revamp','ongoing');

INSERT INTO tasks VALUES
(1,'Design UI','Create homepage','pending',1,2),
(2,'Backend APIs','Build Flask APIs','pending',1,3);
