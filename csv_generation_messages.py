import pandas as pd
import numpy as np
from sqlalchemy import create_engine, types
import os, yaml # credentials:


# Récup des info de connection
with open('config_local.yaml', 'r') as file:
    config = yaml.safe_load(file)
#print(config)

cfg=config['PG']
print(cfg)

# Connection à BDD
url = "{driver}://{user}:{password}@{host}/{database}".format(**cfg)
print('URL', url)
engine = create_engine(url)

df = pd.read_sql("""SELECT username, body FROM "Messages";""", engine)

#print(df)

df.to_csv('messages.csv', index=False)

print('done')
