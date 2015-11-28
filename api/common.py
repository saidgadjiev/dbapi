def list_following(cursor, user_id):
    cursor.execute("""SELECT followee FROM follower WHERE follower = %s;""", (user_id, ))
    following = [i['followee'] for i in cursor.fetchall()]

    return following


def list_followers(cursor, user_id):
    cursor.execute("""SELECT follower FROM follower WHERE followee = %s;""", (user_id, ))
    followers = [i['follower'] for i in cursor.fetchall()]

    return followers
