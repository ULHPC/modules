#!/bin/bash

mkdir -p $HOME/.resif/src && cd $HOME/.resif/src
git clone https://gitlab.uni.lu/modules/infrastructure.git .
sudo pip install $HOME/.resif/src/bin/
sudo mkdir /usr/local/apps
sudo chown $USER: /usr/local/apps
resif user cleaninstall core