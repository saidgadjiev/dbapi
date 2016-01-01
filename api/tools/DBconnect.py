__author__ = 'IS'
#encoding: utf8
import MySQLdb as db

def connect():
    try:
        return connect.conn
    except AttributeError:
        connect.conn = db.connect(host="localhost",
                	          user="root",
                        	  passwd="said",
                          	db="forumdb",
                          	charset="utf8")
        return connect.conn

def update_query(connect,query, params):
    try:
        cursor = connect.cursor()
        cursor.execute(query, params)
        inserted_id = cursor.lastrowid
        connect.commit()
        cursor.close()
    except db.Error:
        connect.rollback()
        cursor.close()
        return "Ituser"
    return inserted_id

def select_query(connect,query, params):
    try:
        cursor = connect.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        cursor.close()
    except db.Error:
        cursor.close()
	raise db.Error("Database error in usual query")
    return result

def select_query_dict(query,params):
    try:
        con = connect()
        cursor = con.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, params)
        result = cursor.fetchall()
        cursor.close()
    except db.Error:
        raise db.Error("Database error in dict query")
    return result

def execute(connect,query):
    try:
        cursor = connect.cursor()
        cursor.execute(query)
        connect.commit()
        cursor.close()
    except db.Error:
        connect.rollback()
	cursor.close()
    return
