import sqlite3
from config import DATABASE
from flask import request


def connect_to_db():
    conn = sqlite3.connect(DATABASE)
    return conn


def get_resources():
    """
    Returns annual resource data based on the api well number.
    """
    connect = connect_to_db()
    result = {}
    well = request.args.get('well')
    connect.row_factory = sqlite3.Row
    cursor = connect.cursor()
    cursor.execute(
        '''SELECT * FROM annual_production WHERE api_well_number = ?''',
        (well,)
        )
    data = cursor.fetchone()
    if data:
        result["oil"] = data['oil']
        result["brine"] = data['brine']
        result["gas"] = data['gas']
    connect.close()
    return result
