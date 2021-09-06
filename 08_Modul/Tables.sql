CREATE TABLE roles (
    id INT PRIMARY KEY,
    name VARCHAR(30)
);

CREATE TABLE groups (
    id INT PRIMARY KEY,
    name VARCHAR(30)
);

CREATE TABLE subjects (
    id INT PRIMARY KEY,
    name VARCHAR(30)
);

CREATE TABLE users (
    id INT PRIMARY KEY,
    name VARCHAR(30), 
    family_name VARCHAR(30), 
    id_role  INT,
    FOREIGN KEY (id_role) REFERENCES roles (id)
          ON DELETE SET NULL
          ON UPDATE CASCADE
);

CREATE TABLE students_in_groups (
    id INT PRIMARY KEY,
    id_group INT,
    id_student INT,
    FOREIGN KEY (id_group) REFERENCES groups (id)
          ON DELETE SET NULL
          ON UPDATE CASCADE,
   FOREIGN KEY (id_student) REFERENCES users (id)
          ON DELETE SET NULL
          ON UPDATE CASCADE   
);


CREATE TABLE schedule (
    id INT PRIMARY KEY, -- не уверенна нужен ли тут ключ
    id_group INT,
    id_subject INT,
    id_lector INT,
    FOREIGN KEY (id_group) REFERENCES groups (id)
          ON DELETE SET NULL
          ON UPDATE CASCADE,
   FOREIGN KEY (id_subject) REFERENCES subjects (id)
          ON DELETE SET NULL
          ON UPDATE CASCADE,
   FOREIGN KEY (id_lector) REFERENCES users (id)
          ON DELETE SET NULL
          ON UPDATE CASCADE       
);

CREATE TABLE marks (
    id INT PRIMARY KEY, 
    mark TINYINT UNSIGNED,
    id_subject INT,
    id_student INT,
    created_at DATE DEFAULT CURRENT_DATE,
   	FOREIGN KEY (id_subject) REFERENCES subjects (id)
          ON DELETE SET NULL
          ON UPDATE CASCADE,
   	FOREIGN KEY (id_student) REFERENCES users (id)
          ON DELETE SET NULL
          ON UPDATE CASCADE       
);