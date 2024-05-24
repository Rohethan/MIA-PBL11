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
    htmlCode = "<ol>" # again, start a html str to send later

    # print the first cell (or column) of all rows (or records)
    for row in cur.fetchall():
        htmlCode += "<li>"+str(row[0])+" "+str(row[1])+"</li>" #appends the 2nd index of the every query results, it in a loop, with a html list element

    htmlCode += "</ol>"
    cur.close()
    return htmlCode


app.run()
