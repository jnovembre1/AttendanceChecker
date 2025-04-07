-- Drop tables if they exist
DROP TABLE IF EXISTS attendance;
DROP TABLE IF EXISTS studentcourses;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS instructors;
DROP TABLE IF EXISTS location;
DROP TABLE IF EXISTS meetingdays;

-- Create instructors table
CREATE TABLE instructors (
    instructorid SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Create courses table
CREATE TABLE courses (
    courseid SERIAL PRIMARY KEY,
    coursename VARCHAR(255) NOT NULL,
    instructor VARCHAR(255),
    meetingdays VARCHAR(255),
    meetingtime VARCHAR(255),
    classendtime VARCHAR(255)
);

-- Create students table
CREATE TABLE students (
    studentid SERIAL PRIMARY KEY,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    profilepic VARCHAR(255)
);

-- Create studentcourses junction table
CREATE TABLE studentcourses (
    id SERIAL PRIMARY KEY,
    studentid INTEGER REFERENCES students(studentid),
    courseid INTEGER REFERENCES courses(courseid)
);

-- Create attendance table
CREATE TABLE attendance (
    attendanceid SERIAL PRIMARY KEY,
    studentid INTEGER REFERENCES students(studentid) NOT NULL,
    courseid INTEGER REFERENCES courses(courseid) NOT NULL,
    datetime TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Create indexes
CREATE INDEX idx_attendance_studentid ON attendance(studentid);
CREATE INDEX idx_attendance_courseid ON attendance(courseid);
CREATE INDEX idx_attendance_datetime ON attendance(datetime);
