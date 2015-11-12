FROM python:3.4

MAINTAINER zqdou zqdou@dataman-inc.com

ADD . /code
WORKDIR /code

VOLUME omega_god/settings.py omega_god/settings.py

#RUN apt-get install python3-dev -y
RUN pip3 install -r requirements.txt
CMD python3 manage.py runserver 0.0.0.0:8000
