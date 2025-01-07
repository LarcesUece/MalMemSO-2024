import time
import dotenv

import data


def run():
    while True:
        time.sleep(3600)


if __name__ == "__main__":
    dotenv.load_dotenv()
    data.write_initial_data()
    run()
