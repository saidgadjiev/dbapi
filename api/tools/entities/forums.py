__author__ = 'IS'

from api.tools import DBconnect
from api.tools.entities import users
import MySQLdb
from api import common


def save_forum(connect,name, short_name, user):
    DBconnect.update_query(connect,'INSERT INTO forum (name, short_name, user) VALUES (%s, %s, %s)',
                               (name, short_name, user, ))
    forum = DBconnect.select_query(connect,
            'select id, name, short_name, user FROM forum WHERE short_name = %s', (short_name, )
        )
    return forum_description(forum)


def forum_description(forum):
    forum = forum[0]
    response = {
        'id': forum[0],
        'name': forum[1],
        'short_name': forum[2],
        'user': forum[3]
    }
    return response


def details(connect,short_name, related):
    forum = DBconnect.select_query(connect,
        'select id, name, short_name, user FROM forum WHERE short_name = %s LIMIT 1;', (short_name, )
    )
    if len(forum) == 0:
        raise ("No forum with exists short_name=" + short_name)
    forum = forum_description(forum)

    if "user" in related:
        forum["user"] = users.details(connect,forum["user"])
    return forum


def list_users(connect,short_name, optional):
    query = "SELECT user.id, user.email, user.name, user.username, user.isAnonymous, user.about FROM user " \
        "WHERE user.email IN (SELECT DISTINCT user FROM post WHERE forum = %s)"
    if "since_id" in optional:
        query += " AND user.id >= " + str(optional["since_id"])
    if "order" in optional:
        query += " ORDER BY user.name " + optional["order"]
    if "limit" in optional:
        query += " LIMIT " + str(optional["limit"])
 
    cursor = connect.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(query, (short_name, ))
    users_tuple = [i for i in cursor.fetchall()]

    for user_sql in users_tuple:
        cursor.execute("""SELECT `thread` FROM `subscription` WHERE `user` = %s;""", (user_sql['email'], ))
        sub = [i['thread'] for i in cursor.fetchall()]

        followers = common.list_followers(cursor, user_sql['email'])
        following = common.list_following(cursor, user_sql['email'])

        user_sql.update({'following': following, 'followers': followers, 'subscriptions': sub})
    cursor.close()
    return users_tuple
