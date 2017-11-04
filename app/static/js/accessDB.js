
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

function addEvent(user, eventName, startTime, endTime, tagId) {

    var obj = {"user" : user, "eventName" : eventName, "startTime" : startTime, "endTime" : endTime, "tagId" : tagId};

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

    var obj = {"eventId" : eventId, "eventName" : eventName, "startTime" : startTime, "endTime" : endTime, "tagId" : tagId};

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

function addTask(userid, taskname, course, duedate, details) {

    var obj = {"userid" : userid, "taskname" : taskname, "course" : course,  "duedate" : duedate, "details" : details};

    var xhr = new XMLHttpRequest();
    xhr.open("POST", 'http://localhost:5000/addTask/', true);
    xhr.setRequestHeader("Content-Type", "application/json")
    console.log(JSON.stringify(obj));
    xhr.send(JSON.stringify(obj));
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

function addTask()) {

    var obj = {"user" : user, "taskName" : taskName, "courseId" : courseId, "tag" : tag, "startDate" : startDate, "dueDate" : dueDate, "details" : details};

    var xhr = new XMLHttpRequest();
    xhr.open("POST", 'http://localhost:5000/addTask/', true);
    xhr.setRequestHeader("Content-Type", "application/json")
    console.log(JSON.stringify(obj));
    xhr.send(JSON.stringify(obj));
}

function addCourse(user, courseId) {

    var obj = {"user" : user,  "courseId" : courseId };

    var xhr = new XMLHttpRequest();
    xhr.open("POST", 'http://localhost:5000/addCourse/', true);
    xhr.setRequestHeader("Content-Type", "application/json")
    console.log(JSON.stringify(obj));
    xhr.send(JSON.stringify(obj));
}

function removeCourse(userId, courseId) {

    var obj = {"courseId" : courseId , "userId" : userId };

    var xhr = new XMLHttpRequest();
    xhr.open("POST", 'http://localhost:5000/removeCourse/', true);
    xhr.setRequestHeader("Content-Type", "application/json")
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
  xhr.open("GET", 'http://localhost:5000/getAllCourses/', false);
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
  xhr.open("GET", 'http://localhost:5000/getColor/' + name, false);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.send(null);
  return JSON.parse(xhr.responseText);
}
