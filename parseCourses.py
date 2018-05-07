from collections import namedtuple
from datetime import datetime
import requests
import time
import urllib
import urllib2
import simplejson
import psycopg2
import urllib
from collections import defaultdict
import gc
import os

from course import CourseParserJson


# Check to see what month it is
month = time.strftime("%m")
year = time.strftime("%Y")[2:]
semester = "SP"
# If it is later than June, search for the fall exams, otherweise search for spring exams
if (int(month) > 6):
    semester = "FA"
roster_slug = semester + year
api_call_time = 0
API_CALL_COOLDOWN = 0.8

def make_api_call(endpoint, args=None):
    global api_call_time
    # Rate limiting
    new_time = time.time()
    if new_time - api_call_time < API_CALL_COOLDOWN:
        time.sleep(API_CALL_COOLDOWN - (new_time - api_call_time))
    api_call_time = new_time

    url = 'https://classes.cornell.edu/api/2.0/' + endpoint
    if args is not None:
        url += '?'
        url += urllib.urlencode(args)

    retry = 3
    result = None
    while retry > 0:
        retry -= 1
        try:
            result = simplejson.load(urllib2.urlopen(url))
            break
        except Exception as e:
            print('Error: %s, retrying...' % e)

    if result is None:
        raise APIError('Cannot call API after retrying')

    if result['status'] != 'success':
        raise APIError('Error (%s): %s' % (result['status'], str(result['message'])))
    else:
        return result['data']

def get_db():
    return psycopg2.connect(dbname=os.getenv('SAMWISE_DBNAME'), host=os.getenv('SAMWISE_DB'), user=os.getenv('SAMWISE_USERNAME'), password=os.getenv('SAMWISE_PASSWORD'), sslmode='require')



def update_term(term):
    global course_id_max

    print('Reading subject list...')

    raw_data = {}

    # subjectlist
    subjects = []

    raw_data_subjects = make_api_call('config/subjects.json', {'roster': term})
    for node in raw_data_subjects['subjects']:
        subjects.append({
            'sub' : node.get('value'),
            'desc' : node.get('descrformal')
        })

    subjects.sort(key=lambda x: x['sub'])

    course_parser = CourseParserJson()

    for subj in subjects:
        sub = subj['sub']

        raw_data_subj = make_api_call('search/classes.json', {'roster': term, 'subject': sub})

        for cls in raw_data_subj['classes']:
            course_parser.parse(cls)

        print('Done.')
        # break # test: only one subject

        gc.collect()

    courses = course_parser.courses

    course_by_number = defaultdict(list)
    for course in courses:
        course_by_number[course['sub'] + str(course['nbr'])].append(course)
        #print course
        #print course['sub'] + str(course['nbr'])


    # Open connection to the database
    connection = get_db()

    for c_key, c_val in course_by_number.iteritems():
        for s_key, s_val in c_val[0]['secs'].iteritems():
            # print s_val
            try:
                setting = s_val[0]['mt'][0]
                try:
                    cursor = connection.cursor()
                    query = "insert into Course(courseId) values (" + c_key + ");"
                    print query
                    cursor.execute(query)
                    connection.commit()
                finally:
                    print "DONE"
            except Exception, e:
                print dir(e)

    connection.close()

if __name__ == "__main__":
  update_term(roster_slug)
