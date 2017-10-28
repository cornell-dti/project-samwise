import json
import os
import mysql.connector
from flask import Flask, render_template, url_for, redirect, request, session, jsonify, g

app = Flask(__name__)
app.config.from_object('config')

def get_db():
    if not hasattr(g, 'db'):
        g.db = mysql.connector.connect(user=os.getenv('SAMWISE_USERNAME'), password=os.getenv('SAMWISE_PASSWORD'),
                                       host=os.getenv('SAMWISE_DB'))
    return g.db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()


@app.route("/")
def index():
    if 'netid' in session:
        app.logger.debug('NetID: ' + session['netid'])
        return redirect(url_for('calData', userid=session['netid']))
    return render_template("index.html")


@app.route("/calendar")
def calendar():
    return render_template("calendar.html")


@app.route("/<userid>")
def calData(userid):
    if 'netid' in session:
        app.logger.debug('User ID Data For ' + session['netid'])
        return render_template("index.html", netid=userid)
    return redirect(url_for('index'))


@app.route('/getUserExams/<netId>')
def getUserExams(netId):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute('SELECT courseId FROM samwisedb.User WHERE netId = %s', (netId,))
    courses = [item[0] for item in cursor.fetchall()]
    data = []
    for courseId in courses:
        cursor.execute('SELECT sections, time FROM samwisedb.Exam WHERE courseId = %s', (courseId,))
        exam = [{'courseId': courseId, 'section': item[0], 'start': item[1]} for item in cursor.fetchall()]
        data.append(exam)
    return jsonify(data)


@app.route('/getAllCourses')
def getAllCourses():
    # Open the connection to database
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute('SELECT DISTINCT courseId FROM samwisedb.Course ORDER BY courseId')
    data = [item[0] for item in cursor.fetchall()]
    return jsonify(data)


@app.route('/getUserCourses/<netId>')
def getUserCourses(netId):
    # Open the connection to database
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute('SELECT DISTINCT courseId FROM samwisedb.User WHERE netId = %s', (netId,))
    data = [item[0] for item in cursor.fetchall()]
    return jsonify(data)


@app.route('/addCourse/', methods=['POST'])
def addCourse():
    data = request.get_json(force=True)
    courseId = data['courseId']
    user = data['user']
    connection = get_db()
    cursor = connection.cursor()
    # TODO: Make sure course exists and use does not already have course
    cursor.execute('INSERT INTO samwisedb.User(netId, courseId) VALUES (%s, %s)', (user, courseId))
    connection.commit()
    return jsonify([])


@app.route('/removeCourse/', methods=['POST'])
def removeCourse():
    data = request.get_json(force=True)
    courseId = data['courseId']
    userId = data['userId']
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM samwisedb.User WHERE (userId, courseId) = (%s, %s)', (userId, courseId))
    connection.commit()
    return jsonify([])


@app.route('/getProjects/<userId>')
def getProjects(userId):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute('SELECT DISTINCT * FROM samwisedb.Project WHERE user = %s', (userId,))
    data = [{'projectId': item[1], 'projectName': item[2], 'date': item[3], 'courseId': item[4]} for item in
            cursor.fetchall()]
    for d in data:
        cursor.execute('SELECT subtaskName FROM samwisedb.Subtask WHERE projectId = %s', (d['projectId'],))
        subtasks = [item[0] for item in cursor.fetchall()]
        d['subtasks'] = subtasks
    return jsonify(data)


@app.route('/removeProject/', methods=['POST'])
def removeProject():
    data = request.get_json(force=True)
    projectId = data['projectId']
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM samwisedb.Project WHERE projectId = %s', (projectId,))
    cursor.execute('DELETE FROM samwisedb.Subtask WHERE projectId = %s', (projectId,))
    connection.commit()
    return jsonify([])


@app.route('/updateProject/', methods=['POST'])
def updateProject():
    data = request.get_json(force=True)
    projectId = data['projectid']
    projectName = data['projectname']
    dueDate = data['duedate']
    courseId = data['course']

    connection = get_db()
    cursor = connection.cursor()
    cursor.execute('''
       UPDATE samwisedb.Project
       SET projectName=%s, dueDate=%s, courseId=%s
       WHERE projectId=%s
    ''', (projectName, dueDate, courseId, projectId))
    connection.commit()
    return jsonify(data)


@app.route('/addProject/', methods=['POST'])
def addProject():
    data = request.get_json(force=True)
    userId = data['userId']
    projectName = data['projectName']
    courseId = data['courseId']
    dueDate = data['dueDate']
    subtasks = data['subtasks']

    connection = get_db()
    cursor = connection.cursor()
    cursor.execute('INSERT INTO samwisedb.Project(userId, projectName, dueDate, courseId) VALUES (%s, %s, %s, %s)',
                   (userId, projectName, dueDate, courseId))
    projectId = cursor.lastrowid
    for subtask in subtasks:
        cursor.execute('INSERT INTO samwisedb.Subtask(projectId, subtaskName) VALUES (%s, %s)', (projectId, subtask))
    connection.commit()
    return jsonify([projectId])


@app.route('/getEvents/<userid>')
def getEvents(userid):
    connection = get_db()

    cursor = connection.cursor()

    query = "SELECT DISTINCT * FROM samwisedb.Event WHERE user = \"" + userid + "\";"
    cursor.execute(query)

    data = [{"eventName": str(item[2]), "startTime": str(item[3]), "endTime": str(item[4]), "tagId": str(item[5])} for
            item in cursor.fetchall()]

    return json.dumps(data)


@app.route('/removeEvent/', methods=['POST'])
def removeEvent():
    if request.method == 'POST':
        data = request.get_json(force=True)
        eventId = data['eventId']

        connection = get_db()

        try:
            cursor = connection.cursor()
            query = "DELETE FROM samwisedb.Event WHERE eventId = \"" + eventId + "\";"
            print(query)
            cursor.execute(query)
            connection.commit()
        finally:
            print ("DONE")

    return json.dumps([])


@app.route('/addEvent/', methods=['POST'])
def addEvent():
    event_id = -1
    if request.method == 'POST':
        data = request.get_json(force=True)
        user = data['user']
        eventName = data['eventName']
        startTime = data['startTime']
        endTime = data['endTime']
        tagId = data['tagId']

        connection = get_db()

        try:
            cursor = connection.cursor()
            query = "insert into samwisedb.Event(user, eventName, startTime, endTime, tagId) values (\"" + user + "\", \"" + eventName + "\", \"" + startTime + "\", \"" + endTime + "\", \"" + tagId + "\");"
            print(query)
            cursor.execute(query)
            connection.commit()
            event_id = cursor.lastrowid
        finally:
            print ("DONE")
    return json.dumps([event_id])


@app.route('/updateEvent/', methods=['POST'])
def updateEvent():
    if request.method == 'POST':
        data = request.get_json(force=True)
        eventId = data['eventId']
        eventName = data['eventName']
        startTime = data['startTime']
        endTime = data['endTime']
        tagId = data['tagId']

        connection = get_db()

        try:
            cursor = connection.cursor()
            cursor.execute("""
               UPDATE samwisedb.Event
               SET eventName=%s, startTime=%s, endTime=%s, tagId=%s
               WHERE eventId=%s
            """, (eventName, startTime, endTime, tagId, eventId))
            connection.commit()
        finally:
            print ("DONE")

    return json.dumps([])


@app.route('/getTasks/<userId>', methods=['GET'])
def getTasks(userId):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute('SELECT DISTINCT * FROM samwisedb.Task WHERE user = %s', (userId,))
    data = [{
        'user': item[0],
        'taskId': item[1],
        'taskName': item[2],
        'courseId': item[3],
        'tag': item[4],
        'dueDate': item[5],
        'details': item[6]
    } for item in cursor.fetchall()]

    return jsonify(data)


@app.route('/removeTask/', methods=['POST'])
def removeTask():
    data = request.get_json(force=True)
    taskId = data['taskid']

    connection = get_db()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM samwisedb.Task WHERE taskId = %s', taskId)
    connection.commit()

    return json.dumps([])


@app.route('/addTask/', methods=['POST'])
def addTaskCourse():
    task_id = -1
    if request.method == 'POST':
        data = request.get_json(force=True)
        userid = data['userid']
        taskname = data['taskname']
        course = data['course']
        duedate = data['duedate']
        details = data['details']

        connection = get_db()

        try:
            cursor = connection.cursor()
            query = "INSERT into samwisedb.Task(user, taskName, courseId, dueDate, details) values (\"" + userid + "\", \"" + taskname + "\", \"" + course + "\", \"" + duedate + "\", \"" + details + "\");"
            print(query)
            cursor.execute(query)
            connection.commit()
            task_id = cursor.lastrowid
        finally:
            print ("DONE")
    return json.dumps([task_id])


@app.route('/updateTask/', methods=['POST'])
def updateTask():
    if request.method == 'POST':
        data = request.get_json(force=True)
        taskid = data['taskid']
        taskname = data['taskname']
        details = data['details']
        duedate = data['duedate']
        course = data['course']

        taskid = int(taskid)

        connection = get_db()

        try:
            cursor = connection.cursor()
            cursor.execute("""
               UPDATE samwisedb.Task
               SET taskName=%s, dueDate=%s, courseId=%s, details=%s
               WHERE taskId=%s
            """, (taskname, duedate, course, details, taskid))
            connection.commit()
        finally:
            print ("DONE")

    return json.dumps([])


@app.route('/exams/<course_id>')
def getExams(course_id):
    # Open the connection to database
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute('SELECT time FROM samwisedb.Exam WHERE courseId = %s', (course_id,))
    data = [{'course_id': course_id, 'start': item[0]} for item in cursor.fetchall()]
    return jsonify(data)


@app.route('/courses/<courseId>')
def getClassInfo(courseId):
    # Open the connection to database
    connection = get_db()

    cursor = connection.cursor()
    cursor.execute('SELECT startTime FROM samwisedb.Course WHERE courseId = %s', courseId)
    data = [{"course": courseId + " Class", "start": str(item[0])} for item in cursor.fetchall()]
    return json.dumps(data)


@app.route('/addSubtask/', methods=['POST'])
def addSubtask():
    data = request.get_json(force=True)
    projectId = data['projectId']
    subtask = data['subtask']
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute('INSERT INTO samwisedb.Subtask(projectId, subtask) VALUES (%s, %s)', (projectId, subtask))
    subtaskId = cursor.lastrowid
    connection.commit()
    return jsonify([subtaskId])


@app.route('/removeSubtask/', methods=['POST'])
def removeSubtask():
    data = request.get_json(force=True)
    subtaskId = data['subtaskId']
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM samwisedb.Subtask WHERE subtaskId = %s', (subtaskId,))
    connection.commit()
    return jsonify([subtaskId])


@app.route('/updateSubtask/', methods=['POST'])
def updateSubtask():
    data = request.get_json(force=True)
    subtaskId = data['subtaskId']
    subtaskName = data['subtaskName']
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute('UPDATE samwisedb.Subtask SET subtaskName = %s WHERE subtaskId = %s', (subtaskName, subtaskId))
    connection.commit()
    return jsonify([subtaskName])


@app.route('/getColor/<name>')
def getColor(name):
    return app.config['COLORS'][hash(name) % len(app.config['COLORS'])]


if __name__ == "__main__":
    app.run(debug=True)
