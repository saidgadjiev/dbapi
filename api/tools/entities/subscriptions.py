__author__ = 'IS'

from api.tools import DBconnect


"""
Helper class to manipulate with subscriptions.
"""


def save_subscription(connect,email, thread_id):
   
    DBconnect.update_query(connect,'INSERT INTO subscription (thread, user) VALUES (%s, %s)', (thread_id, email, ))
    subscription = DBconnect.select_query(connect,
        'select thread, user FROM subscription WHERE user = %s AND thread = %s', (email, thread_id, )
    )
    response = {
        "thread": subscription[0][0],
        "user": subscription[0][1]
    }
    return response


def remove_subscription(connect,email, thread_id):
    try:    
        DBconnect.update_query(connect,'DELETE FROM subscription WHERE user = %s AND thread = %s', (email, thread_id, ))
    except Exception as e:
        raise Exception("user " + email + " does not subscribe thread #" + str(thread_id))
    response = {
        "thread": subscription[0][0],
        "user": subscription[0][1]
    }
    return response
