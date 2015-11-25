__author__ = 'IS'
from api.tools import DBconnect

def status():

	resp = [];
	tables = ['user', 'thread', 'forum', 'post'];
	for table in tables:
		currCount = len(DBconnect.select_query('SELECT id FROM ' + table, ()))
		resp.append(currCount)
	statusResponse = {
		'user'   : resp[0],
		'thread' : resp[1],
		'forum'  : resp[2],
		'post'   : resp[3]
	}
	return statusResponse
