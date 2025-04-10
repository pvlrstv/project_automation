import os
import pandas as pd
import random
from datetime import datetime
import configparser
import uuid

dirname = os.path.dirname(__file__)

data_dir = os.path.join(dirname, 'data')
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

config = configparser.ConfigParser()
config.read(os.path.join(dirname, 'config.ini'))

goods = []

for section in config.sections():
    if section not in ['Shops', 'Cash desks', 'Database']:
        for good in list(config[section]):
            goods.append((section, good))
            
            
if 0 <= datetime.today().weekday() <= 5:
    
    shops = list(range(1, int(config['Shops']['SHOPS_CNT'])+1))
    cashdesks = int(config['Cash desks']['CASHDESKS_CNT'])
    
    for shop in shops:
        for cashdesk in range(1, random.randint(2, cashdesks+1)):
            
            d = {
                'doc_id': [],
                'item': [],
                'category': [],
                'amount': [],
                'price': [],
                'discount': []
            }
            
            for check in range(10, random.randint(20, 100)):
                
                doc_id = uuid.uuid4().hex
                
                random.shuffle(goods)                
                for good in goods[:random.randint(1, 6)]:                    
                    d['doc_id'].append(doc_id)
                    d['item'].append(good[1])
                    d['category'].append(good[0])
                    d['amount'].append(random.randint(1, 5))
                    d['price'].append(random.randint(50, 1000))
                    d['discount'].append(random.randint(0, 15))
                    
            df = pd.DataFrame(d)
            df.to_csv(os.path.join(data_dir, f'{shop}_{cashdesk}.csv'), index=False)