CREATE TABLE Institutions (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    description TEXT,
    creationDate DATE
);

CREATE TABLE Teachers (
    id INT PRIMARY KEY,
    institutionID INT,
    name VARCHAR(100),
    email VARCHAR(100),
    FOREIGN KEY (institutionID) REFERENCES Institutions(id)
);

CREATE TABLE Students (
    id INT PRIMARY KEY,
    institutionID INT,
    name VARCHAR(100),
    birthDate DATE,
    FOREIGN KEY (institutionID) REFERENCES Institutions(id)
);

CREATE TABLE Subjects (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    description TEXT
);

CREATE TABLE Assessment (
    id INT PRIMARY KEY,
    studentID INT,
    subjectID INT,
    teacherID INT,
    date DATE,
    proficiencyLevel INT,
    FOREIGN KEY (studentID) REFERENCES Students(id),
    FOREIGN KEY (subjectID) REFERENCES Subjects(id),
    FOREIGN KEY (teacherID) REFERENCES Teachers(id)
);

CREATE TABLE TranscriptionJobs (
    id INT PRIMARY KEY,
    assessmentID INT,
    status VARCHAR(20),
    creationDate DATE,
    completionDate DATE,
    FOREIGN KEY (assessmentID) REFERENCES Assessment(id)
);

CREATE TABLE BlobStorage (
    id INT PRIMARY KEY,
    jobID INT,
    blobData TEXT,
    FOREIGN KEY (jobID) REFERENCES TranscriptionJobs(id)
);

CREATE TABLE Feedback (
    id INT PRIMARY KEY,
    assessmentID INT,
    teacherID INT,
    feedback TEXT,
    date DATE,
    FOREIGN KEY (assessmentID) REFERENCES Assessment(id),
    FOREIGN KEY (teacherID) REFERENCES Teachers(id)
);
