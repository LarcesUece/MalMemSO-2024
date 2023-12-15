import subprocess
import time
import os
import re

dumpit_path = 'C:\\Users\\renan\\OneDrive\\Área de Trabalho\\automation\\Dumpit\\x64\\DumpIt.exe'
dump_folder = r'\\VBOXSVR\dumps'

total_runtime = 3*60   # modify the total runtime if needed
dump_interval = 40      # creates dump every 1 minute

start_number = 1  # Starting number for the dumps

# Check existing dump files to find the latest number in the sequence
existing_dumps = [filename for filename in os.listdir(dump_folder) if re.match(r'dump\d+\.dmp', filename)]
if existing_dumps:
    latest_dump_number = max(int(re.search(r'dump(\d+)\.dmp', filename).group(1)) for filename in existing_dumps)
    start_number = latest_dump_number + 1

start_time = time.time()
count = start_number

while time.time() - start_time < total_runtime:
    try:
        dump_filename = f'dump{count}.dmp'
        dump_path = os.path.join(dump_folder, dump_filename)

        subprocess.Popen([dumpit_path, '/OUTPUT', dump_path, '/Q'])

        count += 1
        time.sleep(dump_interval)       # wait for 1 minute to create another dump

    except Exception as e:
        print(f"An error occurred: {e}")

print("Finished creating dumps")
