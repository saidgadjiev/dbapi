__author__ = 'IS'

from api.tools import DBconnect


def save_user(email, username, about, name, optional):
    isAnonymous = 0
    if "isAnonymous" in optional:
        isAnonymous = optional["isAnonymous"]
    try:
        DBconnect.update_query(
                'INSERT INTO user (email, about, name, username, isAnonymous) VALUES (%s, %s, %s, %s, %s)',
                (email, about, name, username, isAnonymous, ))
        user = DBconnect.select_query('select email, about, isAnonymous, id, name, username FROM user WHERE email = %s',
                           (email, ))
    except Exception as e:
        raise Exception(e.message)

    return user_format(user)


def update_user(email, about, name):
    DBconnect.update_query('UPDATE user SET email = %s, about = %s, name = %s WHERE email = %s',
                           (email, about, name, email, ))
    return details(email)


def followers(email, type):
    where = "followee"
    if type == "followee":
        where = "follower"
    f_list = DBconnect.select_query(
        "SELECT " + type + " FROM follower WHERE " + where + " = %s ", (email, )
    )
    return tuple2list(f_list)


def details(email):
    user = DBconnect.select_query('select email, about, isAnonymous, id, name, username FROM user WHERE email = %s LIMIT 1;', (email, ))
    user = user_format(user)
    if user is None:
        raise Exception("No user with email " + email)
    f_list = DBconnect.select_query(
        "SELECT follower FROM follower WHERE followee = %s ", (email, )
    )
    user["followers"] = tuple2list(f_list)
    f_list = DBconnect.select_query(
        "SELECT followee FROM follower WHERE follower = %s ", (email, )
    )
    user["following"] = tuple2list(f_list)
    user["subscriptions"] = user_subscriptions(email)
    return user


def user_subscriptions(email):
    s_list = []
    subscriptions = DBconnect.select_query('select thread FROM subscription WHERE user = %s', (email, ))
    for el in subscriptions:
        s_list.append(el[0])
    return s_list


def user_format(user):
    user = user[0]
    user_response = {
        'about': user[1],
        'email': user[0],
        'id': user[3],
        'isAnonymous': bool(user[2]),
        'name': user[4],
        'username': user[5]
    }
    return user_response


def tuple2list(t):
    l = []
    for el in t:
        l.append(el[0])
    return l
