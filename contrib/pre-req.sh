#!/bin/bash

sudo mkdir /usr/local/src/underground
sudo chown ubuntu. /usr/local/src/underground

sudo apt install python3-pip
sudo python3 -m pip install 'ansible<2.10'
