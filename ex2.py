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
    generated_html = "<ul>" #we create a string that we will send later to the browser
    for i in range(1, 5):
        generated_html += "<li>item #" + str(i) + "</li>" #here, in a loop, add an item to a list with python generated value
    generated_html += "</ul>" #finish it for happy html
    return generated_html #return our string to send it



app.run()
