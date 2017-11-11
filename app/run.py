import os
import datetime
import config
import mysql.connector
from urllib2 import HTTPError
from flask import Flask, render_template, url_for, redirect, request, session, jsonify, g
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, current_user, login_user, UserMixin
from requests_oauthlib import OAuth2Session

app = Flask(__name__)
app.config.from_object(config)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.session_protection = 'strong'


class UserData(db.Model, UserMixin):
    __tablename__ = 'samwisedb.UserData'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=True)
    netid = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())


def google_auth(state=None, token=None):
    if token:
        return OAuth2Session(app.config['GOOGLE_CLIENT_ID'], token=token)
    if state:
        return OAuth2Session(
            app.config['GOOGLE_CLIENT_ID'],
            state=state,
            redirect_uri=app.config['REDIRECT_URI']
        )
    return OAuth2Session(
        app.config['GOOGLE_CLIENT_ID'],
        redirect_uri=app.config['REDIRECT_URI'],
        scope=app.config['SCOPE']
    )


def get_db():
    if not hasattr(g, 'db'):
        g.db = mysql.connector.connect(user=os.getenv('SAMWISE_USERNAME'), password=os.getenv('SAMWISE_PASSWORD'),
                                       host=os.getenv('SAMWISE_DB'))
    return g.db


def access_denied():
    return jsonify({'status': 'Access denied.'})


def success():
    return jsonify({'status': 'Success'})


@login_manager.user_loader
def load_user(id):
    if id is None:
        return None
    return UserData.query.get(id)


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    session['next'] = url_for('index') if 'next' not in request.args else request.args['next']
    if current_user.is_authenticated:
        return redirect(session['next'])
    google = google_auth()
    auth_url, state = google.authorization_url(
        app.config['AUTH_URI'],
        access_type='offline'
    )
    session['oauth_state'] = state
    return redirect(auth_url)


@app.route('/gauth_callback')
def callback():
    session['next'] = url_for('index') if 'next' not in session else session['next']
    if current_user and current_user.is_authenticated:
        return redirect(session['next'])
    if 'error' in request.args:
        print('error while logging in: %s' % request['error'])
        return redirect(url_for('index'))
    if 'code' not in request.args and 'state' not in request.args:
        print('error while logging in: %s' % request['error'])
        return redirect(url_for('login'))
    google = google_auth(state=session['oauth_state'])
    try:
        token = google.fetch_token(
            app.config['TOKEN_URI'],
            client_secret=app.config['GOOGLE_CLIENT_SECRET'],
            authorization_response=request.url
        )
    except HTTPError:
        print('Encountered an HTTPError while logging in.')
        return redirect(url_for('index'))
    google = google_auth(token=token)
    resp = google.get(app.config['USER_INFO'])
    if resp.status_code == 200:
        user_data = resp.json()
        email = user_data['email']
        user = UserData.query.filter_by(email=email).first()
        if not user:
            user = UserData()
            user.email = email
        user.name = user_data['name']
        user.netid = email.split('@')[0]
        db.session.add(user)
        db.session.commit()
        login_user(user)
    return redirect(session['next'])


@app.route('/calendar')
@login_required
def calendar():
    print('Current user: %s' % current_user.netid)
    return render_template('calendar.html')


@app.route('/<userid>')
@login_required
def calData(userid):
    if current_user.netid == userid:
        return render_template('index.html', netid=userid)
    return redirect(url_for('index'))


@app.route('/getUserExams/<netId>')
@login_required
def getUserExams(netId):
    if current_user.netid == netId:
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
    return access_denied()


@app.route('/getAllCourses')
@login_required
def getAllCourses():
    # Open the connection to database
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute('SELECT DISTINCT courseId FROM samwisedb.Course ORDER BY courseId')
    data = [item[0] for item in cursor.fetchall()]
    return jsonify(data)


@app.route('/getUserCourses/<netId>')
@login_required
def getUserCourses(netId):
    if current_user.netid == netId:
        # Open the connection to database
        connection = get_db()
        cursor = connection.cursor()
        cursor.execute('SELECT DISTINCT courseId FROM samwisedb.User WHERE netId = %s', (netId,))
        data = [item[0] for item in cursor.fetchall()]
        return jsonify(data)
    return access_denied()


@app.route('/addCourse/', methods=['POST'])
@login_required
def addCourse():
    data = request.get_json(force=True)
    courseId = data['courseId']
    user = data['user']
    if current_user.netid == user:
        connection = get_db()
        cursor = connection.cursor()
        cursor.execute('SELECT * from samwisedb.User WHERE (userId, courseId) = (%s, %s)', (user, courseId))
        if len(cursor.fetchall() == 0):
            cursor.execute('INSERT INTO samwisedb.User(netId, courseId) VALUES (%s, %s)', (user, courseId))
        connection.commit()
        return success()
    return access_denied()


@app.route('/removeCourse/', methods=['POST'])
@login_required
def removeCourse():
    data = request.get_json(force=True)
    courseId = data['courseId']
    userId = data['userId']
    if current_user.netid == userId:
        connection = get_db()
        cursor = connection.cursor()
        cursor.execute('DELETE FROM samwisedb.User WHERE (userId, courseId) = (%s, %s)', (userId, courseId))
        connection.commit()
        return success()
    return access_denied()


@app.route('/getProjects/<userId>')
@login_required
def getProjects(userId):
    if current_user.netid == userId:
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
    return access_denied()


@app.route('/removeProject/', methods=['POST'])
@login_required
def removeProject():
    data = request.get_json(force=True)
    projectId = data['projectId']
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute('SELECT user FROM samwisedb.Project WHERE projectId = %s', (projectId,))
    user_rows = cursor.fetchall()

    if len(user_rows) > 0 and current_user.netid == user_rows[0][0]:
        cursor.execute('DELETE FROM samwisedb.Project WHERE projectId = %s', (projectId,))
        cursor.execute('DELETE FROM samwisedb.Subtask WHERE projectId = %s', (projectId,))
        connection.commit()
        return success()
    return access_denied()


@app.route('/updateProject/', methods=['POST'])
@login_required
def updateProject():
    data = request.get_json(force=True)
    projectId = data['projectid']
    projectName = data['projectname']
    dueDate = data['duedate']
    courseId = data['course']

    connection = get_db()
    cursor = connection.cursor()
    cursor.execute('SELECT user FROM samwisedb.Project WHERE projectId = %s', (projectId,))
    user_rows = cursor.fetchall()

    if len(user_rows) > 0 and current_user.netid == user_rows[0][0]:
        cursor.execute('''
           UPDATE samwisedb.Project
           SET projectName=%s, dueDate=%s, courseId=%s
           WHERE projectId=%s
        ''', (projectName, dueDate, courseId, projectId))
        connection.commit()
        return jsonify(data)
    return access_denied()


@app.route('/addProject/', methods=['POST'])
@login_required
def addProject():
    data = request.get_json(force=True)
    userId = data['userId']
    projectName = data['projectName']
    courseId = data['courseId']
    dueDate = data['dueDate']
    subtasks = data['subtasks']
    if current_user.netid == userId:
        connection = get_db()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO samwisedb.Project(user, projectName, dueDate, courseId) VALUES (%s, %s, %s, %s)',
                       (userId, projectName, dueDate, courseId))
        projectId = cursor.lastrowid
        for subtask in subtasks:
            cursor.execute('INSERT INTO samwisedb.Subtask(projectId, subtaskName) VALUES (%s, %s)',
                           (projectId, subtask))
        connection.commit()
        return jsonify([projectId])
    return access_denied()


@app.route('/getEvents/<userid>')
@login_required
def getEvents(userid):
    if current_user.netid == userid:
        connection = get_db()
        cursor = connection.cursor()
        cursor.execute('SELECT DISTINCT * FROM samwisedb.Event WHERE user = %s', (userid,))
        data = [{'eventId': str(item[1]), 'eventName': str(item[2]), 'startTime': str(item[3]), 'endTime': str(item[4]),
                 'tagId': str(item[5]), 'notes': str(item[6]), 'location': str(item[7])} for
                item in cursor.fetchall()]
        return jsonify(data)


@app.route('/removeEvent/', methods=['POST'])
@login_required
def removeEvent():
    data = request.get_json(force=True)
    eventId = data['eventId']
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute('SELECT user FROM samwisedb.Event WHERE eventId = %s', (eventId,))
    user_rows = cursor.fetchall()

    if len(user_rows) > 0 and current_user.netid == user_rows[0][0]:
        cursor.execute('DELETE FROM samwisedb.Event WHERE eventId = %s', eventId)
        connection.commit()
        return success()
    return access_denied()


@app.route('/addEvent/', methods=['POST'])
@login_required
def addEvent():
    data = request.get_json(force=True)
    user = data['user']
    eventName = data['eventName']
    startTime = data['startTime']
    endTime = data['endTime']
    tagId = data['tagId']
    notes = data['notes']
    location = data['location']
    if current_user.netid == user:
        connection = get_db()
        cursor = connection.cursor()
        cursor.execute(
            'INSERT INTO samwisedb.Event(user, eventName, startTime, endTime, tagId, notes, location) values (%s, %s, %s, %s, %s, %s, %s)',
            (user, eventName, startTime, endTime, tagId, notes, location))
        connection.commit()
        event_id = cursor.lastrowid
        return jsonify([event_id])
    return access_denied()


@app.route('/updateEvent/', methods=['POST'])
@login_required
def updateEvent():
    data = request.get_json(force=True)
    eventId = data['eventId']
    eventName = data['eventName']
    startTime = data['startTime']
    endTime = data['endTime']
    tagId = data['tagId']
    notes = data['notes']
    location = data['location']
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute('SELECT user FROM samwisedb.Event WHERE eventId = %s', (eventId,))
    user_rows = cursor.fetchall()

    if len(user_rows) > 0 and current_user.netid == user_rows[0][0]:
        cursor.execute(
            'UPDATE samwisedb.Event SET eventName=%s, startTime=%s, endTime=%s, tagId=%s, notes=%s, location=%s WHERE eventId=%s',
            (eventName, startTime, endTime, tagId, eventId, notes, location))
        connection.commit()
        return success()
    return access_denied()


@app.route('/getTasks/<userId>', methods=['GET'])
@login_required
def getTasks(userId):
    if current_user.netid == userId:
        connection = get_db()
        cursor = connection.cursor()
        cursor.execute('SELECT DISTINCT * FROM samwisedb.Task WHERE user = %s', (userId,))
        data = [{
            'user': item[0],
            'taskId': item[1],
            'taskName': item[2],
            'courseId': item[3],
            'tag': item[4],
            'startDate': item[5],
            'dueDate': item[6],
            'details': item[7]
        } for item in cursor.fetchall()]
        return jsonify(data)
    return access_denied()


@app.route('/removeTask/', methods=['POST'])
@login_required
def removeTask():
    data = request.get_json(force=True)
    taskId = data['taskid']

    connection = get_db()
    cursor = connection.cursor()
    cursor.execute('SELECT user FROM samwisedb.Task WHERE taskId = %s', (taskId,))
    user_rows = cursor.fetchall()

    if len(user_rows) > 0 and current_user.netid == user_rows[0][0]:
        cursor.execute('DELETE FROM samwisedb.Task WHERE taskId = %s', taskId)
        connection.commit()
        return success()
    return access_denied()


@app.route('/addTask/', methods=['POST'])
@login_required
def addTask():
    data = request.get_json(force=True)
    userid = data['userid']
    taskname = data['taskname']
    course = data['course']
    tag = data['tag']
    startdate = data['startdate']
    duedate = data['duedate']
    details = data['details']
    if current_user.netid == userid:
        connection = get_db()
        cursor = connection.cursor()
        cursor.execute(
            '''INSERT INTO samwisedb.Task(user, taskName, courseId, tag, startDate, dueDate, details)
            VALUES (%s, %s, %s, %s, %s, %s, %s)''',
            (userid, taskname, course, tag, startdate, duedate, details))
        connection.commit()
        task_id = cursor.lastrowid
        return jsonify([task_id])
    return access_denied()


@app.route('/updateTask/', methods=['POST'])
@login_required
def updateTask():
    data = request.get_json(force=True)
    taskid = data['taskid']
    taskname = data['taskname']
    details = data['details']
    duedate = data['duedate']
    course = data['course']

    taskid = int(taskid)

    connection = get_db()
    cursor = connection.cursor()
    cursor.execute('SELECT user FROM samwisedb.Task WHERE taskId = %s', (taskid,))
    user_rows = cursor.fetchall()

    if len(user_rows) > 0 and current_user.netid == user_rows[0][0]:
        cursor.execute('''
           UPDATE samwisedb.Task
           SET taskName=%s, dueDate=%s, courseId=%s, details=%s
           WHERE taskId=%s
        ''', (taskname, duedate, course, details, taskid))
        connection.commit()
        return success()
    return access_denied()


@app.route('/exams/<course_id>')
@login_required
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
    data = [{'course': courseId + ' Class', 'start': str(item[0])} for item in cursor.fetchall()]
    return jsonify(data)


@app.route('/addSubtask/', methods=['POST'])
@login_required
def addSubtask():
    data = request.get_json(force=True)
    projectId = data['projectId']
    subtask = data['subtask']
    connection = get_db()
    cursor = connection.cursor()

    cursor.execute('SELECT user FROM samwisedb.Project WHERE projectId = %s', (projectId,))
    user_rows = cursor.fetchall()

    if len(user_rows) > 0 and current_user.netid == user_rows[0][0]:
        cursor.execute('INSERT INTO samwisedb.Subtask(projectId, subtask) VALUES (%s, %s)', (projectId, subtask))
        connection.commit()
        subtaskId = cursor.lastrowid
        return jsonify([subtaskId])
    return access_denied()


@app.route('/removeSubtask/', methods=['POST'])
@login_required
def removeSubtask():
    data = request.get_json(force=True)
    subtaskId = data['subtaskId']
    connection = get_db()
    cursor = connection.cursor()

    user = get_user_from_subtask_id(subtaskId)
    if user and current_user.netid == user:
        cursor.execute('DELETE FROM samwisedb.Subtask WHERE subtaskId = %s', (subtaskId,))
        connection.commit()
        return jsonify([subtaskId])
    return access_denied()


@app.route('/updateSubtask/', methods=['POST'])
@login_required
def updateSubtask():
    data = request.get_json(force=True)
    subtaskId = data['subtaskId']
    subtaskName = data['subtaskName']
    connection = get_db()
    cursor = connection.cursor()
    user = get_user_from_subtask_id(subtaskId)
    if user and current_user.netid == user:
        cursor.execute('UPDATE samwisedb.Subtask SET subtaskName = %s WHERE subtaskId = %s', (subtaskName, subtaskId))
        connection.commit()
        return jsonify([subtaskName])
    return access_denied()


@app.route('/getColor/<name>')
@login_required
def getColor(name):
    return jsonify([app.config['COLORS'][hash(name) % len(app.config['COLORS'])]])


@app.route('/getUserCourseColor/<userId>/<courseId>')
@login_required
def getUserCourseColor(userId, courseId):
    if current_user.netid == userId:
        # Open the connection to database
        connection = get_db()
        cursor = connection.cursor()
        cursor.execute('SELECT netId, courseId, color FROM samwisedb.User WHERE netId = %s AND courseId = %s',
                       (userId, courseId))
        data = [item[2] for item in cursor.fetchall()]
        return jsonify(data)
    return access_denied()


def get_user_from_subtask_id(subtask_id):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute('SELECT projectId FROM samwisedb.Subtask WHERE subtaskId = %s', (subtask_id,))
    rows = cursor.fetchall()
    projectId = -1 if len(rows) == 0 else rows[0][0]
    cursor.execute('SELECT user FROM samwisedb.Project WHERE projectId = %s', (projectId,))
    user_rows = cursor.fetchall()
    return None if len(user_rows) == 0 else user_rows[0][0]


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
