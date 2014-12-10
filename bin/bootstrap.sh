#!/bin/bash

mkdir -p $HOME/.resif/src && cd $HOME/.resif/src
git clone https://gitlab.uni.lu/modules/infrastructure.git .
cd bin
sudo pip install .
sudo mkdir /usr/local/apps
sudo chown $USER: /usr/local/apps
resif user cleaninstall