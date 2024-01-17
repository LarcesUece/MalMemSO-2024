import subprocess
import time
import os
import re

def compress(file, input_folder, output_folder):
    try:
        subprocess.run(["tar", "-acf", os.path.join(output_folder, f"{file}.zip"), os.path.join(input_folder, file)], check=True)
        print(f"Compression successful: {file}")
    except subprocess.CalledProcessError as e:
        print(f"Compression failed: {e}")

dumpit_path = 'C:\\Users\\vboxuser\\Downloads\\automation\\Magnet\\x64\\Dumpit.exe'
dump_folder = 'C:\\Users\\vboxuser\\Downloads\\automation\\tmp'
compressed_folder = r'\\VBOXSVR\dumps'

total_runtime = 3*60   # modify the total runtime if needed
dump_interval = 60      # creates dump every 1 minute

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

files = os.listdir(dump_folder)
print(files)
for file in files:
    dump_path = os.path.join(dump_folder, file)
    compress(file, dump_folder, compressed_folder)
