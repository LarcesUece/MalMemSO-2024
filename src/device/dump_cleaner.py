from utils import setup_logging, setup_argparser


def clean_dump():
    pass


if __name__ == "__main__":
    setup_logging(custom_filename=True)
    args = setup_argparser()
    clean_dump(**vars(args))
