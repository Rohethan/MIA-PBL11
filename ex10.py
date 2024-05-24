from flask_mysqldb import MySQL
from sshtunnel import SSHTunnelForwarder
from flask import Flask, request

# Starting ssh tunnel for this exos's remote DB
tunnel = SSHTunnelForwarder(
    ("op-dev.icam.fr", 22),
    ssh_username="MIAPBL11-STUDENT",
    ssh_password="sei4B",
    remote_bind_address=("127.0.0.1", 3306),
)
tunnel.start()

app = Flask("MIA PBL11")

app.config['MYSQL_HOST'] = '127.0.0.1'

app.config['MYSQL_USER'] = 'MIAPBL11-STUDENT'
app.config['MYSQL_PASSWORD'] = 'sei4B'
app.config['MYSQL_DB'] = 'MIAPBL11-STUDENT'
app.config['MYSQL_PORT'] = tunnel.local_bind_port
mysql = MySQL(app)


@app.route('/')
def index():
    #htmlCode is some text
    htmlCode = "Hello Icam =)"
    htmlCode += "<br>"
    htmlCode += "<a href='/'>Homepage</a>"
    htmlCode += "<br>"
    htmlCode += "<a href='/list'>List</a>"
    htmlCode += "<br>"
    htmlCode += "<a href='/add'>Add</a>"
    htmlCode += "<br>"
    #this text is returned
    return htmlCode


@app.route("/list")
def list():
    # you must create a Cursor object
    # it will let you execute the needed query
    cur = mysql.connection.cursor()

    cur.execute(
        "SELECT MobilityWish.studentMail, Campus.campusName FROM MobilityWish LEFT JOIN Campus ON MobilityWish.Campus_idCampus = Campus.idCampus")
    # that sql query join in campus name based in the campus ids
    mysql.connection.commit()  # Chose the latest; has more data
    htmlCode = """
    Menu<br>
    <a href='/'>Homepage</a><br>
    <a href='/list'>List</a><br>
    <a href='/add'>Add</a><br>
    <table border='1'>
    <tr>
    <th>Student's mail</th>
    <th>Campus choice</th></tr>"""  # again, start a html str to send later

    # print the first cell (or column) of all rows (or records)
    for row in cur.fetchall():
        htmlCode += "<tr><td>" + str(row[0]) + "</td><td>" + str(row[1]) + "</td></tr>"

    htmlCode += "</table>"
    cur.close()
    return htmlCode


@app.route('/add')
def add():
    htmlCode = """
        Menu<br>
        <a href='/'>Homepage</a><br>
        <a href='/list'>List</a><br>
        <a href='/add'>Add</a><br>
        <br>Make a wish<br>
        <form action='addsave' method='GET'>
        <label>Email Address:</label><br>
        <input type='email' name='student' required><br>
        <label>Campus choice:</label><br>
        <select name='choice'>"""

    # you must create a Cursor object
    # it will let you execute the needed query
    cur = mysql.connection.cursor()

    # we look for all campuses
    cur.execute("SELECT * FROM Campus")
    mysql.connection.commit()

    # print the first cell (or column) of all rows (or records)
    for row in cur.fetchall():
        # for each campus, we create an <option value=id>name</option>
        htmlCode += "<option value=" + str(row[0]) + ">"
        htmlCode += str(row[1])
        htmlCode += "</option>"

    # we close the form
    htmlCode += "</select><br><input type='submit' value='Save'></form>"
    return htmlCode


@app.route('/addsave', methods=['GET'])
def addsave():
    htmlCode = """
    Menu<br>
    <a href='/'>Homepage</a><br>
    <a href='/list'>List</a><br>
    <a href='/add'>Add</a><br>"""
    # you must create a Cursor object
    # it will let you execute the needed query
    cur = mysql.connection.cursor()

    # MobilityWish is the table
    # Campus_idCampus and studentMail are the fields in the table
    # SQL syntax is INSERT INTO table(field1, field2) VALUES('value1', 'value2')
    sql = "INSERT INTO MobilityWish(studentMail, Campus_idCampus) VALUES (%s, %s)"
    # request.values['choice'] and request.values['student'] are input from the form by user
    val = (request.values['student'], request.values['choice'])
    # we execute an insert query
    cur.execute(sql, val)

    # commit = save changes in database
    mysql.connection.commit()

    # display the number of records added
    htmlCode += str(cur.rowcount) + " record inserted."
    return htmlCode


app.run()
