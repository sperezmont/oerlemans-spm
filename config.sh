#! /bin/bash
echo 'Configuration in progress ...'
[ ! -d "./temp/" ] && mkdir './temp/'

echo 'Installing requirements ...'
pip install -r config/requirements.txt

echo 'Enabling "runmodel" and "runtests" ...'
chmod +x runmodel
chmod +x runtests

echo 'Configuration completed'