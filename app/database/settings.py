from sqlalchemy import create_engine, event
from sqlalchemy.orm import declarative_base
from urllib.parse import quote_plus
import os
from app.utils.logging import log_db, log_error
from dotenv import load_dotenv


load_dotenv()

class DatabaseConfig:
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASS = quote_plus(os.getenv("DB_PASS", "Yogi@gag2580"))
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "einsurance")


    DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


# Create engine and Base
try:
    engine = create_engine(DatabaseConfig.DATABASE_URL, echo=False, pool_pre_ping=True)
    Base = declarative_base()
    log_db("Database engine created")
except Exception as e:
    log_error(f"Database engine creation failed: {e}")
    raise


# SQL event listeners to log SQL statements and timing
@event.listens_for(engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    context._query_start_time = perf_counter_start = None
    try:
    # store start time on context
        from time import perf_counter
        context._query_start_time = perf_counter()
        log_db(f"Executing SQL: {statement} | Params: {parameters}")
    except Exception:
        pass


@event.listens_for(engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    try:
        from time import perf_counter
        if hasattr(context, "_query_start_time") and context._query_start_time:
            total_ms = (perf_counter() - context._query_start_time) * 1000
            log_db(f"Query executed in {total_ms:.2f} ms")
    except Exception:
        pass