import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')


def python_loging(mgs):
    if mgs == "none":
        logging.info(mgs)
    logging.info(mgs)
