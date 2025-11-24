from sqlalchemy.orm import sessionmaker
from app.database.settings import engine
from app.utils.logging import log_db


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class DB:
    def __init__(self):
        self.engine = engine
        self.SessionLocal = SessionLocal

    def connect(self):
        try:
            with self.engine.connect() as conn:
                log_db("PostgreSQL connection test successful")
        except Exception as e:
            log_db(f"PostgreSQL connection test failed: {e}")
            raise

    def disconnect(self):
        try:
            self.engine.dispose()
            log_db("Engine disposed")
        except Exception:
            pass

    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()


# global instance
db = DB()
get_db=db.get_db