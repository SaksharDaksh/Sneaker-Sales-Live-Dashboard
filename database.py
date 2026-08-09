from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# CHANGE "yourpassword" to whatever root password you set in MySQL Workbench
# Format: mysql+pymysql://username:password@host:port/database_name
DATABASE_URL = "mysql+pymysql://root:Ohara2099@localhost:3306/sales_db"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,   # checks the connection is alive before using it, reconnects if not
    pool_recycle=280,     # recycles connections every ~4.5 min, before MySQL times them out
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """
    This function gives each API request its own database connection,
    and closes it automatically when the request is done.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
