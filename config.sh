#! /bin/bash
echo 'Configuration in progress ...'

echo 'Installing requirements ...'
pip install -r config/requirements.txt

echo 'Enabling "runmodel" and "runtests" ...'
chmod +x runmodel
chmod +x runtests

echo 'Configuration completed'