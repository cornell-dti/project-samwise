@app.route('/cal/<userid>/<course>')
def addCourse(userid, course):
    if 'netid' in session:
        connection = mysql.connector.connect(user='samwise', password='3XJ73bgCS87mfvbe', host='samwisedata.ckbdcr0vghnq.us-east-1.rds.amazonaws.com')

        try:
            cursor = connection.cursor()
            query = "insert into samwisedb.User(netId, courseId) values (\"" + userid + "\", \"" + course + "\");"
            print(query)
            cursor.execute(query)
            connection.commit()
        finally:
            print ("DONE")
            connection.close()
    return redirect(url_for('index'))

@app.route('/addSubtask/', methods=['POST'])
def addSubtask():
    data = request.get_json(force=True)
    project_id = data['id']
    subtask = data['subtask']
    connection = mysql.connector.connect(user='samwise', password='3XJ73bgCS87mfvbe',
                                         host='samwisedata.ckbdcr0vghnq.us-east-1.rds.amazonaws.com')
    try:
        cursor = connection.cursor()
        query = "insert into samwisedb.subtasks(id, subtask) values (\"" + str(project_id) + "\", \"" + subtask + "\");"
        print(query)
        cursor.execute(query)
        subtask_id = cursor.lastrowid
        connection.commit()
    finally:
        print ("DONE")
        connection.close()
    return json.dumps([subtask_id])

@app.route('/removeSubtask/', methods=['POST'])
def removeSubtask():
    data = request.get_json(force=True)
    subtask_name = data['subtask']
    connection = mysql.connector.connect(user='samwise', password='3XJ73bgCS87mfvbe',
                                         host='samwisedata.ckbdcr0vghnq.us-east-1.rds.amazonaws.com')
    try:
        cursor = connection.cursor()
        query = "DELETE FROM samwisedb.subtasks WHERE subtask=%s" % subtask_name
        print(query)
        cursor.execute(query)
        connection.commit()
    finally:
        print ("DONE")
        connection.close()
    return json.dumps([subtask_name])

@app.route('/updateSubtask/', methods=['POST'])
def updateSubtask():
    data = request.get_json(force=True)
    subtask_id = data['id']
    subtask_name = data['subtask']
    connection = mysql.connector.connect(user='samwise', password='3XJ73bgCS87mfvbe',
                                         host='samwisedata.ckbdcr0vghnq.us-east-1.rds.amazonaws.com')
    try:
        cursor = connection.cursor()
        query = "UPDATE samwisedb.subtasks SET subtask=%s WHERE id = %s" % (subtask_name, subtask_id)
        print(query)
        cursor.execute(query)
        connection.commit()
    finally:
        print ("DONE")
        connection.close()
    return json.dumps([subtask_name])
