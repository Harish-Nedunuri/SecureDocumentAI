import sqlite3
from pydantic import BaseModel
from typing import List
from datetime import datetime
import os
from ragcore.SupportUtils.audit.logging import logger as Logger


# Function to create a database connection
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        Logger.info(f"SQLite version: {sqlite3.version}")
    except sqlite3.Error as e:
        Logger.info(e)
    return conn

# Function to create table
def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        Logger.info(e)

# Generic function to insert values into any table
def insert_table_values(conn, values, table_schema):
    table_name = table_schema.__name__.lower()
    columns = ', '.join([field for field in table_schema.__fields__])
    placeholders = ', '.join(['?' for _ in table_schema.__fields__])
   
    sql = f''' INSERT INTO {table_name}({columns})
               VALUES({placeholders}) '''
    
    cur = conn.cursor()
    cur.execute(sql, tuple(values.values()))
    conn.commit()
    return cur.lastrowid

# Function to read data from a table
def read_table(conn, sql):
    
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    
    return rows
