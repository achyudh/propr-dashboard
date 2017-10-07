from flask import Flask, request, jsonify
from db import fetch

app = Flask(__name__)


@app.route('/profile', methods=['POST'])
def profile():
    if request.json["action"] == 'fetch':
        return jsonify(fetch.profile(request.json["user_id"]))
    elif request.json["action"] == 'fetch_ranged':
        return jsonify(fetch.profile_ranged(request.json["user_id"], request.json["start_date"], request.json["end_date"]))
    elif request.json["action"] == 'trends':
        return jsonify(fetch.trends())
    else:
        return 'Request not handled', 501


@app.route('/modal', methods=['POST'])
def modal():
    return jsonify(fetch.modal(request.json["user_id"], request.json["action"], request.json["label"]))


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
