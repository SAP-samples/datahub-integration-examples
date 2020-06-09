FROM python:3.6.4-slim-stretch

ENV DEBIAN_FRONTEND=noninteractive 

RUN apt-get update && \
 apt install -y python3-pip && \
 apt-get install -y python3-dev && \
 apt-get install -y krb5-user && \
 apt-get install -y libsasl2-dev && \
 apt-get install -y libsasl2-modules-gssapi-mit && \
 mkdir /keytabs

# Install python libraries
RUN pip3 install pyhive[hive]
RUN pip3 install tornado==5.0.2


# Add vflow user and vflow group to prevent error 
# container has runAsNonRoot and image will run as root
RUN groupadd -g 1972 vflow && useradd -g 1972 -u 1972 -m vflow
USER 1972:1972
WORKDIR /home/vflow
ENV HOME=/home/vflow