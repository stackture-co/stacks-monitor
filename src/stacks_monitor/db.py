from aparat import assert_env_vars
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

[db_uri, db_pool_size] = assert_env_vars('DB_URI', 'DB_POOL_SIZE')

db_engine = create_engine(db_uri, pool_size=int(db_pool_size))

session_args = {'autocommit': False, 'autoflush': False}

session_maker = sessionmaker(bind=db_engine, **session_args)
