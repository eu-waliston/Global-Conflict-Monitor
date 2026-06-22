import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()


def get_engine():
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST')
    database = os.getenv('DB_NAME')

    connection_string = (
        f'mysql+mysqlconnector://{user}:{password}@{host}/{database}'
    )

    return create_engine(connection_string)

def get_server_engine():

    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST')

    connection_string = (
        f'mysql+mysqlconnector://'
        f'{user}:{password}@{host}'
    )

    return create_engine(connection_string)