import random
import json
import string
import httplib2
import datetime
import os
import mysql.connector
from flask import Flask, render_template, make_response, url_for, redirect, request, session, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from auth import OAuthSignIn
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from simplekv.memory import DictStore

# try:
#     import argparse
#     flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
# except ImportError:
#     flags = None

app = Flask(__name__)

app.config['GOOGLE_LOGIN_CLIENT_ID'] = '197302358001-s09lnod2vb7rltrkj9qn906tte1u4esp.apps.googleusercontent.com'
app.config['GOOGLE_LOGIN_CLIENT_SECRET'] = 'USV2G6fCF122c4433-rRDNMO'
app.config['SECRET_KEY'] = 'USV2G6fCF122c4433-rRDNMO'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['OAUTH_CREDENTIALS'] = {
    'google': {
            'id': '197302358001-s09lnod2vb7rltrkj9qn906tte1u4esp.apps.googleusercontent.com',
            'secret': 'USV2G6fCF122c4433-rRDNMO'
    }
}

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


# db = SQLAlchemy(app)
lm = LoginManager()
lm.login_view = 'index'


# See the simplekv documentation for details
store = DictStore()


# SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
# CLIENT_SECRET_FILE = 'client_secret.json'
# APPLICATION_NAME = 'Google Calendar API Python Quickstart'

@app.route("/")
def index():
    if 'netid' in session:
        app.logger.debug('NetID: ' + session['netid'])
        return redirect(url_for('calData', userid=session['netid']))
    return render_template("index.html")

@app.route('/', methods=['GET'])
def index2():
    """Initialize a session for the current user, and render index.html."""
    # Create a state token to prevent request forgery.
    # Store it in the session for later validation.
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                  for x in xrange(32))
    session['state'] = state
    # Set the Client ID, Token State, and Application Name in the HTML while
    # serving it.
    response = make_response(
        render_template('index.html',
                      CLIENT_ID=CLIENT_ID,
                      STATE=state,
                      APPLICATION_NAME=APPLICATION_NAME))
    response.headers['Content-Type'] = 'text/html'
    return response

@app.route("/calendar")
def calendar():
    return render_template("calendar.html")

@app.route("/cal/<userid>")
def calData(userid):
    if 'netid' in session:
        app.logger.debug('User ID Data For ' + session['netid'])
        return render_template("index.html", netid=userid)
    return redirect(url_for('index'))

@app.route('/cal/<netId>/getUserExams')
def getUserExams(netId):
    if 'netid' in session:
        connection = mysql.connector.connect(user='samwise', password='3XJ73bgCS87mfvbe', host='samwisedata.ckbdcr0vghnq.us-east-1.rds.amazonaws.com')
        cursor = connection.cursor()
        cursor.execute('SELECT courseId FROM samwisedb.User WHERE netId = %s', (netId,))
        courses = [item[0] for item in cursor.fetchall()]
        data = []
        for courseId in courses:
            cursor.execute('SELECT time FROM samwisedb.Exam WHERE courseId = %s', (courseId,))
            exam = [{'courseId': courseId, 'start': item[0]} for item in cursor.fetchall()]
            data.append(exam)
        connection.close()
        return jsonify(data)
    return jsonify([])

@app.route('/getAllClasses')
def getClasses():

    # Open the connection to database
    connection = mysql.connector.connect(user='samwise', password='3XJ73bgCS87mfvbe', host='samwisedata.ckbdcr0vghnq.us-east-1.rds.amazonaws.com')

    cursor = connection.cursor()

    query = "SELECT DISTINCT course FROM samwisedb.courses ORDER BY course;"
    cursor.execute(query)

    data = [item[0] for item in cursor.fetchall()]

    connection.close()

    return json.dumps(data)

@app.route('/cal/<userId>/<courseId>')
def addCourse(userId, courseId):
    if 'netid' in session:
        connection = mysql.connector.connect(user='samwise', password='3XJ73bgCS87mfvbe', host='samwisedata.ckbdcr0vghnq.us-east-1.rds.amazonaws.com')
        cursor = connection.cursor()
        # TODO: Make sure course exists and use does not already have course
        cursor.execute('INSERT INTO samwisedb.User(netId, courseId) VALUES (%s, %s)', (userId, courseId))
        connection.commit()
        connection.close()
    return redirect(url_for('index'))

@app.route('/removeCourse/', methods=['POST'])
def removeCourse():
    data = request.get_json(force=True)
    courseId = data['courseId']
    userId = data['userId']
    connection = mysql.connector.connect(user='samwise', password='3XJ73bgCS87mfvbe',
                                         host='samwisedata.ckbdcr0vghnq.us-east-1.rds.amazonaws.com')
    cursor = connection.cursor()
    cursor.execute('DELETE FROM samwisedb.User WHERE (userId, courseId) = (%s, %s)', (userId, courseId,))
    connection.commit()
    connection.close()
    return jsonify([])

@app.route('/getProjects/<userId>')
def getProjects(userId):
    connection = mysql.connector.connect(user='samwise', password='3XJ73bgCS87mfvbe', host='samwisedata.ckbdcr0vghnq.us-east-1.rds.amazonaws.com')
    cursor = connection.cursor()
    cursor.execute('SELECT DISTINCT * FROM samwisedb.Project WHERE user = %s', (userId,))
    data = [{'projectId': item[1], 'projectName': item[2], 'date': item[3], 'courseId': item[4]} for item in
            cursor.fetchall()]
    for d in data:
        cursor.execute('SELECT subtaskName FROM samwisedb.Subtask WHERE projectId = %s', (d['projectId'],))
        subtasks = [item[0] for item in cursor.fetchall()]
        d['subtasks'] = subtasks
    connection.close()
    return jsonify(data)

@app.route('/removeProject/', methods=['POST'])
def removeProject():
    data = request.get_json(force=True)
    projectId = data['projectId']
    connection = mysql.connector.connect(user='samwise', password='3XJ73bgCS87mfvbe', host='samwisedata.ckbdcr0vghnq.us-east-1.rds.amazonaws.com')
    cursor = connection.cursor()
    cursor.execute('DELETE FROM samwisedb.Project WHERE projectId = %s', (projectId,))
    cursor.execute('DELETE FROM samwisedb.Subtask WHERE projectId = %s', (projectId,))
    connection.commit()
    connection.close()
    return jsonify([])

@app.route('/updateProject/', methods=['POST'])
def updateProject():
    data = request.get_json(force=True)
    projectId = data['projectid']
    projectName = data['projectname']
    dueDate = data['duedate']
    courseId = data['course']

    connection = mysql.connector.connect(user='samwise', password='3XJ73bgCS87mfvbe', host='samwisedata.ckbdcr0vghnq.us-east-1.rds.amazonaws.com')
    cursor = connection.cursor()
    cursor.execute ('''
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

    connection = mysql.connector.connect(user='samwise', password='3XJ73bgCS87mfvbe', host='samwisedata.ckbdcr0vghnq.us-east-1.rds.amazonaws.com')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO samwisedb.Project(userId, projectName, dueDate, courseId) VALUES (%s, %s, %s, %s)', (userId, projectName, dueDate, courseId))
    projectId = cursor.lastrowid
    for subtask in subtasks:
        cursor.execute('INSERT INTO samwisedb.Subtask(projectId, subtaskName) VALUES (%s, %s)', (projectId, subtask))
    connection.commit()
    connection.close()
    return jsonify([projectId])


@app.route('/getEvents/<userid>')
def getEvents(userid):
    connection = mysql.connector.connect(user='samwise', password='3XJ73bgCS87mfvbe', host='samwisedata.ckbdcr0vghnq.us-east-1.rds.amazonaws.com')

    cursor = connection.cursor()

    query = "SELECT DISTINCT * FROM samwisedb.Event WHERE user = \"" + userid + "\";"
    cursor.execute(query)

    data = [{"eventName" : str(item[2]), "startTime" : str(item[3]), "endTime" : str(item[4]), "tagId" : str(item[5])} for item in cursor.fetchall()]

    return json.dumps(data)

@app.route('/removeEvent/', methods=['POST'])
def removeEvent():
    if request.method == 'POST':
        data = request.get_json(force=True)
        eventId=data['eventId']

        connection = mysql.connector.connect(user='samwise', password='3XJ73bgCS87mfvbe', host='samwisedata.ckbdcr0vghnq.us-east-1.rds.amazonaws.com')

        try:
            cursor = connection.cursor()
            query = "DELETE FROM samwisedb.Event WHERE eventId = \"" + eventId + "\";"
            print(query)
            cursor.execute(query)
            connection.commit()
        finally:
            print ("DONE")
            connection.close()

    return json.dumps([])

@app.route('/addEvent/', methods=['POST'])
def addEvent():
    event_id = -1
    if request.method == 'POST':
        data = request.get_json(force=True)
        user=data['user']
        eventName=data['eventName']
        startTime=data['startTime']
        endTime=data['endTime']
        tagId=data['tagId']

        connection = mysql.connector.connect(user='samwise', password='3XJ73bgCS87mfvbe', host='samwisedata.ckbdcr0vghnq.us-east-1.rds.amazonaws.com')


        try:
            cursor = connection.cursor()
            query = "insert into samwisedb.Event(user, eventName, startTime, endTime, tagId) values (\"" + user + "\", \"" + eventName + "\", \"" + startTime + "\", \"" + endTime + "\", \"" + tagId + "\");"
            print(query)
            cursor.execute(query)
            connection.commit()
            event_id = cursor.lastrowid
        finally:
            print ("DONE")
        connection.close()
    return json.dumps([event_id])

@app.route('/updateEvent/', methods=['POST'])
def updateEvent():
    if request.method == 'POST':
        data = request.get_json(force=True)
        eventId=data['eventId']
        eventName=data['eventName']
        startTime=data['startTime']
        endTime=data['endTime']
        tagId=data['tagId']

        connection = mysql.connector.connect(user='samwise', password='3XJ73bgCS87mfvbe', host='samwisedata.ckbdcr0vghnq.us-east-1.rds.amazonaws.com')

        try:
            cursor = connection.cursor()
            cursor.execute ("""
               UPDATE samwisedb.Event
               SET eventName=%s, startTime=%s, endTime=%s, tagId=%s
               WHERE eventId=%s
            """, (eventName, startTime, endTime, tagId, eventId))
            connection.commit()
        finally:
            print ("DONE")
            connection.close()

    return json.dumps([])


@app.route('/getTasks/<userId>', methods=['GET'])
def getTasks(userId):
    connection = mysql.connector.connect(user='samwise', password='3XJ73bgCS87mfvbe', host='samwisedata.ckbdcr0vghnq.us-east-1.rds.amazonaws.com')
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
    if request.method == 'POST':
        data = request.get_json(force=True)
        taskid=data['taskid']

        connection = mysql.connector.connect(user='samwise', password='3XJ73bgCS87mfvbe', host='samwisedata.ckbdcr0vghnq.us-east-1.rds.amazonaws.com')

        try:
            cursor = connection.cursor()
            query = "DELETE FROM samwisedb.tasks WHERE taskid = \"" + taskid + "\";"
            print(query)
            cursor.execute(query)
            connection.commit()
        finally:
            print ("DONE")
            connection.close()

    return json.dumps([])

@app.route('/addTask/', methods=['POST'])
def addTaskCourse():
    task_id = -1
    if request.method == 'POST':
        data = request.get_json(force=True)
        userid=data['userid']
        taskname=data['taskname']
        course=data['course']
        color=data['color']
        duedate=data['duedate']
        details=data['details']

        connection = mysql.connector.connect(user='samwise', password='3XJ73bgCS87mfvbe', host='samwisedata.ckbdcr0vghnq.us-east-1.rds.amazonaws.com')

        try:
            cursor = connection.cursor()
            query = "insert into samwisedb.tasks(user, taskname, course, color, duedate, details) values (\"" + userid + "\", \"" + taskname + "\", \"" + course + "\", \"" + color + "\", \"" + duedate + "\", \"" + details + "\");"
            print(query)
            cursor.execute(query)
            connection.commit()
            task_id = cursor.lastrowid
        finally:
            print ("DONE")
            connection.close()
    return json.dumps([task_id])


@app.route('/updateTask/', methods=['POST'])
def updateTask():
    if request.method == 'POST':
        data = request.get_json(force=True)
        taskid=data['taskid']
        taskname=data['taskname']
        details=data['details']
        duedate=data['duedate']
        course=data['course']
        color=data['color']

        taskid = int(taskid)

        connection = mysql.connector.connect(user='samwise', password='3XJ73bgCS87mfvbe', host='samwisedata.ckbdcr0vghnq.us-east-1.rds.amazonaws.com')

        try:
            cursor = connection.cursor()
            cursor.execute ("""
               UPDATE samwisedb.tasks
               SET taskname=%s, duedate=%s, course=%s, color=%s, details=%s
               WHERE taskid=%s
            """, (taskname, duedate, course, color, details, taskid))
            connection.commit()
        finally:
            print ("DONE")
            connection.close()

    return json.dumps([])


@app.route('/exams/<course_id>')
def getExams(course_id):
    # Open the connection to database
    connection = mysql.connector.connect(user='samwise', password='3XJ73bgCS87mfvbe', host='samwisedata.ckbdcr0vghnq.us-east-1.rds.amazonaws.com')
    cursor = connection.cursor()
    cursor.execute('SELECT time FROM samwisedb.Exam WHERE courseId = %s', (course_id,))
    data = [{'course_id': course_id, 'start': item[0]} for item in cursor.fetchall()]
    connection.close()
    return jsonify(data)

@app.route('/courses/<course>')
def getClassInfo(course):
    # Open the connection to database
    connection = mysql.connector.connect(user='samwise', password='3XJ73bgCS87mfvbe', host='samwisedata.ckbdcr0vghnq.us-east-1.rds.amazonaws.com')

    cursor = connection.cursor()

    query = "SELECT st FROM samwisedb.courses WHERE course = \"" + course + "\";"

    cursor.execute(query)

    weekday_range()

    d = datetime.date(2011, 7, 2)
    next_monday = next_weekday(d, 0) # 0 = Monday, 1=Tuesday, 2=Wednesday...

    data = [{"title" : course + " Class", "start" : str(item[0])} for item in cursor.fetchall()]

    connection.close()

    return json.dumps(data)

def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)

def weekday_range(sd, ed, weekday):
    weekday = next_weekday(sd, weekday)
    weekday_list = [weekday]
    delta = ed - weekday
    for i in range(delta+1):
        weekday += 7
        weekday_list.append(weekday)
        i += 7


@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()

class User(UserMixin):
    user_database = {}

    def __init__(self, netid, name):
        self.id = netid
        self.name = name

    @classmethod
    def get(cls,id):
        return cls.user_database.get(id)


@lm.request_loader
def load_user(request):
    token = request.headers.get('Authorization')
    if token is None:
        token = request.args.get('token')

    if token is not None:
        netid,name = token.split(":") # naive token
        user_entry = User.get(netid)
        if (user_entry is not None):
            user = User(user_entry[0],user_entry[1])
            if (user.name == name):
                return user
    return None

@lm.user_loader
def load_user(user_id):
    session['netid'] = user_id
    return User.get(user_id)


@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    name, email = oauth.callback()
    if email is None:
        flash('Not a valid email address')
        return redirect(url_for('index'))
    netid = email.split('@')[0]
    user = User.get(netid)
    if not user:
        user = User(netid=netid, name=name)

    user=User(netid=netid, name=name)

    login_user(user, remember=True)
    session['netid'] = netid
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html',
                           title='Sign In')

@app.route('/logout')
def logout():
    logout_user()
    session.pop('netid', None)
    return redirect(url_for('index'))

@app.route('/connect', methods=['POST'])
def connect():
    """Exchange the one-time authorization code for a token and
    store the token in the session."""
    # Ensure that the request is not a forgery and that the user sending
    # this connect request is the expected user.
    if request.args.get('state', '') != session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Normally, the state is a one-time token; however, in this example,
    # we want the user to be able to connect and disconnect
    # without reloading the page.  Thus, for demonstration, we don't
    # implement this best practice.
    # del session['state']

    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secret.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
    return response

    # An ID Token is a cryptographically-signed JSON object encoded in base 64.
    # Normally, it is critical that you validate an ID Token before you use it,
    # but since you are communicating directly with Google over an
    # intermediary-free HTTPS channel and using your Client Secret to
    # authenticate yourself to Google, you can be confident that the token you
    # receive really comes from Google and is valid. If your server passes the
    # ID Token to other components of your app, it is extremely important that
    # the other components validate the token before using it.
    gplus_id = credentials.id_token['sub']

    stored_credentials = session.get('credentials')
    stored_gplus_id = session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Store the access token in the session for later use.
    session['credentials'] = credentials
    session['gplus_id'] = gplus_id
    response = make_response(json.dumps('Successfully connected user.'), 200)
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/disconnect', methods=['POST'])
def disconnect():
    """Revoke current user's token and reset their session."""

    # Only disconnect a connected user.
    credentials = session.get('credentials')
    if credentials is None:
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Execute HTTP GET request to revoke current token.
    access_token = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset the user's session.
        del session['credentials']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

@app.route('/gsync', methods=['GET'])
def gsync():
    """Get Google calendar events into FullCalendar"""
    credentials = session.get('credentials')
    # Only fetch a list of people for connected users.
    if credentials is None:
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    try:
        # Create a new authorized API client
        http = httplib2.Http()
        http = credentials.authorize(http)
        service = discovery.build('calendar', 'v3', http=http)
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        eventsResult = service.events().list(
            calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
            orderBy='startTime').execute()
        events = eventsResult.get('items', [])

        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])

    except AccessTokenRefreshError:
        response = make_response(json.dumps("Failed to refresh access token."), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

@app.route('/addSubtask/', methods=['POST'])
def addSubtask():
    data = request.get_json(force=True)
    projectId = data['projectId']
    subtask = data['subtask']
    connection = mysql.connector.connect(user='samwise', password='3XJ73bgCS87mfvbe',
                                         host='samwisedata.ckbdcr0vghnq.us-east-1.rds.amazonaws.com')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO samwisedb.Subtask(projectId, subtask) VALUES (%s, %s)', (projectId, subtask))
    subtaskId = cursor.lastrowid
    connection.commit()
    connection.close()
    return jsonify([subtaskId])

@app.route('/removeSubtask/', methods=['POST'])
def removeSubtask():
    data = request.get_json(force=True)
    subtaskId = data['subtaskId']
    connection = mysql.connector.connect(user='samwise', password='3XJ73bgCS87mfvbe',
                                         host='samwisedata.ckbdcr0vghnq.us-east-1.rds.amazonaws.com')
    cursor = connection.cursor()
    cursor.execute('DELETE FROM samwisedb.Subtask WHERE subtaskId = %s', (subtaskId,))
    connection.commit()
    connection.close()
    return jsonify([subtaskId])

@app.route('/updateSubtask/', methods=['POST'])
def updateSubtask():
    data = request.get_json(force=True)
    subtaskId = data['subtaskId']
    subtaskName = data['subtaskName']
    connection = mysql.connector.connect(user='samwise', password='3XJ73bgCS87mfvbe',
                                         host='samwisedata.ckbdcr0vghnq.us-east-1.rds.amazonaws.com')
    cursor = connection.cursor()
    cursor.execute('UPDATE samwisedb.Subtask SET subtaskName = %s WHERE subtaskId = %s', (subtaskName, subtaskId))
    connection.commit()
    connection.close()
    return jsonify([subtaskName])

if __name__ == "__main__":
    # db.create_all()
    lm.init_app(app)
    app.secret_key = os.urandom(32)
    app.run(debug=True)
