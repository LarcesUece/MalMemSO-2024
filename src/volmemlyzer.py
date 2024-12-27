from subprocess import Popen, PIPE
from re import search, DOTALL
from logging import info
from app import app


class VolMemLyzer:
    def __init__(self):
        self.volmemlyzer_file = app.config["VOLMEMLYZER_FILE"]
        self.raw_dir = app.config["RAW_DIR"]
        self.csv_dir = app.config["CSV_DIR"]
        self.volatility_file = app.config["VOLATILITY_FILE"]

    def edit_vol_modules(target_file, new_dict):
        info("Iniciando a edição do arquivo do VolMemLyzer.")
        with open(target_file, "r") as file:
            content = file.read()
        info("Arquivo lido.")

        match = search(r"(VOL_MODULES\s*=\s*)({.*?})", content, DOTALL)

        if match:
            info("Dicionário encontrado.")
            old_dict = match.group(2)
            updated_content = content.replace(old_dict, new_dict.strip())

            with open(target_file, "w") as file:
                file.write(updated_content)
            info("Arquivo atualizado.")

        else:
            raise ValueError(
                "Unable to find the VOL_MODULES dictionary in the target file."
            )

    def run(self):
        info("Inicando execução do VolMemLyzer.")
        command = [
            "python",
            self.volmemlyzer_file,
            "-f",
            self.raw_dir,
            "-o",
            self.csv_dir,
            "-V",
            self.volatility_file,
        ]

        try:
            process = Popen(command, stdout=PIPE, stderr=PIPE)
            stdout, stderr = process.communicate()
        except Exception:
            raise

        info("Análise concluída.")
        info(stdout.decode())
        info(stderr.decode())
