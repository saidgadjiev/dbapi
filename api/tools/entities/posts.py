from api.tools.entities import users, forums, threads
from api.tools import DBconnect
from api.tools.DBconnect import *
from api.tools import DBconnect

def create(connect,date, thread, message, user, forum, optional):
    try:
        query = "INSERT INTO post (message, user, forum, thread, date"
        values = "(%s, %s, %s, %s, %s"
        parameters = [message, user, forum, thread, date]

        for param in optional:
            query += ", " + param
            values += ", %s"
            parameters.append(optional[param])
    except Exception as e:
        print e.message
    query += ") VALUES " + values + ")"
    update_thread_posts = "UPDATE thread SET posts = posts + 1 WHERE id = %s"
    update_parent = "UPDATE post SET parent =  %s WHERE id = %s"
    con = connect
    with con:
        cursor = con.cursor()
        cursor.execute(update_thread_posts, (thread, ))
        cursor.execute(query, parameters)
        con.commit()
        post_id = cursor.lastrowid
        cursor.close()

    post = post_query(connect,post_id)
    del post["dislikes"]
    del post["likes"]
    del post["parent"]
    del post["points"]
    return post


def details(connect,details_id, related):
    post = post_query(connect,details_id)
    if post is None:
        raise Exception("no post with id = " + details_id)

    if "user" in related:
        post["user"] = users.details(connect,post["user"])
    if "forum" in related:
        post["forum"] = forums.details(connect=connect,short_name=post["forum"], related=[])
    if "thread" in related:
        post["thread"] = threads.details(connect=connect,id=post["thread"], related=[])

    return post


def walk(array, id, level):
    list = []
    for post in array:
        if str(post[11]) == id:
            path = post[15].split('.')[level:]
            pf = {
                'date': str(post[0]),
                'dislikes': post[1],
                'forum': post[2],
                'id': post[3],
                'isApproved': bool(post[4]),
                'isDeleted': bool(post[5]),
                'isEdited': bool(post[6]),
                'isHighlighted': bool(post[7]),
                'isSpam': bool(post[8]),
                'likes': post[9],
                'message': post[10],
                'parent': post[11],
                'points': post[12],
                'thread': post[13],
                'user': post[14],
                'childs': walk(array, path[0], level + 1)
            }
            list.append(pf)
    return list


def posts_list(connect, entity, params, identifier, related=[]):
    query = "SELECT date, dislikes, forum, id, isApproved, isDeleted, isEdited, isHighlighted, isSpam, likes, message, " \
            "parent, points, thread, user FROM post WHERE " + entity + " = %s "

    parameters = [identifier]
    if "since" in params:
        query += " AND date >= %s"
        parameters.append(params["since"])

    query += " ORDER BY date " + params["order"]

    if "limit" in params:
        query += " LIMIT " + str(params["limit"])

    post_ids = DBconnect.select_query(connect=connect,query=query, params=parameters)
    post_list = []
    for post in post_ids:
        pf = {
                'date': str(post[0]),
                'dislikes': post[1],
                'forum': post[2],
                'id': post[3],
                'isApproved': bool(post[4]),
                'isDeleted': bool(post[5]),
                'isEdited': bool(post[6]),
                'isHighlighted': bool(post[7]),
                'isSpam': bool(post[8]),
                'likes': post[9],
                'message': post[10],
                'parent': post[11],
                'points': post[12],
                'thread': post[13],
                'user': post[14],
            }
        if "user" in related:
            pf["user"] = users.details(connect,pf["user"])
        if "forum" in related:
            pf["forum"] = forums.details(connect,short_name=pf["forum"], related=[])
        if "thread" in related:
            pf["thread"] = threads.details(connect,id=pf["thread"], related=[])
        post_list.append(pf)
    return post_list


def remove_restore(connect,post_id, status):
    DBconnect.update_query(connect,"UPDATE post SET isDeleted = %s WHERE post.id = %s", (status, post_id, ))
    return {
        "post": post_id
    }


def update(connect,update_id, message):
    DBconnect.update_query(connect,'UPDATE post SET message = %s WHERE id = %s', (message, update_id, ))
    return details(connect,details_id=update_id, related=[])


def vote(connect,vote_id, vote_type):
    if vote_type == -1:
        DBconnect.update_query(connect,"UPDATE post SET dislikes=dislikes+1, points=points-1 where id = %s", (vote_id, ))
    else:
        DBconnect.update_query(connect,"UPDATE post SET likes=likes+1, points=points+1  where id = %s", (vote_id, ))
    return details(connect,details_id=vote_id, related=[])


def post_query(connect,id):
    post = DBconnect.select_query(connect,'select date, dislikes, forum, id, isApproved, isDeleted, isEdited, '
                       'isHighlighted, isSpam, likes, message, parent, points, thread, user '
                       'FROM post WHERE id = %s LIMIT 1;', (id, ))
    if len(post) == 0:
        return None
    return post_formated(post)


def post_formated(post):
    post = post[0]
    post_response = {
        'date': str(post[0]),
        'dislikes': post[1],
        'forum': post[2],
        'id': post[3],
        'isApproved': bool(post[4]),
        'isDeleted': bool(post[5]),
        'isEdited': bool(post[6]),
        'isHighlighted': bool(post[7]),
        'isSpam': bool(post[8]),
        'likes': post[9],
        'message': post[10],
        'parent': post[11],
        'points': post[12],
        'thread': post[13],
        'user': post[14],

    }
    return post_response
