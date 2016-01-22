FROM python:3.4

MAINTAINER zqdou zqdou@dataman-inc.com

ADD . /code
WORKDIR /code

ENV GOD_DB_HOST 'localhost'
ENV GOD_DB_PORT '3306'
ENV GOD_DB_NAME 'omega_god'
ENV GOD_DB_USER 'root'
ENV GOD_DB_PASSWORD '111111'

ENV OMEGA_DB_HOST 'localhost'
ENV OMEGA_DB_PORT '3306'
ENV OMEGA_DB_NAME 'omega'
ENV OMEGA_DB_USER 'root'
ENV OMEGA_DB_PASSWORD '111111'

ENV OAPP_DB_HOST 'localhost'
ENV OAPP_DB_PORT '3306'
ENV OAPP_DB_NAME 'oapp'
ENV OAPP_DB_USER 'root'
ENV OAPP_DB_PASSWORD '111111'

VOLUME omega_god/settings.py omega_god/settings.py

#RUN apt-get update -y
#RUN apt-get install python3-dev libmysqlclient-dev libxml2-dev libxslt1-dev -y
RUN pip3 install -r requirements.txt
CMD python3 manage.py runserver 0.0.0.0:8000
