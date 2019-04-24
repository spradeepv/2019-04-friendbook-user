from flask import Flask
from flask import request, jsonify, Response

from user.common.utils import *
from user.common.errors import *

app = Flask(__name__)


@app.route("/user", methods=['GET'])
def getUsers():
    print("Get Users called....")
    emailId = request.args.get('emailId')
    displayName = request.args.get('displayName')
    id = request.args.get('id')
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
    user, status_code = add__or_modify_user(data)
    return jsonify(user), status_code


@app.route("/user", methods=['DELETE'])
def deleteUser():
    emailId = request.args.get('emailId')
    return jsonify(delete_user(emailId))


@app.route("/user/auth", methods=['POST'])
def authenticateUser():
    data = request.get_json()
    authenticated, resp = authenticate_user(data)
    if authenticated:
        return jsonify(resp), 200


@app.route("/user/block", methods=['PUT'])
def blockUnblockUser():
    data = request.get_json()
    return jsonify(block_unblock_user(data))


@app.errorhandler(UserException)
def handle_user_exception(error):
    response = jsonify(error.to_dict())
    return response, error.status_code


@app.errorhandler(UserDbException)
def handle_user_db_exception(error):
    response = jsonify(error.to_dict())
    return response, error.status_code


@app.errorhandler(UserNotFoundException)
def handle_user_not_found_exception(error):
    response = jsonify(error.to_dict())
    return response, error.status_code


@app.errorhandler(UnauthorizedException)
def handle_unauthorized_exception(error):
    response = jsonify(error.to_dict())
    return response, error.status_code


if __name__ == "__main__":
    initialize_db()
    app.run(host="0.0.0.0")
