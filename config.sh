#! /bin/bash
conda_path='/home/sergio/'
env_name='oerlemans_env' # environment name
py_version='3.7.3'       # python version

echo 'Configuration in progress ...'
[ ! -d "./temp/" ] && mkdir './temp/'
[ ! -d "./output/" ] && mkdir './output/'

echo 'Installing requirements ...'
source ${conda_path}/anaconda3/etc/profile.d/conda.sh
conda create -n ${env_name} python=${py_version}  
conda activate ${env_name}
pip install -r config/requirements.txt
conda deactivate 

echo 'Enabling "runmodel" and "runtests" ...'
chmod +x runmodel
chmod +x runtests

echo 'Configuration completed'
