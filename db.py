from sqlmodel import SQLModel, Session, create_engine

# SQLite database file in the current folder
engine = create_engine("sqlite:///database.db", echo=False)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session() -> Session:
    return Session(engine)
