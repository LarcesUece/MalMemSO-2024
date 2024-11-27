from utils import setup_argparser, setup_logging


def disable_network():
    pass


if __name__ == "__main__":
    setup_logging(custom_filename=True)
    args = setup_argparser()
    disable_network(**vars(args))
