# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 21:13:20 2023

@author: Utilisateur
"""

import json, utils, yaml
from pymongo import MongoClient
from sqlalchemy import create_engine
import time,sys
import pandas as pd
import plotly.express as px

#ouverture du fichier de configuration
with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)

#connection à la base postgres
Postgres_engine = create_engine(config['postgres_mooc_v2_local']['url'])


result = Postgres_engine.execute("""select * from public.vue_stats_resultats_all_with_thread""")

df = pd.DataFrame(result, columns=['col1', 'col2', 'col3', 'col4', 'col5', 'col6', 'col7', 'col8', 'col9', 'col10', 'col11'])

fig = px.scatter(df, x='col2', y='col3', color='col4')
fig.show()

