import getpass

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

userID: str = input('User ID [postgres]--> ') or "postgres"

password: str = getpass.getpass(prompt=userID + ' password--> ')
host: str = input('hostname [CECS-Postgresql]--> ') or "CECS-Postgresql"
port: str = input('port number [5432]--> ') or "5432"
database: str = input('database [2023FallS01]--> ') or "2023FallS01"

db_url: str = f"postgresql+psycopg2://{userID}:{password}@{host}:{port}/{database}"
db_url_display: str = f"postgresql+psycopg2://{userID}:********@{host}:{port}/{database}"
print("DB URL: " +db_url_display)
engine = create_engine(db_url, pool_size=5, pool_recycle=3600, echo=False)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)