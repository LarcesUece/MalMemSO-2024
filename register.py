from google.cloud import bigquery
from datetime import datetime
#from bigquery import get_client

def on_bigquery(hostname, ip, datetime, is_detected):

#    datetime = datetime.now()
#    hostname = "desktop"
#    ip = "192.168.0.0"
#    is_detected = False

    project_id = 'malware-detection-422423' # Fill with project ID
    #service_account = 'bq-user@malware-detection-422423.iam.gserviceaccount.com>
    dataset = "detection_records" # Fill with dataset name
    table = "records" # Fill with table name

    # JSON key provided by Google
    json_key = 'malware-detection-422423-bde15ff25756.json'
    try:
        client = bigquery.Client(json_key_file=json_key)
    except:
        print("Was not possible to register")
        return

    rows =  [
        {'hostname': hostname, 'ip': ip, "is_malware_detected": is_detected,  "timestamp": datetime} ]
    print("Recording")
    # Insert data into table.
    try:
        inserted = client.push_rows(dataset, table, rows)
    except:
        print("Was not possible to register")
        pass
    
    return
