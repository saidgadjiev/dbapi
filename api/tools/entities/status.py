__author__ = 'IS'
from api.tools.DBconnect import *
from api.tools import DBconnect

def status():
        con = connect()
	resp = [];
	tables = ['user', 'thread', 'forum', 'post'];
	for table in tables:
		currCount = len(DBconnect.select_query(con,'SELECT id FROM ' + table, ()))
		resp.append(currCount)
	statusResponse = {
		'user'   : resp[0],
		'thread' : resp[1],
		'forum'  : resp[2],
		'post'   : resp[3]
	}
	return statusResponse
