from sqlalchemy import create_engine

DATABASE_URL = "sqlite:///database/app.db"

engine = create_engine(DATABASE_URL)