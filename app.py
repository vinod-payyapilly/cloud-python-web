from flask import Flask,request
from redis import Redis
import socket
from datetime import datetime
import json
hostname = socket.gethostname()

app = Flask(__name__)
redis = Redis(host='redis', port=6379)

@app.route('/')
def hello():
    redis.incr('hits')
    counter = str(redis.get('hits'),'utf-8')
    
    # Remote IP
    remote_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    # Save Remote IP to redis
    client_access_entry = {"ip": remote_ip, "access_date":datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}
    redis.lpush("CLIENT_ACCESS_LIST", json.dumps(client_access_entry) )

    flask_response = f"Host:{hostname} - This webpage has been viewed "+counter+" time(s)"
    flask_response += """<br/>Thank you for visiting"""
    return flask_response
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
