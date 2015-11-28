__author__ = 'IS'

from api.tools import DBconnect


def save_user(connect,email, username, about, name, optional):
    isAnonymous = 0
    if "isAnonymous" in optional:
        isAnonymous = optional["isAnonymous"]
    
    str = DBconnect.update_query(connect,
                'INSERT INTO user (email, about, name, username, isAnonymous) VALUES (%s, %s, %s, %s, %s)',
                (email, about, name, username, isAnonymous, ))
    if str == "Ituser":
        raise Exception("5")
    user = DBconnect.select_query(connect,'select email, about, isAnonymous, id, name, username FROM user WHERE email = %s',
                           (email, ))

    return user_format(user)


def update_user(connect,email, about, name):
    DBconnect.update_query(connect,'UPDATE user SET email = %s, about = %s, name = %s WHERE email = %s',
                           (email, about, name, email, ))
    return details(connect,email)


def followers(connect,email, type):
    where = "followee"
    if type == "followee":
        where = "follower"
    f_list = DBconnect.select_query(connect,
        "SELECT " + type + " FROM follower WHERE " + where + " = %s ", (email, )
    )
    return tuple2list(f_list)


def details(connect,email):
    user = DBconnect.select_query(connect,'select email, about, isAnonymous, id, name, username FROM user WHERE email = %s LIMIT 1;', (email, ))
    user = user_format(user)
    if user is None:
        raise Exception("No user with email " + email)
    f_list = DBconnect.select_query(connect,
        "SELECT follower FROM follower WHERE followee = %s ", (email, )
    )
    user["followers"] = tuple2list(f_list)
    f_list = DBconnect.select_query(connect,
        "SELECT followee FROM follower WHERE follower = %s ", (email, )
    )
    user["following"] = tuple2list(f_list)
    user["subscriptions"] = user_subscriptions(connect,email)
    return user


def user_subscriptions(connect,email):
    s_list = []
    subscriptions = DBconnect.select_query(connect,'select thread FROM subscription WHERE user = %s', (email, ))
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
