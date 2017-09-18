function addProjectColor(id, projectName, date, tasklist, color) {

        var obj = {"userid" : id, "project" : projectName, "duedate" : date, "subtasks" : tasklist, "color" : color};

        var xhr = new XMLHttpRequest();
        xhr.open("POST", 'http://localhost:5000/addProjectColor/', true);
        xhr.setRequestHeader("Content-Type", "application/json")
        console.log(JSON.stringify(obj));
        xhr.send(JSON.stringify(obj));
}

function addProjectCourse(id, projectName, date, tasklist, course) {

        var obj = {"userid" : id, "project" : projectName, "duedate" : date, "subtasks" : tasklist, "course" : course};

        var xhr = new XMLHttpRequest();
        xhr.open("POST", 'http://localhost:5000/addProjectCourse/', true);
        xhr.setRequestHeader("Content-Type", "application/json")
        console.log(JSON.stringify(obj));
        xhr.send(JSON.stringify(obj));
}

function updateProject(projectid, projectName, date, course, color) {

        var obj = {"projectid" : projectid, "project" : projectName, "duedate" : date, "course" : course, "color" : color};

        var xhr = new XMLHttpRequest();
        xhr.open("POST", 'http://localhost:5000/updateProject/', true);
        xhr.setRequestHeader("Content-Type", "application/json")
        console.log(JSON.stringify(obj));
        xhr.send(JSON.stringify(obj));
}

    function removeProject(projectname) {

        var obj = {"projectname" : projectname};

        var xhr = new XMLHttpRequest();
        xhr.open("POST", 'http://localhost:5000/removeProject/', true);
        xhr.setRequestHeader("Content-Type", "application/json")
        console.log(JSON.stringify(obj));
        xhr.send(JSON.stringify(obj));
    }

    function addEvent(userid, eventname, date, color) {

        var obj = {"userid" : userid, "eventname" : eventname, "date" : date, "color" : color};

        var xhr = new XMLHttpRequest();
        xhr.open("POST", 'http://localhost:5000/addEvent/', true);
        xhr.setRequestHeader("Content-Type", "application/json")
        console.log(JSON.stringify(obj));
        xhr.send(JSON.stringify(obj));
    }

    function removeEvent(eventid) {

        var obj = {"eventid" : eventid};

        var xhr = new XMLHttpRequest();
        xhr.open("POST", 'http://localhost:5000/removeEvent/', true);
        xhr.setRequestHeader("Content-Type", "application/json")
        console.log(JSON.stringify(obj));
        xhr.send(JSON.stringify(obj));
    }

    function updateEvent(eventid, eventname, date, course, color) {

        var obj = {"eventid" : eventid, "eventname" : eventname, "duedate" : date, "course" : course, "color" : color};

        var xhr = new XMLHttpRequest();
        xhr.open("POST", 'http://localhost:5000/updateEvent/', true);
        xhr.setRequestHeader("Content-Type", "application/json")
        console.log(JSON.stringify(obj));
        xhr.send(JSON.stringify(obj));
    }

    function addTaskCourse(id, task, course, date, details) {

        var obj = {"userid" : id, "taskname" : task, "course" : course, "date" : date, "details" : details};

        var xhr = new XMLHttpRequest();
        xhr.open("POST", 'http://localhost:5000/addTaskCourse/', true);
        xhr.setRequestHeader("Content-Type", "application/json")
        console.log(JSON.stringify(obj));
        xhr.send(JSON.stringify(obj));
    }

    function addTaskColor(id, task, color, date, details) {

        var obj = {"userid" : id, "taskname" : task, "color" : color, "date" : date, "details" : details};

        var xhr = new XMLHttpRequest();
        xhr.open("POST", 'http://localhost:5000/addTaskColor/', true);
        xhr.setRequestHeader("Content-Type", "application/json")
        console.log(JSON.stringify(obj));
        xhr.send(JSON.stringify(obj));
    }

    function removeTask(taskid) {

        var obj = {"taskid" : taskid};

        var xhr = new XMLHttpRequest();
        xhr.open("POST", 'http://localhost:5000/removeTask/', true);
        xhr.setRequestHeader("Content-Type", "application/json")
        console.log(JSON.stringify(obj));
        xhr.send(JSON.stringify(obj));
    }

    function updateTask(taskid, taskname, date, course, color, details) {

        var obj = {"taskid" : taskid, "taskname" : taskname, "duedate" : date, "course" : course, "color" : color, "details" : details};

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
        return xhr.responseText;
    }

    function getProjects(id) {
        console.log("hi");
        var userid = id;
            var xhr = new XMLHttpRequest();
            xhr.open("GET", 'http://localhost:5000/getProjects/' + userid, false);
        xhr.setRequestHeader("Content-Type", "application/json");
            xhr.send(null);
        return xhr.responseText;
    }