import psycopg 
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg.connect(
        dbname = os.getenv("DB_NAME"),
        user = os.getenv("DB_USER"),
        host = os.getenv("DB_HOST"),
        port = os.getenv("DB_PORT"),
        password = os.getenv("DB_PASSWORD")
    )

def get_db():
    db = get_connection()
    try:
        yield db
    finally:
        db.close()
 
