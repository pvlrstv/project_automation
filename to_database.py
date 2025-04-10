import configparser
import os
import glob
import pandas as pd

from pgdb import PGDatabase


dirname = os.path.dirname(__file__)
data_dir = os.path.join(dirname, 'data')

config = configparser.ConfigParser()
config.read(os.path.join(dirname, 'config.ini'))


DATABASE_CREDS = config['Database']

database = PGDatabase(
    host=DATABASE_CREDS['HOST'],
    database=DATABASE_CREDS['DATABASE'],
    user=DATABASE_CREDS['USER'],
    password=DATABASE_CREDS['PASSWORD'],
)


shops = list(range(1, int(config['Shops']['SHOPS_CNT'])+1))
cashdesks = list(range(1, int(config['Cash desks']['CASHDESKS_CNT'])+1))

files = []

for shop in shops:
    for cashdesk in cashdesks:
        filename = f'{shop}_{cashdesk}.csv'
        matching_file = glob.glob(os.path.join(data_dir, filename))

        if matching_file:
            files.extend(matching_file)
            
for file in files:
    df = pd.read_csv(os.path.join(data_dir, file))
    for i, row in df.iterrows():
        query = """
            INSERT INTO purchases (doc_id, item, category, amount, price, discount)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        args = (
            row['doc_id'],
            row['item'],
            row['category'],
            row['amount'],
            row['price'],
            row['discount']
        )
        database.post(query, args)