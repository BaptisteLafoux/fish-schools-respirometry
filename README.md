

# Respirometry on fish schools 

This repository regroups code that:
- extracts data from respirometry files (timeseries of O2 concentration measurement)
- plots this data

## Getting started
### Clone the repo
The code runs on Python 3. Copy the following lines in your terminal to get started: 
```
git clone https://github.com/BaptisteLafoux/fish-schools-respirometry
cd fish-schools-respirometry
```
> note that cloning the repo will download ~30Mo of (useful) data

### Install the requirements 
The code relies on different libraries. To install them in a virtual environment (```respirenv``````), do
```
conda create -n respirenv python=3.11 anaconda
```
then
```
conda install --file requirements.txt
```
(or ```pip install requirements.txt```) 

