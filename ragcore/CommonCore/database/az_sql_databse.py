from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Generator
from ragcore.CommonCore.secret_utils.config import get_settings
from ragcore.CommonCore.audit.logging import logger
from sqlalchemy import create_engine, Column, Integer, String, DateTime,Float
from sqlalchemy.orm import class_mapper
from sqlalchemy.exc import IntegrityError
import shutil

Base = declarative_base()
settings = get_settings()
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=5,
    max_overflow=0
)   
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine) 
def get_db() -> Generator:
    """ This function returns a database session for database within GACdocAI resource group"""
    db = Session()
    try:
        yield db
    finally:
        db.close()

class DocumentRegister(Base):
    __tablename__ = 'documentregister'
    
    document_id = Column(String, primary_key=True)
    num_of_pages = Column(Integer, nullable=False)
    file_size = Column(Integer, nullable=False)
    file_name = Column(String, nullable=False, unique=True)
    document_path_uri = Column(String, nullable=False)
    content_type = Column(String)
    creation_time = Column(DateTime)
    last_modified = Column(DateTime)
    register_time = Column(DateTime, nullable=False)
    embeddings_status = Column(Integer, nullable=False)
    document_summary = Column(String, nullable=True)

class PageRegister(Base):
    __tablename__ = 'pageregister'
    
    page_id = Column(String, primary_key=True)
    document_id = Column(String, nullable=False)
    page_number = Column(Integer, nullable=False)    
    file_name = Column(String, nullable=False, unique=True)
    document_path_uri = Column(String, nullable=False)
    page_path_uri = Column(String, nullable=False)  
    page_register_time = Column(DateTime, nullable=False)
    page_type = Column(String, nullable=True)
    classifier_confidence = Column(Float, nullable=True) 
    extraction_status = Column(Integer, nullable=False)
    page_summary = Column(String, nullable=True)

class TagRegister(Base):
    __tablename__ = 'tagregister'
    
    tag_id = Column(String(255), primary_key=True)
    page_id = Column(String(255), nullable=False)
    document_id = Column(String(255), nullable=False)
    tag_value = Column(String(255), nullable=False)
    tag_page_num = Column(Integer, nullable=False)
    file_name = Column(String(255), nullable=False)
    document_path_uri = Column(String, nullable=False)  # NVARCHAR(MAX) maps to String in SQLAlchemy
    marked_image = Column(String, nullable=False)  # NVARCHAR(MAX) maps to String in SQLAlchemy
    register_time = Column(DateTime, nullable=False)
    asset_type = Column(String(255))
    asset_name = Column(String(255))

class AssetLookup(Base):
    __tablename__ = 'assetlookup'
    
    asset_type = Column(String(255), primary_key=True)
    regex = Column(String(255))


def query_to_dict(obj, fields=None):
    """Converts a SQLAlchemy model instance to a dictionary, including only the specified fields."""
    if fields:
        return {field: getattr(obj, field) for field in fields if hasattr(obj, field)}
    return {c.key: getattr(obj, c.key) for c in class_mapper(obj.__class__).columns}

def commit_data_and_rmv_temp_dir(dbs,temp_dir=None):
    try:
        dbs.commit()
    except IntegrityError as e:
        dbs.rollback()
        logger.error(f"IntegrityError: {e}")
    except Exception as e:
        dbs.rollback()
        logger.error(f"Exception during commit: {e}")
    if temp_dir:
        shutil.rmtree(temp_dir)
        logger.info(f"Temporary directory deleted: {temp_dir}")

 
