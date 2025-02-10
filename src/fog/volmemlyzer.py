from subprocess import Popen, PIPE
from re import search, DOTALL
from app import app
from src import report


def edit_vol_modules(target_file, new_dict):
    print("Iniciando a edição do arquivo do VolMemLyzer.")
    with open(target_file, "r") as file:
        content = file.read()
    print("Arquivo lido.")

    match = search(r"(VOL_MODULES\s*=\s*)({.*?})", content, DOTALL)

    if match:
        print("Dicionário encontrado.")
        old_dict = match.group(2)
        updated_content = content.replace(old_dict, new_dict.strip())

        with open(target_file, "w") as file:
            file.write(updated_content)
        print("Arquivo atualizado.")

    else:
        raise ValueError(
            "Unable to find the VOL_MODULES dictionary in the target file."
        )


def edit_output_file(target_file, new_output):
    with open(target_file, "r") as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if line.strip().startswith(
            "file_path = os.path.join(CSVoutput_path, 'output.csv')"
        ):
            lines[i] = f"    file_path = os.path.join(CSVoutput_path, '{new_output}')\n"
            break

    with open(target_file, "w") as file:
        file.writelines(lines)


def run():
    volmemlyzer_file = app.config.get("VOLMEMLYZER_FILE")
    processing_raw_dir = app.config.get("PROCESSING_RAW_DIR")
    csv_dir = app.config.get("CSV_DIR")
    volatility_file = app.config.get("VOLATILITY_FILE")

    print("Inicando execução do VolMemLyzer.")
    command = [
        "python",
        volmemlyzer_file,
        "-f",
        processing_raw_dir,
        "-o",
        csv_dir,
        "-V",
        volatility_file,
    ]

    try:
        process = Popen(command, stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
    except Exception:
        raise

    print("Análise concluída.")
    print(stdout.decode())
    print(stderr.decode())
