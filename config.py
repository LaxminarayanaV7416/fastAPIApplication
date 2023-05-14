import os

# ============= SETTINGS FOR BASE APPLICATION TO RUN ============
BASE_DIR = os.path.dirname(os.path.abspath(__name__))
LOG_BASE_PATH = os.path.join(BASE_DIR, 'logs')
STATIC_DIR_PATH = os.path.join(BASE_DIR, 'static')
SQLLITE_DB_PATH = os.path.join(STATIC_DIR_PATH, 'users_sqllite_database.sqlite')
# ===============================================================

# ============= SETTINGS FOR HASH KEYS AND ACTIVITY ============
SECRET_KEY = 'eyJhbGciOiJIUzI1NiJ9.ew0KImVtYWlsIiA6ICJtZWduYS5hbGFtcGFsbGlAdGFsZW50aW5jLmNvbSINCn0'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
# ===============================================================

# ============= SETTINGS FOR DB NEVER CHANGING RUN ============
RIO_DRIVER = "postgresql+psycopg2"
RIO_PORT = 5432
# ===============================================================
