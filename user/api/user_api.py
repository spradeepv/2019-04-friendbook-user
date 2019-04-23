from flask import Flask
from flask import request, jsonify, Response
from user.common.utils import *

app = Flask(__name__)


@app.route("/user", methods=['GET'])
def getUsers():
    print("Get Users called....")
    emailId = request.args.get('emailId')
    displayName = request.args.get('displayName')
    id = request.args.get('id')
    print(emailId)
    print(displayName)
    print(id)
    if emailId is not None:
        return jsonify(get_user_by_emailId(emailId))
    elif displayName is not None:
        return jsonify(get_user_by_displayName(displayName))
    elif id is not None:
        return jsonify(get_user_by_id(id))
    else:
        return jsonify(get_users())


@app.route("/user", methods=['PUT'])
def addOrModifyUser():
    data = request.get_json()
    print(data)
    return jsonify(add__or_modify_user(data))


@app.route("/user", methods=['DELETE'])
def deleteUser():
    emailId = request.args.get('emailId')
    return jsonify(delete_user(emailId))


@app.route("/user/auth", methods=['POST'])
def authenticateUser():
    data = request.get_json()
    authenticated, resp = authenticate_user(data)
    if authenticated:
        return jsonify(resp), 201
    return "", 404


@app.route("/user/block", methods=['PUT'])
def blockUnblockUser():
    data = request.get_json()
    return jsonify(block_unblock_user(data))


if __name__ == "__main__":
    initialize_db()
    app.run(host='0.0.0.0')
