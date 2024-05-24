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
    htmlCode = """
    <table border='1'>
    <tr>
    <th>title of the first column</th>
    <th>title of the second column</th></tr>"""

    # <table> flag for beginning of a table
    # <tr> flag for a row
    # <td> is a column
    # <th> is a header for the table
    # source : https://developer.mozilla.org/fr/docs/Web/HTML/Element/table

    for i in range(1, 5):
        # here we add a row with two column. first is just value of i, second is i²
        htmlCode += "<tr><td>item #" + str(i) + "</td><td>" + str(i * i) + "</td></tr>"
    htmlCode += "</table>"

    return htmlCode


app.run()
