CREATE TABLE User (
  id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
  netId INTEGER NOT NULL,
  courseId TEXT NOT NULL,
  color TEXT NOT NULL
);

CREATE TABLE Tag (
  id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
  user INTEGER NOT NULL,
  tagId TEXT NOT NULL,
  color TEXT NOT NULL
);

CREATE TABLE Exam (
  id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
  courseId TEXT NOT NULL,
  section TEXT NOT NULL,
  start TEXT NOT NULL
);

CREATE TABLE Course (
  id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
  courseId TEXT NOT NULL UNIQUE
);

CREATE TABLE Event (
  eventId INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
  user INTEGER NOT NULL,
  eventName TEXT NOT NULL,
  startTime TEXT NOT NULL,
  endTime TEXT NOT NULL,
  tagId TEXT NOT NULL,
  notes TEXT NOT NULL,
  location TEXT NOT NULL
);