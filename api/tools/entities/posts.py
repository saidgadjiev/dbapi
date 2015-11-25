from api.tools.entities import users, forums, threads
from api.tools import DBconnect
from api.tools.DBconnect import *


def create(date, thread, message, user, forum, optional):
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
    con = connect()
    #con.autocommit(False)
    with con:
        cursor = con.cursor()
        # try:
        con.begin()
        cursor.execute(update_thread_posts, (thread, ))
        cursor.execute(query, parameters)
        con.commit()
        # except Exception as e:
        #     con.rollback()
            # raise Exception("Database error: " + e.message)

        post_id = cursor.lastrowid
        #cursor.execute(update_parent, (parent, post_id, ))
        cursor.close()

    con.close()
    post = post_query(post_id)
    del post["dislikes"]
    del post["likes"]
    del post["parent"]
    del post["points"]
    return post


def details(details_id, related):
    post = post_query(details_id)
    if post is None:
        raise Exception("no post with id = " + details_id)

    if "user" in related:
        post["user"] = users.details(post["user"])
    if "forum" in related:
        post["forum"] = forums.details(short_name=post["forum"], related=[])
    if "thread" in related:
        post["thread"] = threads.details(id=post["thread"], related=[])

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


def posts_list(entity, params, identifier, related=[]):
    query = "SELECT date, dislikes, forum, id, isApproved, isDeleted, isEdited, isHighlighted, isSpam, likes, message, " \
            "parent, points, thread, user FROM post WHERE " + entity + " = %s "

    parameters = [identifier]
    if "since" in params:
        query += " AND date >= %s"
        parameters.append(params["since"])

    if "sort" in params:
        if params["sort"] == "flat":
            query += " ORDER BY date "
        elif params["sort"] == "tree":
            if params["order"] == "desc":
                query += " ORDER BY  SUBSTRING_INDEX(path, '.', 2) DESC, TRIM(LEADING SUBSTRING_INDEX(path, '.', 2) FROM path) "
            else:
                query += " ORDER BY path "
            if "limit" in params:
                query += " LIMIT " + str(params["limit"])
        else:
            bound_query = "SELECT SUBSTRING_INDEX(MIN(t.path), '.', 2) AS left_bound FROM "\
                "(SELECT path FROM post WHERE thread = %s AND parent IS NULL ORDER BY path " + params["order"] or ""
            if "limit" in params:
                bound_query += " LIMIT " + str(params["limit"])
            bound_query += ") AS t;"
            left = DBconnect.select_query(bound_query, (identifier, ))[0][0]
            bound_query = "SELECT MAX(t.path) AS left_bound FROM "\
                "(SELECT path FROM post WHERE thread = %s AND parent IS NULL ORDER BY path " + params["order"] or ""
            if "limit" in params:
                bound_query += " LIMIT " + str(params["limit"])
            bound_query += ") AS t;"
            right = DBconnect.select_query(bound_query, (identifier, ))[0][0]

            query += " AND SUBSTRING_INDEX(path, '.', 2) BETWEEN %s AND %s ORDER BY " + \
                params["order"] == "desc" and " SUBSTRING_INDEX(path, '.', 2) DESC, " \
                "TRIM(LEADING SUBSTRING_INDEX(path, '.', 2) FROM path) " or " path "
            parameters.append(left)
            parameters.append(right)
    else:
        if "order" in params:
            query += " ORDER BY date " + params["order"]
        else:
            query += " ORDER BY date DESC"
        if "limit" in params:
            query += " LIMIT " + str(params["limit"])

    post_ids = DBconnect.select_query(query=query, params=parameters)
    post_list = []

    if "sort" in params and params["sort"] != "flat":
        for post in post_ids:
            path = post[15].split('.')[1:]
            if len(path) == 1:
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
                    'childs': walk(post_ids, path[0], 2)
                }
                post_list.append(pf)
    else:
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
                pf["user"] = users.details(pf["user"])
            if "forum" in related:
                pf["forum"] = forums.details(short_name=pf["forum"], related=[])
            if "thread" in related:
                pf["thread"] = threads.details(id=pf["thread"], related=[])
            post_list.append(pf)
    return post_list


def remove_restore(post_id, status):
    DBconnect.update_query("UPDATE post SET isDeleted = %s WHERE post.id = %s", (status, post_id, ))
    return {
        "post": post_id
    }


def update(update_id, message):
    DBconnect.update_query('UPDATE post SET message = %s WHERE id = %s', (message, update_id, ))
    return details(details_id=update_id, related=[])


def vote(vote_id, vote_type):
    if vote_type == -1:
        DBconnect.update_query("UPDATE post SET dislikes=dislikes+1, points=points-1 where id = %s", (vote_id, ))
    else:
        DBconnect.update_query("UPDATE post SET likes=likes+1, points=points+1  where id = %s", (vote_id, ))
    return details(details_id=vote_id, related=[])


def post_query(id):
    post = DBconnect.select_query('select date, dislikes, forum, id, isApproved, isDeleted, isEdited, '
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
