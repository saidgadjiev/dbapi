from api.tools.entities import posts, threads
from flask import Blueprint, request
import json
from api.helpers import choose_required, intersection, related_exists, get_json
from api.tools.DBconnect import *

module = Blueprint('post', __name__, url_prefix='/db/api/post')

@module.route("/create/", methods=["POST"])
def create():
    con = connect()
    content = request.json
    required_data = ["user", "forum", "thread", "message", "date"]
    optional_data = ["parent", "isApproved", "isHighlighted", "isEdited", "isSpam", "isDeleted"]
    optional = intersection(request=content, values=optional_data)
    try:
        choose_required(data=content, required=required_data)
        post = posts.create(connect=con,date=content["date"], thread=content["thread"],
                        message=content["message"], user=content["user"],
                        forum=content["forum"], optional=optional)
    except Exception as e:
        return json.dumps({"code": 1, "response": (e.message)})
    return json.dumps({"code": 0, "response": post})


@module.route("/details/", methods=["GET"])
def details():
    con = connect()
    content = get_json(request)
    required_data = ["post"]
    related = related_exists(content)
    try:
        choose_required(data=content, required=required_data)
        post = posts.details(con,content["post"], related=related)
    except Exception as e:
        return json.dumps({"code": 1, "response": (e.message)})
    return json.dumps({"code": 0, "response": post})


@module.route("/list/", methods=["GET"])
def post_list():
    con = connect()
    content = get_json(request)
    try:
        identifier = content["forum"]
        entity = "forum"
    except KeyError:
        try:
            identifier = content["thread"]
            entity = "thread"
        except Exception as e:
            return json.dumps({"code": 1, "response": (e.message)})

    optional = intersection(request=content, values=["limit", "order", "since"])
    try:
        p_list = posts.posts_list(connect=con,entity=entity, params=optional, identifier=identifier, related=[])
    except Exception as e:
        return json.dumps({"code": 1, "response": (e.message)})
    return json.dumps({"code": 0, "response": p_list})


@module.route("/remove/", methods=["POST"])
def remove():
    con = connect()
    content = get_json(request)
    required_data = ["post"]
    try:
        choose_required(data=content, required=required_data)
        post = posts.remove_restore(connect=con,post_id=content["post"], status=1)
        threads.dec_posts_count(con,content["post"])
    except Exception as e:
        return json.dumps({"code": 1, "response": (e.message)})
    return json.dumps({"code": 0, "response": post})


@module.route("/restore/", methods=["POST"])
def restore():
    con = connect()
    content = request.json
    required_data = ["post"]
    try:
        choose_required(data=content, required=required_data)
        threads.inc_posts_count(con,content["post"])
        post = posts.remove_restore(connect=con,post_id=content["post"], status=0)
    except Exception as e:
        return json.dumps({"code": 1, "response": (e.message)})
    return json.dumps({"code": 0, "response": post})


@module.route("/update/", methods=["POST"])
def update():
    con = connect()
    content = request.json
    required_data = ["post", "message"]
    try:
        choose_required(data=content, required=required_data)
        post = posts.update(connect=con,update_id=content["post"], message=content["message"])
    except Exception as e:
        return json.dumps({"code": 1, "response": (e.message)})
    return json.dumps({"code": 0, "response": post})


@module.route("/vote/", methods=["POST"])
def vote():
    con = connect()
    content = request.json
    required_data = ["post", "vote"]
    try:
        choose_required(data=content, required=required_data)
        post = posts.vote(connect = con,vote_id=content["post"], vote_type=content["vote"])
    except Exception as e:
        return json.dumps({"code": 1, "response": (e.message)})
    return json.dumps({"code": 0, "response": post})
