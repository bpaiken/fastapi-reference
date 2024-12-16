import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData

load_dotenv()

database_url = os.environ.get("DATABASE_URL")

# Database connection parameters
DATABASE_URL = "postgresql+psycopg://postgres:postgres@localhost:6024/RecruitIQ"

# Create an engine and connect to the database
engine = create_engine(DATABASE_URL)

# Reflect the existing database into a new MetaData object
meta = MetaData()
meta.reflect(bind=engine)

# Drop all tables
meta.drop_all(bind=engine)

print("All tables have been dropped.")
