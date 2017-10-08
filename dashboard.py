from flask import Flask, request, jsonify
from db import fetch
import pymongo, sys, traceback
from bson.objectid import ObjectId

app = Flask(__name__)


@app.route('/profile', methods=['POST'])
def profile():
    try:
        pr_db = pymongo.MongoClient().pr_database.report_users
        user_info = pr_db.find_one({"_id": ObjectId(request.json["user_id"])})
        user_id = user_info["login"]
    except:
        print("REQUEST:", request.json, file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        return 'User profile invalid', 403

    if request.json["action"] == 'fetch':
        ret_dict = fetch.profile(user_id)
        ret_dict["user_id"] = user_id
        ret_dict["avatar_url"] = user_info.get("avatar_url", "img/user.png")
        return jsonify(ret_dict)
    elif request.json["action"] == 'fetch_ranged':
        return jsonify(fetch.profile_ranged(user_id, request.json["start_date"], request.json["end_date"]))
    elif request.json["action"] == 'trends':
        return jsonify(fetch.trends(user_id))
    else:
        return 'Request not handled', 501


@app.route('/modal', methods=['POST'])
def modal():
    pr_db = pymongo.MongoClient().pr_database.report_users
    try:
        user_info = pr_db.find_one({"_id": ObjectId(request.json["user_id"])})
    except:
        return 'User profile invalid', 403

    return jsonify(fetch.modal(user_info["login"], request.json["action"], request.json["label"]))


@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    if request.method == 'OPTIONS':
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
        headers = request.headers.get('Access-Control-Request-Headers')
        if headers:
            response.headers['Access-Control-Allow-Headers'] = headers
    return response


if __name__ == '__main__':
    app.run(threaded=True)
