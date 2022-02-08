# oerlemans-spm
Oerlemans conceptual model for ice sheets based on Oerlemans (2003)
https://npg.copernicus.org/articles/10/441/2003/

# Quick start guide
* Download
```bash
git clone https://github.com/sperezmont/oerlemans-spm.git
```
* Setup

Enter directory, enable and run config.sh. You may need to change lines 2,3 and 4 of config.sh to your system paths. This script will install the necessary python dependencies and the corresponding virtual environment.
```bash
cd oerlemans-spm
chmod +x config.sh
./config.sh
```
* Finally edit lines 10 and 11 in `runmodel` if needed with your virtual environment name (`env_name`) and `path` to anaconda.

# How to run an experiment
```bash
./runmodel params_name.nml exp_name
```
where `params_name.nml` is the name of the parameters file located in `/par/` and `exp_name` the name of the corresponding experiment.

# Tests
In order to get used to the functioning of the model you can run some predefined tests
* Test 1: Constant forcing
```bash
./runmodel params_test1.nml test1
```

* Test 2: Periodical forcing in zE
```bash
./runmodel params_test2.nml test2
```

* Test 3: Periodical forcing in sea level
```bash
./runmodel params_test3.nml test3
```

* Test 4: Periodical forcing in both zE and sea level
```bash
./runmodel params_test4.nml test4
```
You can even run all the experiments at the same time with
```bash
./runtests
```
