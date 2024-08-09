# MalMemSO

## Setup Windows Agent

Install python3
'https://www.python.org/downloads/'

Install pip

Install requests

'pip3 install requests'

Enable Windows Subsystem Linux

Create and share folder Documents/Dumps on current user home

Copy dump.py to Documents/Dumps

Create folder Documents/Dumps/lib on current user home

Copy dumpIt files to Documents/Dumps/lib

Edit dump.py to actual Fog IP/URL 

Create a task in Windows Task Scheduler to execute dump.py every hour. The task must execute with administrator privileges 
