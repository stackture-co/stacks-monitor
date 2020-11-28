from sqlalchemy import (Column, String, Integer, BigInteger, JSON, Numeric, UniqueConstraint, ARRAY)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

__all__ = ["Base", "Block", "Transaction", "CurrencyRate"]


class Block(Base):
    __tablename__ = 'blocks'

    height = Column('height', Integer, nullable=False, primary_key=True)

    hash = Column('hash', String, nullable=False)

    parent_block_hash = Column('parent_block_hash', String, nullable=False, unique=True)

    txs = Column('txs', ARRAY(String), nullable=False)

    burn_block_time = Column('burn_block_time', BigInteger, nullable=False)


UniqueConstraint(Block.parent_block_hash, name='uix_blocks_parent_block_hash')


class Transaction(Base):
    __tablename__ = 'transactions'

    hash = Column('hash', String, nullable=False, primary_key=True)

    block_height = Column('block_height', Integer, nullable=False)

    raw = Column('raw', JSON, nullable=False)


class CurrencyRate(Base):
    __tablename__ = 'currency_rates'

    id = Column('id', Integer, nullable=False, primary_key=True)

    block_height = Column('block_height', Integer, nullable=False)

    pair = Column('pair', String, nullable=False)

    rate = Column('rate', Numeric, nullable=False)
