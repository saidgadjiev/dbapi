__author__ = 'IS'
from api.tools.DBconnect import *
from api.tools import DBconnect

def clear():
    con = connect()
    tables = ['post', 'thread', 'forum', 'subscription', 'follower', 'user']
    DBconnect.execute(con,"SET global foreign_key_checks = 0;")
    for table in tables:
        DBconnect.execute(con,"TRUNCATE TABLE %s;" % table)
    DBconnect.execute(con,"SET global foreign_key_checks = 1;")
    con.close()
    return
