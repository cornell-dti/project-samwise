from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from collections import namedtuple
from datetime import datetime
import requests
import time
import mysql.connector

courses = {}
Exam = namedtuple("Exam", "section date")

# Check to see what month it is
month = time.strftime("%m")
semester = "spring"
# If it is later than June, search for the fall exams, otherweise search for spring exams
if (int(month) > 6):
	semester = "fall"
r_final = requests.get("https://registrar.cornell.edu/exams/" + semester + "-final-exam-schedule")
r_prelim = requests.get("https://registrar.cornell.edu/exams/" + semester + "-prelim-schedule")

# FINALS -- stores in final_exams list
soup = BeautifulSoup(r_final.text, "html.parser")
lines = soup.prettify().split('\n')

for line in lines:
	if len(line) > 10:
		# If the line starts with an uppercase letter (for the course code)
		# AND the last 2 characters of the line are either AM or PM
		if line[0].isupper() and line[1].isupper():

			# Split the line to get the course number and date/time
			sections = line.split(' ', 3)
			print(sections)
			course = str(sections[0] + sections[1])
			date = str(sections[3].strip())

			# Format the date to be in correct for MySQL
			date = date.split(', ')[1]
			datesplit = date.split('  ')
			date = datesplit[0] +  datesplit[1] + ' ' + datesplit[len(datesplit) - 1]
			date += (' ' + time.strftime("%Y"))
			# print "TESTING " + time.strftime("%Y")
			# print "TESTING " + date
			dt = datetime.strptime(date, '%b %d %I:%M %p %Y')
			date = datetime.strftime(dt, '%Y-%m-%d %H:%M')

			# Create a Final object with the course, date, and location
			final_to_add = {"sections" : str(sections[2]), "date" : date}


			if course in courses:
				added = 0
				for exam in courses[course]:
					if exam["date"] == date:
						exam["sections"] += ", " + str(sections[2])
						added = 1
						break
				if added == 0:
					courses[course].append(final_to_add)

			else:
				courses[course] = []
				courses[course].append(final_to_add)


# PRELIMS -- stores in prelims list
soup = BeautifulSoup(r_prelim.text, "html.parser")
lines = soup.prettify().split('\n')

for line in lines:
	if len(line) > 10:
		# If the line starts with an uppercase letter (for the course code)
		# AND the last character of the line is a digit (for the room number)
		if line[0].isupper() and line[-1].isdigit():

			# Split the line to get the course number
			sections = line.split(' ', 2)
			course = str(sections[0] + sections[1])

			# Split the line again to get the date and location
			sections =  sections[2].strip().split(' ', 1)
			date = str(sections[0].strip()).strip()

			if date[-4:] == time.strftime("%Y"):
				date = date + " 19:30"

				# Format the date to be in correct for MySQL
				dt = datetime.strptime(date, '%m/%d/%Y %H:%M')
				date = datetime.strftime(dt, '%Y-%m-%d %H:%M')
				# loc = sections[1].strip()

				# Create a Prelim object with the course, date, and location
				prelim_to_add = {"sections" : "000", "date" : date}

				if course in courses:
					courses[course].append(prelim_to_add)
				else:
					courses[course] = []
					courses[course].append(prelim_to_add)

# Open the connection to database
connection = mysql.connector.connect(user='samwise', password='3XJ73bgCS87mfvbe', host='samwisedata.ckbdcr0vghnq.us-east-1.rds.amazonaws.com')

# Add each exam time to the database
for key in courses:
	for exam in courses[key]:
		try:
			cursor = connection.cursor()
			query = "insert into samwisedb.exams(course, sections, time) values (\"" + key + "\", \"" + exam["sections"] + "\", \"" + exam["date"] +"\");"
			print(query)
			cursor.execute(query)
			connection.commit()
		finally:
			print ("DONE")
connection.close()
