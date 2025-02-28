import csv
import os
from re import DOTALL, search
from subprocess import PIPE, Popen

from flask import current_app as app


def init_lib():
    edit_vol_modules()
    edit_input_file_list()


def edit_vol_modules():
    volmemlyzer_file = app.config.get("FILE_VOLMEMLYZER")
    new_vol_modules = app.config.get("VOLMEMLYZER_NEW_VOL_MODULES")

    app.logger.info("Iniciando a edição do arquivo do VolMemLyzer.")
    with open(volmemlyzer_file, "r") as file:
        content = file.read()
    app.logger.info("Arquivo lido.")

    match = search(r"(VOL_MODULES\s*=\s*)({.*?})", content, DOTALL)

    if match:
        app.logger.info("Dicionário encontrado.")
        old_dict = match.group(2)
        updated_content = content.replace(old_dict, new_vol_modules.strip())

        with open(volmemlyzer_file, "w") as file:
            file.write(updated_content)
        app.logger.info("Arquivo atualizado.")

    else:
        raise ValueError(
            "Unable to find the VOL_MODULES dictionary in the target file."
        )


def edit_input_file_list():
    volmemlyzer_file = app.config.get("FILE_VOLMEMLYZER")
    raw_dir = app.config.get("DIR_RAW")

    with open(volmemlyzer_file, "r") as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if line.strip().startswith("file_list ="):
            lines[i] = "    file_list = [args.memdump]\n"
        elif line.strip().startswith("folderpath ="):
            lines[i] = f"    folderpath = str('{raw_dir}')\n"

    with open(volmemlyzer_file, "w") as file:
        file.writelines(lines)


def run(filename: str) -> None:
    output_dir = app.config.get("DIR_CSV")
    volmemlyzer_file = app.config.get("FILE_VOLMEMLYZER")
    volatility_file = app.config.get("FILE_VOLATILITY")

    print("Inicando execução do VolMemLyzer.")
    command = [
        "python",
        volmemlyzer_file,
        "-f",
        filename,
        "-o",
        output_dir,
        "-V",
        volatility_file,
    ]
    print(command)

    try:
        process = Popen(command, stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
    except Exception:
        raise

    print("Análise concluída.")
    print(stdout.decode())
    print(stderr.decode())


def get_report_from_csv(filename: str) -> list | None:
    file_path = os.path.join(app.config.get("DIR_CSV"), "output.csv")
    with open(file_path, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        rows = list(reader)

        for row in reversed(rows):
            if len(row) >= 2 and row[1] == filename:
                print(row)
                return row
        return None
