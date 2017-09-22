import json
import random
import string
import mysql.connector
from flask import Flask, render_template, Response, make_response, request, send_file, session
from flask import url_for, current_app, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from auth import OAuthSignIn
import datetime

from googleapiclient.discovery import build


import httplib2
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from oauth2client.client import GoogleCredentials

import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

from simplekv.memory import DictStore
from flask_kvsession import KVSessionExtension


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

@app.route('/cal/<userid>/getExams')
def getUserExams(userid):
	if 'netid' in session:
		connection = mysql.connector.connect(user='samwise', password='3XJ73bgCS87mfvbe', host='samwisedata.ckbdcr0vghnq.us-east-1.rds.amazonaws.com')

		cursor = connection.cursor()

		query = "SELECT DISTINCT course FROM samwisedb.users WHERE netid = \"" + userid + "\";"
		cursor.execute(query)

		courses = [str(item[0]) for item in cursor.fetchall()]

		data = []

		for course in courses:
			query = "SELECT time FROM samwisedb.exams WHERE course = \"" + course + "\";"
			cursor.execute(query)

			newdata = [{"title" : course + " Exam", "start" : str(item[0])} for item in cursor.fetchall()]
			data += newdata

		connection.close()

		return json.dumps(data)
	else:
		return json.dumps([])

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

@app.route('/cal/<userid>/<course>')
def addCourse(userid, course):
	if 'netid' in session:
		connection = mysql.connector.connect(user='samwise', password='3XJ73bgCS87mfvbe', host='samwisedata.ckbdcr0vghnq.us-east-1.rds.amazonaws.com')

		try:
			cursor = connection.cursor()
			query = "insert into samwisedb.users(netid, course) values (\"" + userid + "\", \"" + course + "\");"
			print(query)
			cursor.execute(query)
			connection.commit()
		finally:
			print ("DONE")
			connection.close()
	return redirect(url_for('index'))

@app.route('/getProjects/<userid>')
def getProjects(userid):
	connection = mysql.connector.connect(user='samwise', password='3XJ73bgCS87mfvbe', host='samwisedata.ckbdcr0vghnq.us-east-1.rds.amazonaws.com')

	print ("connected to db to get projects")
	cursor = connection.cursor()

	query = "SELECT DISTINCT * FROM samwisedb.projects WHERE user = \"" + userid + "\";"
	cursor.execute(query)

	data = [{"projectname" : str(item[2]),  "date" : str(item[3]), "id" : str(item[0]), "course" : str(item[4]), "color" : str(item[5])} for item in cursor.fetchall()]

	for d in data:
		query = "SELECT subtask FROM samwisedb.subtasks WHERE id = \"" + d["id"] + "\";"
		cursor.execute(query)
		subtasks = [item[0] for item in cursor.fetchall()]
		d["subtasks"] = subtasks

	print ("DONE")
	connection.close()

	return json.dumps(data)

@app.route('/removeProject/', methods=['POST'])
def removeProject():
	if request.method == 'POST':
		data = request.get_json(force=True)
		projectname=data['projectname']

		connection = mysql.connector.connect(user='samwise', password='3XJ73bgCS87mfvbe', host='samwisedata.ckbdcr0vghnq.us-east-1.rds.amazonaws.com')

		try:
			cursor = connection.cursor()
			query = "DELETE FROM samwisedb.projects WHERE projectname = \"" + projectname + "\";"
			print(query)
			cursor.execute(query)
			connection.commit()
		finally:
			print ("DONE")
			connection.close()

	return json.dumps([])

@app.route('/updateProject/', methods=['POST'])
def updateProject():
	if request.method == 'POST':
		data = request.get_json(force=True)
		projectid=data['projectid']
		projectname=data['projectname']
		duedate=data['duedate']
		course=data['course']
		color=data['color']

		connection = mysql.connector.connect(user='samwise', password='3XJ73bgCS87mfvbe', host='samwisedata.ckbdcr0vghnq.us-east-1.rds.amazonaws.com')

		try:
			cursor = connection.cursor()
			cursor.execute ("""
			   UPDATE samwisedb.projects
			   SET projectname=%s, duedate=%s, course=%s, color=%s
			   WHERE id=%s
			""", (projectname, duedate, course, color, projectid))
			connection.commit()
		finally:
			print ("DONE")
			connection.close()

	return json.dumps([])

@app.route('/addProjectColor/', methods=['POST'])
def addProjectColor():
	proj_id = -1
	if request.method == 'POST':
		data = request.get_json(force=True)
		userid=data['userid']
		project=data['project']
		color=data['color']
		duedate=data['duedate']
		subtasks = data['subtasks']

		connection = mysql.connector.connect(user='samwise', password='3XJ73bgCS87mfvbe', host='samwisedata.ckbdcr0vghnq.us-east-1.rds.amazonaws.com')



		try:
			cursor = connection.cursor()
			query = "insert into samwisedb.projects(user, projectname, duedate, color) values (\"" + userid + "\", \"" + project + "\", \"" +  duedate + "\", \"" + color + "\");"
			print(query)
			cursor.execute(query)
			connection.commit()
			proj_id = cursor.lastrowid
		finally:
			for subtask in subtasks:
				try:
					cursor = connection.cursor()
					query = "insert into samwisedb.subtasks(id, subtask) values (\"" + str(proj_id) + "\", \"" + subtask + "\");"
					print(query)
					cursor.execute(query)
					connection.commit()
				finally:
					print ("DONE")
		connection.close()
	return json.dumps([proj_id])


@app.route('/addProjectCourse/', methods=['POST'])
def addProjectCourse():
	proj_id = -1
	if request.method == 'POST':
		data = request.get_json(force=True)
		userid=data['userid']
		project=data['project']
		course=data['course']
		duedate=data['duedate']
		subtasks = data['subtasks']

		connection = mysql.connector.connect(user='samwise', password='3XJ73bgCS87mfvbe', host='samwisedata.ckbdcr0vghnq.us-east-1.rds.amazonaws.com')



		try:
			cursor = connection.cursor()
			query = "insert into samwisedb.projects(user, projectname, duedate, course) values (\"" + userid + "\", \"" + project + "\", \"" + duedate + "\", \"" + course + "\");"
			print(query)
			cursor.execute(query)
			connection.commit()
			proj_id = cursor.lastrowid
		finally:
			for subtask in subtasks:
				try:
					cursor = connection.cursor()
					query = "insert into samwisedb.subtasks(id, subtask) values (\"" + str(proj_id) + "\", \"" + subtask + "\");"
					print(query)
					cursor.execute(query)
					connection.commit()
				finally:
					print ("DONE")
		connection.close()
	return json.dumps([proj_id])


@app.route('/getEvents/<userid>')
def getEvents(userid):
	connection = mysql.connector.connect(user='samwise', password='3XJ73bgCS87mfvbe', host='samwisedata.ckbdcr0vghnq.us-east-1.rds.amazonaws.com')

	cursor = connection.cursor()

	query = "SELECT DISTINCT * FROM samwisedb.events WHERE user = \"" + userid + "\";"
	cursor.execute(query)

	data = [{"eventname" : str(item[1]), "date" : str(item[2]), "color" : str(item[3])} for item in cursor.fetchall()]

	return json.dumps(data)

@app.route('/removeEvent/', methods=['POST'])
def removeEvent():
	if request.method == 'POST':
		data = request.get_json(force=True)
		eventid=data['eventid']

		connection = mysql.connector.connect(user='samwise', password='3XJ73bgCS87mfvbe', host='samwisedata.ckbdcr0vghnq.us-east-1.rds.amazonaws.com')

		try:
			cursor = connection.cursor()
			query = "DELETE FROM samwisedb.events WHERE eventid = \"" + eventid + "\";"
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
		userid=data['userid']
		eventname=data['eventname']
		date=data['date']
		color=data['color']

		connection = mysql.connector.connect(user='samwise', password='3XJ73bgCS87mfvbe', host='samwisedata.ckbdcr0vghnq.us-east-1.rds.amazonaws.com')


		try:
			cursor = connection.cursor()
			query = "insert into samwisedb.events(user, eventname, date, color) values (\"" + userid + "\", \"" + eventname + "\", \"" + date + "\", \"" + color + "\");"
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
		eventid=data['eventid']
		eventname=data['eventname']
		date=data['date']
		course=data['course']
		color=data['color']

		connection = mysql.connector.connect(user='samwise', password='3XJ73bgCS87mfvbe', host='samwisedata.ckbdcr0vghnq.us-east-1.rds.amazonaws.com')

		try:
			cursor = connection.cursor()
			cursor.execute ("""
			   UPDATE samwisedb.events
			   SET eventname=%s, date=%s, course=%s, color=%s
			   WHERE id=%s
			""", (eventname, date, course, color, eventid))
			connection.commit()
		finally:
			print ("DONE")
			connection.close()

	return json.dumps([])


@app.route('/getTasks/<userid>', methods=['GET'])
def getTasks(userid):
	connection = mysql.connector.connect(user='samwise', password='3XJ73bgCS87mfvbe', host='samwisedata.ckbdcr0vghnq.us-east-1.rds.amazonaws.com')

	cursor = connection.cursor()

	query = "SELECT DISTINCT * FROM samwisedb.tasks WHERE user = \"" + userid + "\";"
	cursor.execute(query)

	data = [{"task" : str(item[1]), "course" : str(item[2]), "color" : str(item[3]), "date" : str(item[4]), "details" : str(item[5]), "taskid" : str(item[6])} for item in cursor.fetchall()]

	return json.dumps(data)

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

@app.route('/addTaskCourse/', methods=['POST'])
def addTaskCourse():
	task_id = -1
	if request.method == 'POST':
		data = request.get_json(force=True)
		userid=data['userid']
		taskname=data['taskname']
		date=data['date']
		details=data['details']
		course=data['course']

		connection = mysql.connector.connect(user='samwise', password='3XJ73bgCS87mfvbe', host='samwisedata.ckbdcr0vghnq.us-east-1.rds.amazonaws.com')

		try:
			cursor = connection.cursor()
			query = "insert into samwisedb.tasks(user, taskname, course, details, date) values (\"" + userid + "\", \"" + taskname + "\", \"" + course + "\", \"" + details + "\", \"" + date + "\");"
			print(query)
			cursor.execute(query)
			connection.commit()
			task_id = cursor.lastrowid
		finally:
			print ("DONE")
			connection.close()
	return json.dumps([task_id])

@app.route('/addTaskColor/', methods=['POST'])
def addTaskColor():
	task_id = -1
	if request.method == 'POST':
		data = request.get_json(force=True)
		userid=data['userid']
		taskname=data['taskname']
		date=data['date']
		details=data['details']
		color=data['color']

		connection = mysql.connector.connect(user='samwise', password='3XJ73bgCS87mfvbe', host='samwisedata.ckbdcr0vghnq.us-east-1.rds.amazonaws.com')

		try:
			cursor = connection.cursor()
			query = "insert into samwisedb.tasks(user, taskname, color, details, date) values (\"" + userid + "\", \"" + taskname + "\", \"" + color + "\", \"" + details + "\", \"" + date + "\");"
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
		date=data['date']
		course=data['course']
		color=data['color']

        taskid = int(taskid)

        connection = mysql.connector.connect(user='samwise', password='3XJ73bgCS87mfvbe', host='samwisedata.ckbdcr0vghnq.us-east-1.rds.amazonaws.com')

        try:
			cursor = connection.cursor()
			cursor.execute ("""
			   UPDATE samwisedb.tasks
			   SET taskname=%s, date=%s, course=%s, color=%s, details=%s
			   WHERE taskid=%d
			""", (taskname, date, course, color, details, taskid))
			connection.commit()
        finally:
			print ("DONE")
			connection.close()

	return json.dumps([])


@app.route('/exams/<course>')
def getExams(course):
	# Open the connection to database
	connection = mysql.connector.connect(user='samwise', password='3XJ73bgCS87mfvbe', host='samwisedata.ckbdcr0vghnq.us-east-1.rds.amazonaws.com')

	cursor = connection.cursor()

	query = "SELECT time FROM samwisedb.exams WHERE course = \"" + course + "\";"
	cursor.execute(query)

	data = [{"title" : course + " Exam", "start" : str(item[0])} for item in cursor.fetchall()]

	connection.close()

	return json.dumps(data)

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

if __name__ == "__main__":
	# db.create_all()
	lm.init_app(app)
	app.secret_key = open("/dev/random","rb").read(32)
	app.run(debug=True)
