import sys
import time
from datetime import datetime

import pytz
from aparat import create_logger
from sqlalchemy.orm import Session
import json

from stacks_monitor.coin_rate import get_stx_usd_for_date, get_stx_btc_for_date
from stacks_monitor.db import session_maker
from stacks_monitor.model import Transaction, Block, CurrencyRate
from stacks_monitor.stacks_api import RosettaBlock, rosetta_get_block, get_transaction

logger = create_logger("sync")


def exception_handler(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logger.critical('Unhandled Exception', exc_info=(exc_type, exc_value, exc_traceback))


sys.excepthook = exception_handler


def insert_block(block: RosettaBlock, db_session: Session) -> Block:
    block_height = block["block_identifier"]["index"]
    txs = [x["transaction_identifier"]["hash"] for x in block["transactions"]]
    burn_block_time = block["timestamp"]

    # block
    b = Block()
    b.height = block_height
    b.hash = block["block_identifier"]["hash"]
    b.parent_block_hash = block["parent_block_identifier"]["hash"] if block_height > 1 else ""  # exception for first block
    b.txs = txs
    b.burn_block_time = burn_block_time
    db_session.add(b)

    # transactions
    for t in txs:
        tx_data = get_transaction(t)

        tr = Transaction()
        tr.hash = tx_data["tx_id"]
        tr.block_height = block_height
        tr.raw = tx_data

        db_session.add(tr)

    # crypto rates for the block time
    burn_block_time_iso = datetime.fromtimestamp(burn_block_time / 1000).replace(tzinfo=pytz.utc)

    cr_stx_usd = CurrencyRate()
    cr_stx_usd.block_height = block_height
    cr_stx_usd.pair = "stx-usd"
    cr_stx_usd.rate = get_stx_usd_for_date(burn_block_time_iso)
    db_session.add(cr_stx_usd)

    cr_stx_btc = CurrencyRate()
    cr_stx_btc.block_height = block_height
    cr_stx_btc.pair = "stx-btc"
    cr_stx_btc.rate = get_stx_btc_for_date(burn_block_time_iso)
    db_session.add(cr_stx_btc)

    # commit
    db_session.commit()

    logger.info("Got new block {} - {}".format(b.height, b.hash))

    return b


db_session = session_maker()


def sync():
    try:
        height_remote = rosetta_get_block()["block"]["block_identifier"]["index"]
    except json.decoder.JSONDecodeError as ex:
        logger.error("Rosetta fetch error: {}".format(str(ex)))
        return

    height_local = db_session.query(Block).with_entities(Block.height).order_by(Block.height.desc()).limit(1).scalar() or 0

    if height_local == height_remote:
        time.sleep(5)
        return

    resume_height = height_local + 1

    try:
        new_block = rosetta_get_block(resume_height)["block"]
    except json.decoder.JSONDecodeError as ex:
        logger.error("Rosetta fetch error: {}".format(str(ex)))
        return

    insert_block(new_block, db_session)


def main():
    while True:
        sync()
