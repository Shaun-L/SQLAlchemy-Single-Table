from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import MetaData


Base = declarative_base(metadata=MetaData(schema=(input('Schema name [introduction]-->') or "introduction")))
metadata = Base.metadata