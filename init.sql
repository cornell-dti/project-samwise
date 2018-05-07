-- NOTE: Don't use 'user' anywhere in the table creation


CREATE TABLE UserCourses(
  id SERIAL PRIMARY KEY,
  netId INT NOT NULL,
  courseId TEXT NOT NULL,
  color TEXT NOT NULL
);

CREATE TABLE Tag (
  id SERIAL PRIMARY KEY,
  netId INT NOT NULL,
  tagId TEXT NOT NULL,
  color TEXT NOT NULL
);

CREATE TABLE Exam (
  id SERIAL PRIMARY KEY,
  courseId TEXT NOT NULL,
  section TEXT NOT NULL,
  start TEXT NOT NULL
);

CREATE TABLE Course (
  id SERIAL PRIMARY KEY,
  courseId TEXT NOT NULL UNIQUE
);

CREATE TABLE Event (
  eventId SERIAL PRIMARY KEY,
  netId INT NOT NULL,
  eventName TEXT NOT NULL,
  startTime TEXT NOT NULL,
  endTime TEXT NOT NULL,
  tagId TEXT NOT NULL,
  notes TEXT NOT NULL,
  location TEXT NOT NULL
);
