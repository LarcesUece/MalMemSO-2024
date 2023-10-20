import subprocess
import time
import os

dumpit_path = '\\path\\to\\dumpit.exe'
dump_folder = '\\path\\to\\dump_folder'

total_runtime = 15*60   # modify the total runtime if needed
dump_interval = 60      # creates dump every 1 minute
count = 1

start_time = time.time()

while time.time() - start_time < total_runtime:
    try:
        dump_filename = f'dump{count}.dmp'
        dump_path = os.path.join(dump_folder, dump_filename)

        subprocess.Popen([dumpit_path, '/OUTPUT', dump_path, '/Q'])

        count += 1
        time.sleep(dump_interval)       # wait for 1 minute to create another dump

    except Exception as e:
        print(f"An error occured: {e}")

print("Finished creating dumps")