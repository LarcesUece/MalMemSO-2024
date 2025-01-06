import time
import dotenv

from data import write_initial_data


def run():
    while True:
        time.sleep(3600)


if __name__ == "__main__":
    dotenv.load_dotenv()
    write_initial_data()
    run()
