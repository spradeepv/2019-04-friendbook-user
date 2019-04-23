from sqlalchemy import Integer, String, Column, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import PasswordType

Base = declarative_base()


# Python object for lbaas_networks table
class users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    emailId = Column(String(256))
    password = Column(PasswordType(
        schemes=[
            'pbkdf2_sha512',
            'md5_crypt'
        ],
        deprecated=['md5_crypt'])
    )
    displayName = Column(String(256))
    status = Column(String(256))
    createdAt = Column(DateTime)
    updatedAt = Column(DateTime)
