FROM python:3.6.4-alpine3.4

ENV PYTHONPATH="/userservice"
#RUN pip install PyMySQL Flask sqlalchemy SQLAlchemy-Utils passlib
ADD requirements.txt .
RUN python3.6 -m pip install -r requirements.txt
WORKDIR /userservice
COPY . .

CMD [ "python", "user/api/user_api.py" ]
