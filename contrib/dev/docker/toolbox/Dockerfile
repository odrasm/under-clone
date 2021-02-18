FROM ubuntu:18.04

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
 && apt-get install -y apt-utils \
 && apt-get install -y \
	git \
    git-review \
	vim \
	sudo \
	mlocate \
	wget \
	curl \
	sshpass \
    dialog \
	python3 \
	python3-pip \
	python3-virtualenv \
    python3-venv \
    python3-setuptools \
    python3-requests \
    python3-distutils \
    python3-passlib \
    virtualenv \
    iputils-ping \
    iproute2 \
    mtr-tiny

RUN wget --no-check-certificate -c https://idm.cloud.e4.lan/ipa/config/ca.crt -O /usr/local/share/ca-certificates/e4lan.crt && \
    update-ca-certificates

RUN cd /root/ && \
    mkdir -p /root/underground && \
    mkdir -p /root/master && \
    cd /root/master && \
    git clone https://review.cloud.e4.lan/e4/underground && \
    mkdir -p /root/.ssh

RUN cd /root/master/underground && \
    pip3 install -r requirements.txt && \
    pip3 install -r test-requirements.txt && \
    bindep -b | xargs apt install -y && \
    ln -s /usr/bin/python3 /usr/bin/python

RUN echo 'pip3 install -r requirements.txt ; pip3 install -r test-requirements.txt ; bindep -b | xargs apt install -y' > /usr/local/bin/testdep.sh
RUN chmod +x /usr/local/bin/testdep.sh
RUN echo 'python3 -m build ; twine upload --config-file .pypirc --repository nexus dist/*' > /usr/local/bin/build.sh
RUN chmod +x /usr/local/bin/build.sh

ENV container docker
ENV PATH="/root/.local/bin:${PATH}"
ENV ANSIBLE_CONFIG="/root/underground/etc/ansible.cfg"
ENV PIP_INDEX="https://pypi.cloud.e4.lan/repository/pypi/"
#ENV PIP_INDEX_URL="https://pypi.cloud.e4.lan/repository/pypi/simple/"

WORKDIR /root/underground
