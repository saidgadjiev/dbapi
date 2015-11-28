from api.tools.entities import users, posts, followers
from api.tools.DBconnect import *
from flask import Blueprint, request
from api.helpers import choose_required, intersection, get_json
import json

module = Blueprint('user', __name__, url_prefix='/db/api/user')


@module.route("/create/", methods=["POST"])
def create():
    con = connect()
    request_data = request.json
    required_data = ["email", "username", "name", "about"]
    optional = intersection(request=request_data, values=["isAnonymous"])
    try:
        choose_required(data=request_data, required=required_data)
        user = users.save_user(connect=con,email=request_data["email"], username=request_data["username"],
                               about=request_data["about"], name=request_data["name"], optional=optional)
    except Exception as e:
        if e.message == "5":
            con.close()           
            return json.dumps({"code": 5, "response": (e.message)})
        con.close()
        return json.dumps({"code": 1, "response": (e.message)})
    con.close()
    return json.dumps({"code": 0, "response": user})


@module.route("/details/", methods=["GET"])
def details():
    con = connect()
    request_data = get_json(request)
    required_data = ["user"]
    try:
        choose_required(data=request_data, required=required_data)
        user_details = users.details(connect=con,email=request_data["user"])
    except Exception as e:
        con.close()
        return json.dumps({"code": 1, "response": (e.message)})
    con.close()
    return json.dumps({"code": 0, "response": user_details})


@module.route("/follow/", methods=["POST"])
def follow():
    con = connect()
    request_data = request.json
    required_data = ["follower", "followee"]
    try:
        choose_required(data=request_data, required=required_data)
        following = followers.add_follow(connect=con,email1=request_data["follower"], email2=request_data["followee"])
    except Exception as e:
        con.close()
        return json.dumps({"code": 1, "response": (e.message)})
    con.close()
    return json.dumps({"code": 0, "response": following})


@module.route("/unfollow/", methods=["POST"])
def unfollow():
    con = connect()
    request_data = request.json
    required_data = ["follower", "followee"]
    try:
        choose_required(data=request_data, required=required_data)
        following = followers.remove_follow(connect=con,email1=request_data["follower"], email2=request_data["followee"])
    except Exception as e:
        con.close()
        return json.dumps({"code": 1, "response": (e.message)})
    con.close()
    return json.dumps({"code": 0, "response": following})


@module.route("/listFollowers/", methods=["GET"])
def list_followers():
    con = connect()
    request_data = get_json(request)
    required_data = ["user"]
    followers_param = intersection(request=request_data, values=["limit", "order", "since_id"])
    try:
        choose_required(data=request_data, required=required_data)
        follower_l = followers.followers_list(connect=con,email=request_data["user"], type="follower", params=followers_param)
    except Exception as e:
        con.close()
        return json.dumps({"code": 1, "response": (e.message)})
    con.close()
    return json.dumps({"code": 0, "response": follower_l})


@module.route("/listFollowing/", methods=["GET"])
def list_following():
    con = connect()
    request_data = get_json(request)
    required_data = ["user"]
    followers_param = intersection(request=request_data, values=["limit", "order", "since_id"])
    try:
        choose_required(data=request_data, required=required_data)
        followings = followers.followers_list(connect = con,email=request_data["user"], type="followee", params=followers_param)
    except Exception as e:
        return json.dumps({"code": 1, "response": (e.message)})
    return json.dumps({"code": 0, "response": followings})


@module.route("/listPosts/", methods=["GET"])
def list_posts():
    con = connect()
    request_data = get_json(request)
    required_data = ["user"]
    optional = intersection(request=request_data, values=["limit", "order", "since"])
    try:
        choose_required(data=request_data, required=required_data)
        posts_l = posts.posts_list(connect=con,entity="user", params=optional, identifier=request_data["user"], related=[])
    except Exception as e:
        con.close()
        return json.dumps({"code": 1, "response": (e.message)})
    con.close()
    return json.dumps({"code": 0, "response": posts_l})


@module.route("/updateProfile/", methods=["POST"])
def update():
    con = connect()
    request_data = request.json
    required_data = ["user", "name", "about"]
    try:
        choose_required(data=request_data, required=required_data)
        user = users.update_user(connect=con,email=request_data["user"], name=request_data["name"], about=request_data["about"])
    except Exception as e:
        con.close()
        return json.dumps({"code": 1, "response": (e.message)})
    con.close()
    return json.dumps({"code": 0, "response": user})
