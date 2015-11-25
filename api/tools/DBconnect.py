__author__ = 'IS'
#encoding: utf8
import MySQLdb as db

def connect():
	try:
		con = db.connect(host="127.0.0.1",
                	          user="root",
                        	  passwd="said1995",
                          	db="forumdb",
                          	charset="utf8")
	except db.Error:
		raise db.Error("Error connection")
	return con

# Execute update query
def update_query(query, params):
    try:
        con = connect()
        cursor = con.cursor()
        cursor.execute(query, params)
        inserted_id = cursor.lastrowid
        con.commit()
        cursor.close()
        con.close()
    except db.Error:
        con.rollback()
        cursor.close()
        con.close()
        raise Exception("5")
    return inserted_id


# Execute query
# Returns tuple!
def select_query(query, params):
    try:
        con = connect()
        cursor = con.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        cursor.close()
        con.close()
    except db.Error:
        raise db.Error("Database error in usual query")
    return result

def select_query_dict(query,params):
    try:
        con = connect()
        cursor = con.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, params)
        result = cursor.fetchall()
        cursor.close()
        con.close()
    except db.Error:
        raise db.Error("Database error in dict query")
    return result

# Check if something exists
def exist(entity, identifier, value):
    if not len(select_query('SELECT  id FROM ' + entity + ' WHERE ' + identifier + '=%s', (value, ))):
        raise Exception("No such element in " + entity + " with " + identifier + "=" + str(value))
    return


def execute(query):
    con = connect()
    cursor = con.cursor()
    cursor.execute(query)
    con.commit()
    cursor.close()
    con.close()
    # except db.Error:
    #     raise db.Error("Database error in update query.")
    return
