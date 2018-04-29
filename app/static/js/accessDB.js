
function syncCalendar() {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", '/getCalendarData', false);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send();
    return JSON.parse(xhr.responseText);
}

function addProject(user, projectName, dueDate, courseId) {

        var obj = {"user" : user, "projectName" : projectName, "dueDate" : dueDate, "courseId" : courseId};

        var xhr = new XMLHttpRequest();
        xhr.open("POST", '/addProject/', false);
        xhr.setRequestHeader("Content-Type", "application/json")
        console.log(JSON.stringify(obj));
        xhr.send(JSON.stringify(obj));
}

function updateProject(projectId, projectName, dueDate, courseId) {

        var obj = {"projectId" : projectId, "projectName" : projectName, "dueDate" : dueDate, "courseId" : courseId};

        var xhr = new XMLHttpRequest();
        xhr.open("POST", '/updateProject/', false);
        xhr.setRequestHeader("Content-Type", "application/json")
        console.log(JSON.stringify(obj));
        xhr.send(JSON.stringify(obj));
}

function removeProject(projectId) {

    var obj = {"projectId" : projectId};

    var xhr = new XMLHttpRequest();
    xhr.open("POST", '/removeProject/', true);
    xhr.setRequestHeader("Content-Type", "application/json")
    console.log(JSON.stringify(obj));
    xhr.send(JSON.stringify(obj));
}

function getProjects(id) {
    console.log("hi");
    var userid = id;
        var xhr = new XMLHttpRequest();
        xhr.open("GET", '/getProjects/' + userid, false);
    xhr.setRequestHeader("Content-Type", "application/json");
        xhr.send(null);
    return JSON.parse(xhr.responseText);
}

function addEvent(user, eventName, startTime, endTime, tagId, pLocation, notes) {
    console.log('In addEvent');
    var obj = {"user" : user, "eventName" : eventName, "startTime" : startTime, "endTime" : endTime, "tagId" : tagId, "notes" : notes, "location" : pLocation};
    console.log('Object:');
    console.log(obj);

    var xhr = new XMLHttpRequest();
    xhr.open("POST", '/addEvent/', false);
    xhr.setRequestHeader("Content-Type", "application/json")
    console.log(JSON.stringify(obj));
    xhr.send(JSON.stringify(obj));
}

function removeEvent(eventId) {
    console.log('Event id to remove');
    console.log(eventId);
    var obj = {"eventId" : eventId};

    var xhr = new XMLHttpRequest();
    xhr.open("POST", '/removeEvent/', true);
    xhr.setRequestHeader("Content-Type", "application/json")
    console.log(JSON.stringify(obj));
    xhr.send(JSON.stringify(obj));
}

// function removeTag (user, tagId) {
//   var obj = {"user" : user,  "tagId" : tagId };
//
//   var xhr = new XMLHttpRequest();
//   xhr.open("POST", 'http://localhost:5000/removeTag/', true);
//   xhr.setRequestHeader("Content-Type", "application/json")
//   console.log(JSON.stringify(obj));
//   xhr.send(JSON.stringify(obj));
// }


function updateEvent(eventId, eventName, startTime, endTime, tagId, notes, loc) {

    var obj = {"eventId" : eventId, "eventName" : eventName, "startTime" : startTime, "endTime" : endTime, "tagId" : tagId, "notes" : notes, "location" : loc};
    console.log(obj);
    var xhr = new XMLHttpRequest();
    xhr.open("POST", '/updateEvent/', true);
    xhr.setRequestHeader("Content-Type", "application/json")
    console.log(JSON.stringify(obj));
    xhr.send(JSON.stringify(obj));
}

function getEvents(id) {
    var userid = id;
    var xhr = new XMLHttpRequest();
    xhr.open("GET", '/getEvents/' + userid, false);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(null);
    return JSON.parse(xhr.responseText);
}

function updateExam(eventId, eventName, startTime, endTime, tagId) {

    var obj = {"eventId" : eventId, "eventName" : eventName, "startTime" : startTime, "endTime" : endTime, "tagId" : tagId};

    var xhr = new XMLHttpRequest();
    xhr.open("POST", '/updateExam/', true);
    xhr.setRequestHeader("Content-Type", "application/json")
    console.log(JSON.stringify(obj));
    xhr.send(JSON.stringify(obj));
}

function addExam(user, taskName, courseId, tag, dueDate, details) {

    var obj = {"user" : user, "taskName" : taskName, "courseId" : courseId, "tag" : tag, "dueDate" : dueDate, "details" : details};

    var xhr = new XMLHttpRequest();
    xhr.open("POST", '/addExam/', true);
    xhr.setRequestHeader("Content-Type", "application/json")
    console.log(JSON.stringify(obj));
    xhr.send(JSON.stringify(obj));
}


function removeExam(taskId) {

    var obj = {"taskId" : taskId};

    var xhr = new XMLHttpRequest();
    xhr.open("POST", '/removeExam/', true);
    xhr.setRequestHeader("Content-Type", "application/json")
    console.log(JSON.stringify(obj));
    xhr.send(JSON.stringify(obj));
}

function getExams(id) {
    var courseId = id;
        var xhr = new XMLHttpRequest();
        xhr.open("GET", '/getExams/' + courseId, false);
    xhr.setRequestHeader("Content-Type", "application/json");
        xhr.send(null);
    return JSON.parse(xhr.responseText);
}

function getUserExams(id) {
    var userid = id;
        var xhr = new XMLHttpRequest();
        xhr.open("GET", '/getUserExams/' + userid, false);
    xhr.setRequestHeader("Content-Type", "application/json");
        xhr.send(null);
    return JSON.parse(xhr.responseText);
}


function updateTask(taskId, taskName, courseId, tag, dueDate, details) {

    var obj = {"taskId" : taskId, "taskName" : taskName, "courseId" : courseId, "tag" : tag, "dueDate" : dueDate, "details" : details};

    var xhr = new XMLHttpRequest();
    xhr.open("POST", '/updateTask/', true);
    xhr.setRequestHeader("Content-Type", "application/json")
    console.log(JSON.stringify(obj));
    xhr.send(JSON.stringify(obj));
}

function getTasks(id) {
    console.log("ID: " + id);
        var xhr = new XMLHttpRequest();
        xhr.open("GET", '/getTasks/' + id, false);
    xhr.setRequestHeader("Content-Type", "application/json");
        xhr.send(null);
    return JSON.parse(xhr.responseText);
}

function addCourse(user, courseId) {

    var obj = {"user" : user,  "courseId" : courseId };

    var xhr = new XMLHttpRequest();
    xhr.open("POST", '/addCourse/', true);
    xhr.setRequestHeader("Content-Type", "application/json");
    console.log(JSON.stringify(obj));
    xhr.send(JSON.stringify(obj));
}

function removeCourse(user, courseId) {

    var obj = {"courseId" : courseId, "userId" : user};

    var xhr = new XMLHttpRequest();
    xhr.open("POST", '/removeCourse/', true);
    xhr.setRequestHeader("Content-Type", "application/json");
    console.log(JSON.stringify(obj));
    xhr.send(JSON.stringify(obj));
}

function getUserCourses(id) {
  var userid = id;
  var xhr = new XMLHttpRequest();
  xhr.open("GET", '/getUserCourses/' + userid, false);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.send(null);
  return JSON.parse(xhr.responseText);
}

function getAllCourses() {
  var xhr = new XMLHttpRequest();
  xhr.open("GET", '/getAllCourses', false);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.send(null);
  return JSON.parse(xhr.responseText);
}

function removeCourseAndProjects (user, courseId) {
  var obj = {"user" : user,  "courseId" : courseId };

  var xhr = new XMLHttpRequest();
  xhr.open("POST", '/removeCourseAndProjects/', true);
  xhr.setRequestHeader("Content-Type", "application/json")
  console.log(JSON.stringify(obj));
  xhr.send(JSON.stringify(obj));
}

function getColor(name) {
  var xhr = new XMLHttpRequest();
  var hash = name;
  xhr.open("GET", '/getColor/' + hash, false);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.send(null);
  return JSON.parse(xhr.responseText);
}

function getUserCourseColor(userId, courseId) {
  var xhr = new XMLHttpRequest();
  var netId = userId;
  var course_id = courseId;
  xhr.open("GET", '/getUserCourseColor/' + netId + '/' + course_id, false);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.send(null);
  return JSON.parse(xhr.responseText);
}

function getTags(user) {
  var xhr = new XMLHttpRequest();
  var netId = user;
  xhr.open("GET", '/getTags/' + user, false);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.send(null);
  return JSON.parse(xhr.responseText);

  // var userid = id;
  // var xhr = new XMLHttpRequest();
  // xhr.open("GET", '/getUserCourses/' + userid, false);
  // xhr.setRequestHeader("Content-Type", "application/json");
  // xhr.send(null);
  // return JSON.parse(xhr.responseText);
}

function addTag(user, tagId, color) {

    var obj = {"user" : user,  "tagId" : tagId,  "color" : color};

    var xhr = new XMLHttpRequest();
    xhr.open("POST", '/addTag/', true);
    xhr.setRequestHeader("Content-Type", "application/json");
    console.log(JSON.stringify(obj));
    xhr.send(JSON.stringify(obj));
}

function removeTag (user, tagId) {
  var obj = {"user" : user,  "tagId" : tagId };

  var xhr = new XMLHttpRequest();
  xhr.open("POST", '/removeTag/', true);
  xhr.setRequestHeader("Content-Type", "application/json")
  console.log(JSON.stringify(obj));
  xhr.send(JSON.stringify(obj));
}

function updateTagColor(user, tagId, color) {

    var obj = {"user" : user, "tagId" : tagId, "color" : color};

    var xhr = new XMLHttpRequest();
    xhr.open("POST", '/updateTagColor/', true);
    xhr.setRequestHeader("Content-Type", "application/json")
    console.log(JSON.stringify(obj));
    xhr.send(JSON.stringify(obj));
}

function updateTagId(user, tagId, newTagId) {

    var obj = {"user" : user, "tagId" : tagId, "newTagId" : newTagId};

    var xhr = new XMLHttpRequest();
    xhr.open("POST", '/updateTagId/', true);
    xhr.setRequestHeader("Content-Type", "application/json")
    console.log(JSON.stringify(obj));
    xhr.send(JSON.stringify(obj));
}

function updateCourseColor(netId, courseId, new_color) {

    var obj = {"netId" : netId, "courseId" : courseId, "color" : new_color};

    var xhr = new XMLHttpRequest();
    xhr.open("POST", '/updateCourseColor/', true);
    xhr.setRequestHeader("Content-Type", "application/json")
    console.log(JSON.stringify(obj));
    xhr.send(JSON.stringify(obj));
}

function getUserTagColor(netid, tagId){
  var xhr = new XMLHttpRequest();
  var netId = userid;
  var tag_id = tagId;
  xhr.open("GET", '/getUserTagColor/' + netId + '/' + tagId, false);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.send(null);
  return JSON.parse(xhr.responseText);
}
