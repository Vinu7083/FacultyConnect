create database faculty_management;
use faculty_management;

-- Create the Faculty table
CREATE TABLE Faculty (
    Faculty_id INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Joining_Date DATE NOT NULL,
    Designation VARCHAR(50),
    Phone_No VARCHAR(15) UNIQUE,
    username VARCHAR(100) UNIQUE,
    password VARCHAR(100) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
);

-- Create the Feedback table
CREATE TABLE Feedback (
    Feedback_id INT PRIMARY KEY,
    Faculty_id INT,
    Rating INT CHECK (Rating BETWEEN 1 AND 5),
    Date DATE,
    FOREIGN KEY (Faculty_id) REFERENCES Faculty(Faculty_id) ON DELETE CASCADE
);

-- Create the Student table
CREATE TABLE Student (
    S_id INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Phone_No VARCHAR(15) UNIQUE,
    DOB DATE,
    Email VARCHAR(100) UNIQUE,
    username VARCHAR(100) UNIQUE,
    password VARCHAR(100) NOT NULL
);

-- Create the Faculty_Role table
CREATE TABLE Faculty_Role (
    Faculty_id INT,
    Role VARCHAR(50),
    PRIMARY KEY (Faculty_id, Role),
    FOREIGN KEY (Faculty_id) REFERENCES Faculty(Faculty_id) ON DELETE CASCADE
);

-- Create the Leaves_Taken table
CREATE TABLE Leaves_Taken (
    Leave_id INT PRIMARY KEY,
    Faculty_id INT,
    Leave_Date DATE NOT NULL,
    Approval_Status VARCHAR(20) CHECK (Approval_Status IN ('Approved', 'Pending', 'Rejected')),
    FOREIGN KEY (Faculty_id) REFERENCES Faculty(Faculty_id) ON DELETE CASCADE
);

-- Create the Handles_Courses table
CREATE TABLE Handles_Courses (
    Faculty_id INT,
    Course_id INT unique,
    Course_Name VARCHAR(100),
    Credits INT CHECK (Credits > 0),
    PRIMARY KEY (Faculty_id, Course_id),
    FOREIGN KEY (Faculty_id) REFERENCES Faculty(Faculty_id) ON DELETE CASCADE
    
);


-- Create the Timetable table
CREATE TABLE Timetable (
    Faculty_id INT,
    Course_id INT,
    Room_No VARCHAR(10),
    Timeslot VARCHAR(20),
    Day VARCHAR(10),
    PRIMARY KEY (Faculty_id, Course_id, Day, Timeslot),
    FOREIGN KEY (Faculty_id) REFERENCES Faculty(Faculty_id) ON DELETE CASCADE,
    FOREIGN KEY (Course_id) REFERENCES Handles_Courses(Course_id) ON DELETE CASCADE
);

-- Create the Gives table (linking Students and Feedback)
CREATE TABLE Gives (
    S_id INT,
    Feedback_id INT,
    PRIMARY KEY (S_id, Feedback_id),
    FOREIGN KEY (S_id) REFERENCES Student(S_id) ON DELETE CASCADE,
    FOREIGN KEY (Feedback_id) REFERENCES Feedback(Feedback_id) ON DELETE CASCADE
);

-- Create the Registration table (linking Students and Courses)
CREATE TABLE Registration (
    S_id INT,
    Course_id INT,
    PRIMARY KEY (S_id, Course_id),
    FOREIGN KEY (S_id) REFERENCES Student(S_id) ON DELETE CASCADE,
    FOREIGN KEY (Course_id) REFERENCES Handles_Courses(Course_id) ON DELETE CASCADE
);

-- Sample Data Insertion

-- Insert into Faculty
INSERT INTO Faculty (Faculty_id, Name, Joining_Date, Designation, Phone_No, username, password, is_admin) VALUES
(1, 'Dr. Smith', '2020-01-15', 'Professor', '1234567890', 'admin', 'vinu', TRUE),
(2, 'Dr. Johnson', '2018-05-20', 'Assistant Professor', '9876543210', 'faculty', 'hashed_password', FALSE);


-- Insert into Feedback
INSERT INTO Feedback (Feedback_id, Faculty_id, Rating, Date) VALUES
(1, 1, 5, '2025-01-01'),
(2, 2, 4, '2025-01-02');

-- Insert into Student
INSERT INTO Student (S_id, Name, Phone_No, DOB, Email, username, password) VALUES
(1, 'Alice', '1112223334', '2000-03-15', 'alice@example.com', 'alice', 'hashed_password'),
(2, 'Bob', '2223334445', '1999-08-20', 'bob@example.com', 'bob', 'hashed_password');


