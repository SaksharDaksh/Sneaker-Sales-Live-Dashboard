import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# --------------------------------------------------------------------
# Local development (MySQL) vs. Deployed (PostgreSQL on Render)
# --------------------------------------------------------------------
# Render automatically injects a DATABASE_URL environment variable
# when you attach a PostgreSQL instance to your web service.
# Locally, that variable won't exist, so we fall back to your MySQL setup.
#
# CHANGE "yourpassword" below to your local MySQL root password.
# --------------------------------------------------------------------

LOCAL_MYSQL_URL = "mysql+pymysql://root:yourpassword@localhost:3306/sales_db"

DATABASE_URL = os.environ.get("DATABASE_URL", LOCAL_MYSQL_URL)

# Render's Postgres URLs start with "postgres://", but SQLAlchemy 2.x
# requires "postgresql://" — this line fixes that automatically.
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,   # checks the connection is alive before using it, reconnects if not
    pool_recycle=280,     # recycles connections every ~4.5 min, before the DB times them out
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
