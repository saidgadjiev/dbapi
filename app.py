__author__ = 'IS'

from flask import Flask, request
from api.tools.entities.clear import clear as clear_db
from api.tools.entities.status import status as status_db
from werkzeug.contrib.fixers import ProxyFix
import json
app = Flask(__name__)

#app.config['DEBUG'] = True
#app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

from api.thread import module as thread
from api.user import module as user
from api.forum import module as forum
from api.post import module as post

app.register_blueprint(user)
app.register_blueprint(forum)
app.register_blueprint(thread)
app.register_blueprint(post)


#@app.before_request
#def before_request():
#    print request.endpoint


@app.route('/db/api/clear/', methods=['POST'])
def clear():
	clear_db()
	return json.dumps({"code" : 0, "response" : "OK" })

@app.route('/db/api/status/', methods=['GET'])
def status():
	stat = status_db()
	return json.dumps({"code" : 0, "response" : stat })


#app.wsgi_app=ProxyFix(app.wsgi_app)

if __name__ == '__main__':
    app.run(host='localhost',port=4242)
