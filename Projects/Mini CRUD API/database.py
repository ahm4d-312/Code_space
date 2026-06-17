from dotenv import load_dotenv
from os import getenv
from contextlib import closing
import sqlite3
import logging

#.env variablse
load_dotenv()
DB_file=getenv('DB_file')

def init_db():
    #check if the tables exists
    with closing(sqlite3.connect(DB_file)) as db_conn:
        with db_conn:
            pass
        #some queries here...
    pass

def create_lab():
    with closing(sqlite3.connect(DB_file)) as db_conn:
        with db_conn:
            pass
        #some queries here...
    pass

def get_all_labs():
    with closing(sqlite3.connect(DB_file)) as db_conn:
        with db_conn:
            pass
        #some queries here...
    pass

def get_lab():
    with closing(sqlite3.connect(DB_file)) as db_conn:
        with db_conn:
            pass
        #some queries here...
    pass

def update_lab():
    with closing(sqlite3.connect(DB_file)) as db_conn:
        with db_conn:
            pass
        #some queries here...
    pass

def delete_lab():
    with closing(sqlite3.connect(DB_file)) as db_conn:
        with db_conn:
            pass
        #some queries here...
    pass

def execute_query():
    with closing(sqlite3.connect(DB_file)) as db_conn:
        with db_conn:
            pass
        #some queries here...
    pass

def validate_exists():
    with closing(sqlite3.connect(DB_file)) as db_conn:
        with db_conn:
            pass
        #some queries here...
    pass

if __name__=='__main__':
    raise RuntimeError("This is a module and should not be ran directly!!")

