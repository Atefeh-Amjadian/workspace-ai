from app.db.base import Base
from app.db.session import engine
from app.models.email import Email 

def init_db():
    Base.metadata.create_all(bind=engine)