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
