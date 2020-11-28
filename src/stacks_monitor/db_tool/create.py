import logging

from stacks_monitor.db import db_engine
from stacks_monitor.model import *

logging.basicConfig(level=logging.INFO)


def create_db():
    Base.metadata.create_all(bind=db_engine)
    logging.info("OK")


if __name__ == "__main__":
    create_db()
