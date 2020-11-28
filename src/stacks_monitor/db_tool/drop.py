import logging
import sys

from aparat import assert_env_vars

from stacks_monitor.db import db_engine
from stacks_monitor.model import *

logging.basicConfig(level=logging.INFO)


def drop_db(warn=True):
    env = assert_env_vars("ENV")

    if env != "devel":
        logging.error("Can't drop db in {} environment!".format(env))
        exit(1)

    if warn:
        confirm = input('All data will be deleted. Are you sure? Y or N: ')

        while confirm not in ['Y', 'N']:
            confirm = input('Y or N: ')

        if confirm == 'N':
            logging.info('Aborting.')
            sys.exit(0)

    Base.metadata.drop_all(bind=db_engine)
    logging.info("OK")


if __name__ == "__main__":
    drop_db()
