from user.common import constants as const

class UserException(Exception):
    user_default_status_code = const.DEFAULT_STATUS_CODE

    def __init__(self, message, status_code=None):
        Exception.__init__(self)
        if status_code is None:
            status_code = self.user_default_status_code
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        response = dict()
        response['message'] = self.message
        response['status_code'] = self.status_code
        return response


class UserDbException(UserException):
    db_default_status_code = const.DB_DEFAULT_STATUS_CODE

    def __init__(self, message, status_code=None):
        if status_code is None:
            status_code = self.db_default_status_code
        UserException.__init__(self, message, status_code)


class UserNotFoundException(UserException):
    user_not_found_status_code = const.NOT_FOUNT_STATUS_CODE

    def __init__(self, message, status_code=None):
        if status_code is None:
            status_code = self.user_not_found_status_code
        UserException.__init__(self, message, status_code)

class UnauthorizedException(UserException):
    unauthorized_status_code = const.UNAUTHORIZED_STATUS_CODE

    def __init__(self, message, status_code=None):
        if status_code is None:
            status_code = self.unauthorized_status_code
        UserException.__init__(self, message, status_code)
