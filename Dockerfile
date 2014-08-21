FROM ubuntu:latest

MAINTAINER johnys

RUN apt-get update
RUN apt-get install -y git
RUN apt-get install -y vim
RUN apt-get install -y python-pip
RUN apt-get install -y python

ADD app/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
