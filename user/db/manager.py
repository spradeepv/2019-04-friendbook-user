from datetime import datetime
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from user.common.errors import UserDbException
from user.db.models import users as models

log = logging.getLogger(__name__)


class DBConnection(object):
    def __init__(self, host, user, password, dbname='users'):
        self.connection_url = 'mysql+pymysql://' + str(user) + ':' + \
                              str(password) + '@' + str(host) + '/' + \
                              str(dbname)

        self.host = host
        self.user = user
        self.password = password
        self.dbname = dbname
        self.engine = None
        self.connection = None
        self.session = None

    def create_session(self):
        try:
            self.engine = create_engine(
                self.connection_url
            )
            session = sessionmaker(bind=self.engine)
            self.session = session()
            self.connection = self.session.connection()
        except Exception as e:
            err_msg = 'Exception while creating mysql '
            err_msg += 'session with end point:' + self.connection_url
            log.error("%s: %s", err_msg, e)
            raise UserDbException(err_msg)

    def create_users_schema(self):
        ''' To create the users database schema '''
        try:
            models.Base.metadata.create_all(self.engine)
        except Exception as e:
            err_msg = 'Exception while creating users schema '
            log.error("%s: %s", err_msg, e)
            raise UserDbException(err_msg)

    def delete_user_schema(self):
        ''' To delete the user1 database schema '''
        models.Base.metadata.drop_all(self.engine)

    def _insert_row(self, obj, table_name=None):
        ''' To insert table into users database '''
        try:
            self.session.add(obj)
        except Exception as e:
            err_msg = "Exception while inserting a row into table :"
            err_msg += table_name
            log.error("%s: %s", err_msg, e)
            raise UserDbException(err_msg)
        self.session.commit()

    def add_user(self, user):
        user_row = models.users(
            emailId=user["emailId"],
            displayName=user["displayName"],
            password=user["password"],
            status="ACTIVE",
            createdAt=datetime.now()
        )
        self._insert_row(user_row, 'users')
        return user

    def get_users(self):
        try:
            query = self.session.query(models.users)
            rows = query.all()
        except Exception as e:
            err_msg = 'Exception while executing query get_users'
            log.error("%s: %s", err_msg, e)
            raise UserDbException(err_msg)
        return rows

    def get_user_by_email_id(self, email_id):
        try:
            query = self.session.query(models.users)
            rows = query.filter_by(emailId=email_id).all()
        except Exception as e:
            err_msg = 'Exception while executing query get_users'
            log.error("%s: %s", err_msg, e)
            raise Exception(err_msg)
        return rows

    def get_user_by_displayname(self, displayName):
        try:
            query = self.session.query(models.users)
            rows = query.filter_by(displayName=displayName).all()
        except Exception as e:
            err_msg = 'Exception while executing query get_users'
            log.error("%s: %s", err_msg, e)
            raise Exception(err_msg)
        return rows

    def get_user_by_id(self, id):
        try:
            query = self.session.query(models.users)
            rows = query.filter_by(id=id).all()
        except Exception as e:
            err_msg = 'Exception while executing query get_users'
            log.error("%s: %s", err_msg, e)
            raise Exception(err_msg)
        return rows

    def delete_user(self, emailId):
        try:
            query = self.session.query(models.users)
            query.filter_by(emailId=emailId).delete()
        except Exception as e:
            err_msg = 'Exception while deleting user1 '
            log.error("%s %s: %s", err_msg, emailId, e)
            raise UserDbException(err_msg)
        self.session.commit()

    def update_user(self, user):
        query = self.session.query(models.users)
        query.filter_by(
            emailId=user["emailId"]).update({'password': user["password"],
                                             'status': user["status"],
                                             'displayName': user[
                                                 "displayName"],
                                             'updatedAt': datetime.now()
                                             })
        self.session.commit()

    def close(self):
        ''' To close connection handle '''
        if self.session:
            self.session.rollback()
            self.session.close()
        if self.connection:
            self.session.rollback()
            self.connection.close()
        if self.engine:
            self.engine.dispose()

