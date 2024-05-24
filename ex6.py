from flask_mysqldb import MySQL
from sshtunnel import SSHTunnelForwarder
from flask import Flask


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


@app.route("/")
def index():
    # you must create a Cursor object
    # it will let you execute the needed query
    cur = mysql.connection.cursor()


    cur.execute("SELECT MobilityWish.studentMail, Campus.campusName FROM MobilityWish LEFT JOIN Campus ON MobilityWish.Campus_idCampus = Campus.idCampus")
    # that sql query join in campus name based in the campus ids
    mysql.connection.commit() # Chose the latest; has more data
    htmlCode = """
        <table border='1'>
        <tr>
        <th>Student's mail</th>
        <th>Campus choice</th></tr>""" # again, start a html str to send later

    # print the first cell (or column) of all rows (or records)
    for row in cur.fetchall():
        htmlCode += "<tr><td>"+str(row[0])+"</td><td>"+str(row[1])+"</td></tr>"

    htmlCode += "</table>"
    cur.close()
    return htmlCode


app.run()
