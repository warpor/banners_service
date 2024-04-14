import os

from dotenv import load_dotenv

load_dotenv(".env")

ENCRYPT_KEY = os.environ.get("ENCRYPT_KEY")
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")

DB = os.environ.get("DB")
DB_ENGINE = os.environ.get("DB_ENGINE")
DB_NAME = os.environ.get("POSTGRES_DB")
DB_LOGIN = os.environ.get("POSTGRES_USER")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
SQLALCHEMY_DATABASE_URL \
    = f"{DB}+{DB_ENGINE}://{DB_LOGIN}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

REDIS_URI = os.environ.get("REDIS_URI")
REDIS_PORT = os.environ.get("REDIS_PORT")
REDIS_URL \
    = f"{REDIS_URI}:{REDIS_PORT}"

