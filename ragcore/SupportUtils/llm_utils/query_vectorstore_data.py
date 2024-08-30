import sqlite3
from ragcore.SupportUtils.audit.logging import logger


# Function to count the rows with the given string_value
def executor_func(string_value,cursor,query):
    cursor.execute(query, (f"%{string_value}%",))
    result = cursor.fetchone()
   
    return result[0]


# Function to list all tables in the database
def list_tables(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    return tables
# Function to list all the id's with the given string_value
def list_ids(string_value,cursor,query):
    cursor.execute(query, (f"%{string_value}%",))
    ids = cursor.fetchall()
    ids = [id[0] for id in ids]
    return ids
# Function to list all the page values
def list_pages(string_value,cursor,query):
    cursor.execute(query, (f"%{string_value}%",))
    pages = cursor.fetchall()
    pages = [page[0] for page in pages]
    return pages

# Function to inspect a specific table structure
def inspect_table(table_name,cursor):
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()
    return columns

def get_embedding_chunks(file_name,chroma_filepath):
   
    conn = sqlite3.connect(chroma_filepath)

    cursor = conn.cursor()

    # Query to count columns with key == "id" and string_value matches another string input
    count_query = """
    SELECT COUNT(*)
    FROM embedding_metadata
    WHERE key = 'id' AND string_value LIKE ?
    """
    # List all tables
    tables = list_tables(cursor)    
    
    # If 'embedding_metadata' exists, inspect its structure
    table_to_inspect = 'embedding_metadata'
    id_list_query = """
            SELECT string_value
            FROM embedding_metadata
            WHERE key = 'source' AND string_value LIKE ?
            """
    page_list_query = """
        SELECT int_value
        FROM embedding_metadata
        WHERE key = 'page' AND string_value LIKE ?
        """

    # Example usage
    
    count = executor_func(file_name,cursor,count_query)
    idlist = list_ids(file_name,cursor,id_list_query)
    page_list = list_pages(file_name,cursor,page_list_query)
    logger.info(f"The count of rows where key='id' and string_value='{file_name}' is: {count}")


    # Close the connection
    conn.close()
    return count,idlist,page_list