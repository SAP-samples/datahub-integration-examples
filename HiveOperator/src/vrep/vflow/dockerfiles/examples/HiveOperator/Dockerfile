FROM $com.sap.python27

ENV DEBIAN_FRONTEND=noninteractive 

RUN apt-get update && \
 apt install -y python-pip && \
 apt-get install -y python-dev && \
 apt-get install -y krb5-user && \
 apt-get install -y libsasl2-dev && \
 apt-get install -y libsasl2-modules-gssapi-mit && \
 python2.7 -m pip install pyhive[hive] && \
 mkdir /keytabs