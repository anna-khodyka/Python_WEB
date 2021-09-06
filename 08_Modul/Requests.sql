--Список студентов в группе 
SELECT groups.name, users.family_name, users.name
FROM students_in_groups AS sig
JOIN users ON users.id=sig.id_student
JOIN groups ON groups.id=sig.id_group
ORDER by groups.name, users.family_name;
--Оценки студентов в группе по предмету.
SELECT groups.name, subjects.name, users.family_name, users.name, m.created_at, m.mark
FROM marks AS m
JOIN users ON users.id=m.id_student
JOIN subjects ON subjects.id=m.id_subject
JOIN students_in_groups AS sig ON users.id=sig.id_student
JOIN groups ON groups.id=sig.id_group
WHERE groups.name='2021A';
--5 студентов с наибольшим средним баллом по всем предметам.
SELECT users.family_name,  AVG(marks.mark) as Average_Student_Mark
FROM marks
JOIN users ON users.id=marks.id_student
GROUP BY users.family_name
ORDER by Average_Student_Mark DESC
LIMIT 5; 
--1 студент с наивысшим средним баллом по одному предмету.
SELECT subjects.name, users.family_name, AVG(marks.mark) as Average_Student_Mark
FROM marks
JOIN users ON users.id=marks.id_student
JOIN subjects ON subjects.id=marks.id_subject 
WHERE subjects.name='history'
GROUP BY users.family_name
ORDER by Average_Student_Mark DESC
LIMIT 1; 
--средний балл в группе по одному предмету.
SELECT groups.name, subjects.name, AVG(marks.mark) as Average_Mark
FROM marks
JOIN subjects ON subjects.id=marks.id_subject 
JOIN users ON users.id=marks.id_student 
JOIN students_in_groups AS sig ON sig.id_student=users.id 
JOIN groups ON groups.id=sig.id_group 
GROUP BY groups.name, subjects.name;
--Средний балл в потоке.
SELECT avg(marks.mark) as Average_Mark_among_all_year
FROM marks;
--Какие курсы читает преподаватель.
SELECT users.family_name, roles.name, subjects.name 
FROM users
JOIN roles ON users.id_role=roles.id
JOIN schedule AS sch ON sch.id_lector=users.id
JOIN subjects ON subjects.id=sch.id_subject
WHERE roles.name='lector'
GROUP by subjects.name
ORDER BY users.family_name;
--Оценки студентов в группе по предмету на последнем занятии.
SELECT groups.name, users.family_name, marks.created_at, marks.mark
FROM marks
JOIN subjects ON subjects.id=marks.id_subject 
JOIN users ON users.id=marks.id_student 
JOIN students_in_groups AS sig ON sig.id_student=users.id
JOIN groups ON sig.id_group=groups.id
WHERE subjects.name='geometry' and groups.name='2021A' and marks.created_at in (
-- подзапрос - дата последнего занятия в группе по предмету
SELECT max(marks.created_at) AS Last_date
FROM marks
JOIN subjects ON subjects.id=marks.id_subject 
JOIN users ON users.id=marks.id_student 
JOIN students_in_groups AS sig ON sig.id_student=users.id
JOIN groups ON sig.id_group=groups.id
WHERE subjects.name='geometry' and groups.name='2021A');

--Список курсов, которые посещает студент.
SELECT users.family_name, groups.name, subjects.name  
FROM schedule AS sch
JOIN groups ON groups.id=sch.id_group
JOIN subjects ON subjects.id=sch.id_subject
JOIN students_in_groups AS sig ON sig.id_group=groups.id
JOIN users ON users.id=sig.id_student
WHERE users.family_name='Korovina';
--Список курсов, которые студенту читает преподаватель.
SELECT users.family_name AS Student, subjects.name AS Subject
from users 
JOIN students_in_groups AS sig ON users.id=sig.id_student
JOIN groups ON groups.id=sig.id_group
JOIN schedule AS sch ON groups.id=sch.id_group
JOIN subjects ON subjects.id=sch.id_subject
WHERE users.family_name='Sylik' and sch.id_lector in (
-- подзапрос - id лектора чья фамилия задана
SELECT users.id
FROM USERS 
WHERE users.family_name='Khodyka');
--Средний балл, который преподаватель ставит студенту.
SELECT users.family_name, avg(marks.mark)
FROM marks
JOIN users ON marks.id_student=users.id
JOIN students_in_groups AS sig ON users.id=sig.id_student 
JOIN groups ON sig.id_group=groups.id
JOIN schedule AS sch ON sch.id_group=groups.id
JOIN subjects ON sch.id_subject=subjects.id
WHERE users.family_name='Kopanitsha' and sch.id_lector in (
-- подзапрос - id лектора чья фамилия задана
SELECT users.id
FROM users 
WHERE users.family_name='Khodyka');
--Средний балл, который ставит преподаватель.
SELECT sch.id_lector, avg(marks.mark) AS Average_lector_mark
FROM marks
JOIN users ON marks.id_student=users.id
JOIN students_in_groups AS sig ON users.id=sig.id_student 
JOIN groups ON sig.id_group=groups.id
JOIN schedule AS sch ON sch.id_group=groups.id
WHERE sch.id_lector in (
-- подзапрос - id лектора чья фамилия задана
SELECT users.id
FROM users 
WHERE users.family_name='Shevchenko');