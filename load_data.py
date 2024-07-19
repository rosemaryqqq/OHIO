import sqlite3
import argparse
import pandas as pd


def get_excel_data(file_path):
    """
    Reads an Excel file containing well data and returns a DataFrame
    with the annual totals of oil, gas, and brine for each well.
    """
    df = pd.read_excel(file_path)
    annual_data = df.groupby('API WELL  NUMBER')[['OIL', 'GAS', 'BRINE']].sum()
    annual_data = annual_data.reset_index()
    return annual_data


def load_data(annual_data):
    """
    Loads annual production data into an SQLite database.
    """
    conn = sqlite3.connect(args.db)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS annual_production (
            api_well_number TEXT,
            oil INTEGER,
            gas INTEGER,
            brine INTEGER
        )
        ''')
    conn.commit()
    data = list(annual_data.itertuples(index=False, name=None))
    sql = '''
        INSERT INTO annual_production (api_well_number, oil, gas, brine)
        VALUES (?, ?, ?, ?)
        '''
    cur.executemany(sql, data)
    conn.commit()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--db")
    parser.add_argument("-f", "--file_path")
    args = parser.parse_args()
    annual_data = get_excel_data(args.file_path)
    load_data(annual_data)
