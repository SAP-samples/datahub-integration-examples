FROM ubuntu:18.04

RUN apt-get update && apt-get install -y \
	openssl \
	net-tools \
	git \
	locales \
	dumb-init \
	vim \
	curl \
	wget \
	&& rm -rf /var/lib/apt/lists/*

RUN locale-gen en_US.UTF-8
# We cannot use update-locale because docker will not use the env variables
# configured in /etc/default/locale so we need to set it manually.
ENV LC_ALL=en_US.UTF-8 \
	SHELL=/bin/bash

RUN wget https://github.com/cdr/code-server/releases/download/2.1698/code-server2.1698-vsc1.41.1-linux-x86_64.tar.gz
#COPY code-server2.1698-vsc1.41.1-linux-x86_64.tar.gz /code-server2.1698-vsc1.41.1-linux-x86_64.tar.gz
RUN tar xvfz /code-server2.1698-vsc1.41.1-linux-x86_64.tar.gz

RUN groupadd -g 999 coder && \
    useradd -r -u 999 -g coder coder && \
    mkdir /home/coder && \
    chown coder:coder /home/coder

USER 999:999

WORKDIR /home/coder

EXPOSE 3000

ENV HOME /home/coder
ENV GIT_DISCOVERY_ACROSS_FILESYSTEM 1

ENTRYPOINT ["dumb-init", "--"]
CMD ["bash", "-c", "exec /code-server2.1698-vsc1.41.1-linux-x86_64/code-server --port 3000 --auth none /vhome"]
