import subprocess
import os

volatility_exe      = '/home/renanlima/volatility/vol.py'
volmemlyzer_script  = '/home/renanlima/automation/VolatilityFeatureExtractor.py'
dump_directory      = '/home/renanlima/automation/dumps/'
csv_output_file     = '/home/renanlima/automation/csv_file'
dump_number_file    = '/home/renanlima/automation/dumps/processed_dumps.txt'  # File to store the last processed dump number

def get_last_processed_dump_number(file_path):
    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            return int(file.read().strip())

    else:
        return 0  # Default starting dump number if the file doesn't exist

def update_last_processed_dump_number(file_path, new_number):
    with open(file_path, 'w') as file:
        file.write(str(new_number))

if __name__ == '__main__':
    last_processed_dump = get_last_processed_dump_number(dump_number_file)
    next_dump_number = last_processed_dump + 1

    dump_to_process = f"dump{next_dump_number}.dmp"
    dump_path = os.path.join(dump_directory, dump_to_process)

    if os.path.exists(dump_path):
        command = f"python3 {volmemlyzer_script} -o {csv_output_file} -V {volatility_exe} {dump_path}"
        subprocess.run(command, shell=True, check=True)

        update_last_processed_dump_number(dump_number_file, next_dump_number)
        print(f"Processed dump {dump_to_process}")
    else:
        print(f"Dump {dump_to_process} not found.")
