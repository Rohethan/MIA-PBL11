from sshtunnel import SSHTunnelForwarder
from flask import Flask

'''
# Starting ssh tunnel for this exos's remote DB
tunnel = SSHTunnelForwarder(
    ("op-dev.icam.fr", 22),
    ssh_username="MIAPBL11-STUDENT",
    ssh_password="sei4B",
    remote_bind_address=("127.0.0.1", 3306),
)
tunnel.start()
'''

app = Flask("MIA PBL11")

@app.route("/")
def index():
    return "Salut."


app.run()
