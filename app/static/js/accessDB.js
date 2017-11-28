
function syncCalendar() {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", 'http://localhost:5000/getCalendarData', false);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send();
    return JSON.parse(xhr.responseText);
}

function addProject(user, projectName, dueDate, courseId) {

        var obj = {"user" : user, "projectName" : projectName, "dueDate" : dueDate, "courseId" : courseId};

        var xhr = new XMLHttpRequest();
        xhr.open("POST", 'http://localhost:5000/addProject/', true);
        xhr.setRequestHeader("Content-Type", "application/json")
        console.log(JSON.stringify(obj));
        xhr.send(JSON.stringify(obj));
}

function updateProject(projectId, projectName, dueDate, courseId) {

        var obj = {"projectId" : projectId, "projectName" : projectName, "dueDate" : dueDate, "courseId" : courseId};

        var xhr = new XMLHttpRequest();
        xhr.open("POST", 'http://localhost:5000/updateProject/', true);
        xhr.setRequestHeader("Content-Type", "application/json")
        console.log(JSON.stringify(obj));
        xhr.send(JSON.stringify(obj));
}

function removeProject(projectId) {

    var obj = {"projectId" : projectId};

    var xhr = new XMLHttpRequest();
    xhr.open("POST", 'http://localhost:5000/removeProject/', true);
    xhr.setRequestHeader("Content-Type", "application/json")
    console.log(JSON.stringify(obj));
    xhr.send(JSON.stringify(obj));
}

function getProjects(id) {
    console.log("hi");
    var userid = id;
        var xhr = new XMLHttpRequest();
        xhr.open("GET", 'http://localhost:5000/getProjects/' + userid, false);
    xhr.setRequestHeader("Content-Type", "application/json");
        xhr.send(null);
    return JSON.parse(xhr.responseText);
}

function addEvent(user, eventName, startTime, endTime, tagId, pLocation, notes) {

    var obj = {"user" : user, "eventName" : eventName, "startTime" : startTime, "endTime" : endTime, "tagId" : tagId, "notes" : notes, "location" : pLocation};

    console.log(user);
    console.log(eventName);
    console.log(startTime);
    console.log(endTime);
    console.log(tagId);
    console.log(pLocation);
    console.log(notes);
    var xhr = new XMLHttpRequest();
    xhr.open("POST", 'http://localhost:5000/addEvent/', true);
    xhr.setRequestHeader("Content-Type", "application/json")
    console.log(JSON.stringify(obj));
    xhr.send(JSON.stringify(obj));
}

function removeEvent(eventId) {

    var obj = {"eventId" : eventId};

    var xhr = new XMLHttpRequest();
    xhr.open("POST", 'http://localhost:5000/removeEvent/', true);
    xhr.setRequestHeader("Content-Type", "application/json")
    console.log(JSON.stringify(obj));
    xhr.send(JSON.stringify(obj));
}

function updateEvent(eventId, eventName, startTime, endTime, tagId) {

    var obj = {"eventId" : eventId, "eventName" : eventName, "startTime" : startTime, "endTime" : endTime, "tagId" : tagId, "notes" : notes, "location" : location};

    var xhr = new XMLHttpRequest();
    xhr.open("POST", 'http://localhost:5000/updateEvent/', true);
    xhr.setRequestHeader("Content-Type", "application/json")
    console.log(JSON.stringify(obj));
    xhr.send(JSON.stringify(obj));
}

function getEvents(id) {
    var userid = id;
    var xhr = new XMLHttpRequest();
    xhr.open("GET", 'http://localhost:5000/getEvents/' + userid, false);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(null);
    return JSON.parse(xhr.responseText);
}

function updateExam(eventId, eventName, startTime, endTime, tagId) {

    var obj = {"eventId" : eventId, "eventName" : eventName, "startTime" : startTime, "endTime" : endTime, "tagId" : tagId};

    var xhr = new XMLHttpRequest();
    xhr.open("POST", 'http://localhost:5000/updateExam/', true);
    xhr.setRequestHeader("Content-Type", "application/json")
    console.log(JSON.stringify(obj));
    xhr.send(JSON.stringify(obj));
}

function addExam(user, taskName, courseId, tag, dueDate, details) {

    var obj = {"user" : user, "taskName" : taskName, "courseId" : courseId, "tag" : tag, "dueDate" : dueDate, "details" : details};

    var xhr = new XMLHttpRequest();
    xhr.open("POST", 'http://localhost:5000/addExam/', true);
    xhr.setRequestHeader("Content-Type", "application/json")
    console.log(JSON.stringify(obj));
    xhr.send(JSON.stringify(obj));
}


function removeExam(taskId) {

    var obj = {"taskId" : taskId};

    var xhr = new XMLHttpRequest();
    xhr.open("POST", 'http://localhost:5000/removeExam/', true);
    xhr.setRequestHeader("Content-Type", "application/json")
    console.log(JSON.stringify(obj));
    xhr.send(JSON.stringify(obj));
}

function getExams(id) {
    var courseId = id;
        var xhr = new XMLHttpRequest();
        xhr.open("GET", 'http://localhost:5000/getExams/' + courseId, false);
    xhr.setRequestHeader("Content-Type", "application/json");
        xhr.send(null);
    return JSON.parse(xhr.responseText);
}

function getUserExams(id) {
    var userid = id;
        var xhr = new XMLHttpRequest();
        xhr.open("GET", 'http://localhost:5000/getUserExams/' + userid, false);
    xhr.setRequestHeader("Content-Type", "application/json");
        xhr.send(null);
    return JSON.parse(xhr.responseText);
}


function updateTask(taskId, taskName, courseId, tag, dueDate, details) {

    var obj = {"taskId" : taskId, "taskName" : taskName, "courseId" : courseId, "tag" : tag, "dueDate" : dueDate, "details" : details};

    var xhr = new XMLHttpRequest();
    xhr.open("POST", 'http://localhost:5000/updateTask/', true);
    xhr.setRequestHeader("Content-Type", "application/json")
    console.log(JSON.stringify(obj));
    xhr.send(JSON.stringify(obj));
}

function getTasks(id) {
    console.log("ID: " + id);
        var xhr = new XMLHttpRequest();
        xhr.open("GET", 'http://localhost:5000/getTasks/' + id, false);
    xhr.setRequestHeader("Content-Type", "application/json");
        xhr.send(null);
    return JSON.parse(xhr.responseText);
}

function addCourse(user, courseId) {

    var obj = {"user" : user,  "courseId" : courseId };

    var xhr = new XMLHttpRequest();
    xhr.open("POST", 'http://localhost:5000/addCourse/', true);
    xhr.setRequestHeader("Content-Type", "application/json");
    console.log(JSON.stringify(obj));
    xhr.send(JSON.stringify(obj));
}

function removeCourse(user, courseId) {

    var obj = {"courseId" : courseId, "userId" : user};

    var xhr = new XMLHttpRequest();
    xhr.open("POST", 'http://localhost:5000/removeCourse/', true);
    xhr.setRequestHeader("Content-Type", "application/json");
    console.log(JSON.stringify(obj));
    xhr.send(JSON.stringify(obj));
}

function getUserCourses(id) {
  var userid = id;
  var xhr = new XMLHttpRequest();
  xhr.open("GET", 'http://localhost:5000/getUserCourses/' + userid, false);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.send(null);
  return JSON.parse(xhr.responseText);
}

function getAllCourses() {
  var xhr = new XMLHttpRequest();
  xhr.open("GET", 'http://localhost:5000/getAllCourses', false);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.send(null);
  return JSON.parse(xhr.responseText);
}

function removeCourseAndProjects (user, courseId) {
  var obj = {"user" : user,  "courseId" : courseId };

  var xhr = new XMLHttpRequest();
  xhr.open("POST", 'http://localhost:5000/removeCourseAndProjects/', true);
  xhr.setRequestHeader("Content-Type", "application/json")
  console.log(JSON.stringify(obj));
  xhr.send(JSON.stringify(obj));
}

function getColor(name) {
  var xhr = new XMLHttpRequest();
  var hash = name;
  xhr.open("GET", 'http://localhost:5000/getColor/' + hash, false);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.send(null);
  return JSON.parse(xhr.responseText);
}

function getUserCourseColor(userId, courseId) {
  var xhr = new XMLHttpRequest();
  var netId = userId;
  var course_id = courseId;
  xhr.open("GET", 'http://localhost:5000/getUserCourseColor/' + netId + '/' + course_id, false);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.send(null);
  return JSON.parse(xhr.responseText);
}

function getTags(user) {
  var xhr = new XMLHttpRequest();
  var netId = userId;
  var course_id = courseId;
  xhr.open("GET", 'http://localhost:5000/getTags/' + user, false);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.send(null);
  return JSON.parse(xhr.responseText);
}

function addTag(user, tagId, color, isCourse) {

    var obj = {"user" : user,  "tagId" : tagId,  "color" : color,  "isCourse" : isCourse };

    var xhr = new XMLHttpRequest();
    xhr.open("POST", 'http://localhost:5000/addTag/', true);
    xhr.setRequestHeader("Content-Type", "application/json");
    console.log(JSON.stringify(obj));
    xhr.send(JSON.stringify(obj));
}

function removeTag (user, tagId) {
  var obj = {"user" : user,  "tagId" : tagId };

  var xhr = new XMLHttpRequest();
  xhr.open("POST", 'http://localhost:5000/removeTag/', true);
  xhr.setRequestHeader("Content-Type", "application/json")
  console.log(JSON.stringify(obj));
  xhr.send(JSON.stringify(obj));
}

function updateTagColor(user, tagId, color) {

    var obj = {"user" : user, "tagId" : tagId, "color" : color};

    var xhr = new XMLHttpRequest();
    xhr.open("POST", 'http://localhost:5000/updateTagColor/', true);
    xhr.setRequestHeader("Content-Type", "application/json")
    console.log(JSON.stringify(obj));
    xhr.send(JSON.stringify(obj));
}
