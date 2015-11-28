from api.tools.entities import users

__author__ = 'IS'

from api.tools import DBconnect

"""
Helper class to manipulate with users.
"""


def add_follow(connect,email1, email2):
    DBconnect.update_query(connect,'INSERT INTO follower (follower, followee) VALUES (%s, %s)', (email1, email2, ))
    user = users.details(connect,email1)
    return user


def remove_follow(connect,email1, email2):
    DBconnect.update_query(connect,'DELETE FROM follower WHERE follower = %s AND followee = %s', (email1, email2, ))
    return users.details(connect,email1)


def followers_list(connect,email, type, params):
    if type == "follower":
        where = "followee"
    if type == "followee":
        where = "follower"

    query = "SELECT " + type + " FROM follower JOIN user ON user.email = follower." + type + \
            " WHERE " + where + " = %s "

    if "since_id" in params:
        query += " AND user.id >= " + str(params["since_id"])
    if "order" in params:
        query += " ORDER BY user.name " + params["order"]
    else:
        query += " ORDER BY user.name DESC "
    if "limit" in params:
        query += " LIMIT " + str(params["limit"])

    followers_ids_tuple = DBconnect.select_query(connect=connect,query=query, params=(email, ))

    f_list = []
    for id in followers_ids_tuple:
        id = id[0]
        f_list.append(users.details(connect=connect,email=id))

    return f_list
