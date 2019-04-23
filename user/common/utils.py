from user.db import manager as db_conn

db = db_conn.DBConnection("localhost",
                          "root",
                          "test123",
                          "users")


def initialize_db():
    db.create_session()
    db.create_users_schema()
    db.close()


def create_session():
    db.create_session()


def close_db():
    db.close()


def add__or_modify_user(data):
    user = db.get_user_by_email_id(data["emailId"])
    if len(user) > 0:
        status = data.get('status', None)
        if status is None:
            status = user[0].status
            data['status'] = status
        db.update_user(data)
    else:
        print("Add User: ", data)
        data['status']= "ACTIVE"
        db.add_user(data)
    data.pop('password')
    return data


def get_users():
    users = db.get_users()
    user_list = []
    for user in users:
        user_list.append(get_user_dict(user))
    return user_list


def get_user_by_emailId(emailId):
    user = db.get_user_by_email_id(emailId)
    if len(user) > 0:
        return get_user_dict(user[0])
    return []


def get_user_by_displayName(displayName):
    user = db.get_user_by_displayname(displayName)
    if len(user) > 0:
        return get_user_dict(user[0])
    return []


def get_user_by_id(id):
    user = db.get_user_by_id(id)
    if len(user) > 0:
        return get_user_dict(user[0])
    return []


def delete_user(emailId):
    db.delete_user(emailId)


def authenticate_user(data):
    emailId = data["emailId"]
    password = data["password"]
    user = db.get_user_by_email_id(emailId)
    if len(user) > 0:
        return user[0].password == password, get_user_dict(user[0])
    return False, None

def block_unblock_user(data):
    user = db.get_user_by_email_id(data['emailId'])
    if len(user) > 0:
        if data["block"] == "true":
            user[0].status = "BLOCKED"
        else:
            user[0].status = "ACTIVE"
        return db.update_user(user[0])
    return ""

def get_user_dict(user):
    user_dict = {}
    user_dict['emailId'] = user.emailId
    user_dict['id'] = user.id
    user_dict['displayName'] = user.displayName
    user_dict['status'] = user.status
    return user_dict