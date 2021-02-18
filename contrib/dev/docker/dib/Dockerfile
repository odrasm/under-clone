FROM ubuntu:18.04

ARG DEBIAN_FRONTEND=noninteractive

RUN mkdir -p /underground/elements
RUN mkdir -p /shared
WORKDIR /shared

RUN apt-get update \
 && apt-get install -y \
	apt-utils \
	vim \
 && apt-get install -y \
	python3-pip \
	xfsprogs \
	squashfs-tools \
	sudo \
	kpartx \
	qemu-utils \
	e2fsprogs \
	curl \
	debootstrap \
	efitools \
	gdisk

RUN pip3 install -U pip
RUN python3 -m pip install diskimage-builder bindep dib-utils ironic-python-agent-builder

RUN wget https://raw.githubusercontent.com/openstack/diskimage-builder/master/bindep.txt
RUN bindep --list_all newline --file bindep.txt | xargs apt-get install -y

ENV ELEMENTS_PATH=/underground/elements
ENV DIB_RELEASE=bionic
ENV DIB_CLOUD_INIT_DEFAULT_USER_NAME=e4user
ENV DIB_CLOUD_INIT_DEFAULT_USER_PASSWORD=000000
ENV DIB_CLOUD_INIT_ENABLE_SSH_PASSWORD=1
