# oerlemans-spm
Oerlemans conceptual model for ice sheets based on Oerlemans (2003)
https://npg.copernicus.org/articles/10/441/2003/

# Quick start guide
* Download
```bash
git clone https://github.com/sperezmont/oerlemans-spm.git
```
* Setup: Enter directory, enable and run config.sh
You may need to change lines 2,3 and 4 of config.sh to your system paths. This script will install the necessary python dependencies and the corresponding virtual environment.
```bash
cd oerlemans-spm
chmod +x config.sh
./config.sh
```
* Finally edit lines 10 and 11 in `runmodel` if needed with your virtual environment name (`env_name`) and `path` to anaconda.

# Tests
In order to get used to the functioning of the model you can run some predefined tests
* Test 1:
