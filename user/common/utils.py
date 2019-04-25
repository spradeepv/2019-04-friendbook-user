import logging
import time

from user.db import manager as db_conn
from user.common.errors import UserNotFoundException, UnauthorizedException
from user.common.constants import DB_NAME, DB_USER, DB_PASSWORD
from user.common.config import DB_HOST

log = logging.getLogger(__name__)
db = db_conn.DBConnection(DB_HOST,
                          DB_USER,
                          DB_PASSWORD,
                          DB_NAME)


def initialize_db():
    count = 0
    retry = False
    while not retry:
        try:
            db.create_session()
            db.create_users_schema()
            retry = False
        except UserDbException e:
            count += 1
            log.error(e)
            time.sleep(10)
            if count > 10:
                return
        finally:
            db.close()


def create_session():
    db.create_session()


def close_db():
    db.close()


def add__or_modify_user(data):
    status_code = 201
    log.debug("add_or_modify_user")
    user = db.get_user_by_email_id(data["emailId"])
    if len(user) > 0:
        log.debug("User with emailId %s found. Modifying user", data["emailId"])
        status = data.get('status', None)
        if status is None:
            status = user[0].status
            data['status'] = status
        db.update_user(data)
        status_code = 202
    else:
        log.debug("Adding User with emailId - ", data['emailId'])
        data['status']= "ACTIVE"
        db.add_user(data)
    data.pop('password')
    return data, status_code


def get_users():
    users = db.get_users()
    user_list = []
    for user in users:
        user_list.append(get_user_dict(user))
    if len(user_list) == 0:
        raise UserNotFoundException("Users not found")
    return user_list


def get_user_by_emailId(emailId):
    user = db.get_user_by_email_id(emailId)
    if len(user) > 0:
        return get_user_dict(user[0])
    else:
        raise UserNotFoundException("User not found")


def get_user_by_displayName(displayName):
    user = db.get_user_by_displayname(displayName)
    if len(user) > 0:
        return get_user_dict(user[0])
    else:
        raise UserNotFoundException("User not found")


def get_user_by_id(id):
    user = db.get_user_by_id(id)
    if len(user) > 0:
        return get_user_dict(user[0])
    else:
        raise UserNotFoundException("User not found")


def delete_user(emailId):
    log.info("delete_user called")
    try:
        get_user_by_emailId(emailId)
    except UserNotFoundException as e:
        raise UserNotFoundException(e.message)
    db.delete_user(emailId)


def authenticate_user(data):
    emailId = data["emailId"]
    password = data["password"]
    user = db.get_user_by_email_id(emailId)
    if len(user) > 0:
        if user[0].password == password:
            return True, get_user_dict(user[0])
        else:
            raise UnauthorizedException("User is not authorized.")
    else:
        raise UserNotFoundException("User Not Found.")


def block_unblock_user(data):
    user = db.get_user_by_email_id(data['emailId'])
    if len(user) > 0:
        if data["block"] == "true":
            user[0].status = "BLOCKED"
        else:
            user[0].status = "ACTIVE"
        data['status'] = user[0].status
        return db.update_user(data)
    else:
        raise UserNotFoundException("User not found.")


def get_user_dict(user):
    user_dict = {}
    user_dict['emailId'] = user.emailId
    user_dict['id'] = user.id
    user_dict['displayName'] = user.displayName
    user_dict['status'] = user.status
    return user_dict
