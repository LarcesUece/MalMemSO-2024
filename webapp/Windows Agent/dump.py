import os
#import time
import socket
import requests
from datetime import datetime

FOG_URL = "http://192.168.0.13:5000/detect"

# Function to export current memory dump and returns dump file name 
def export_dump():
    # The file name will be the datetime from the memory dump
    current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
    
    print("Init dumpIt")
    print(datetime.now())
    # Exporting the memory dump
    cmd = "lib/DumpIt.exe /Q /N /O " + current_datetime
    os.system(cmd)
    print("End dumpIt")
    print(datetime.now())
    
    # Wait to create the dump
    #time.sleep(60)
    
    #  Compress the memory dump
    print("Init TAR")
    print(datetime.now())
    cmd = "tar -czvf " + current_datetime + ".tar.gz " + current_datetime 
    os.system(cmd)
    print("End TAR")
    print(datetime.now())
    
    # Wait to compress the file
    #time.sleep(60)
    
    # Delete original dump and keep the compressed file
    #remove_file(current_datetime)

    return current_datetime

# Function to request the memory dump analysis    
def request_mem_analysis(export_datetime):
    url = FOG_URL
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    
    # send request
    post_obj = {"ip": ip_address, "hostname": hostname, "datetime": export_datetime }
    req  = requests.post(url, post_obj)
    

# Export dump   
export_datetime = export_dump() 

# Request dump analysis
request_mem_analysis(export_datetime)