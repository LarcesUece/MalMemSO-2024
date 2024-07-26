# MalMemSO

## Setup Ubuntu 24.04 Server

## update server
`apt update`

`apt upgrade`

## Install server packages
`apt install openssh-server`

`apt install git`

`apt install python3-virtualenv`

`apt install cifs-utils`


## Create directories

`mkdir /var/app`

`mkdir /var/app/dumps`

`mkdir /var/app/webapp`


## Move to work directory
`cd /var`

## Create virtual env
`virtualenv app`

`cd /var/app`

## Activate virtual env
`source bin/activate`

## Install dependencies
`pip3 install pefile`

`pip3 install yara-python`

`pip3 install capstone`

`pip3 install pycryptodome`

`pip3 install pandas`

`pip3 install flask`

`pip3 install setuptools`

`pip3 install bigquery`

`pip3 install numpy==1.26.4`

`pip3 install pywinrm`

## Install Volatility3 and VolMemLyzer

`cd /var/app/webapp`

`git clone https://github.com/volatilityfoundation/volatility3.git`

`git clone https://github.com/ahlashkari/VolMemLyzer`
