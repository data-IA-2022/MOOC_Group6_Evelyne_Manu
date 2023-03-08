# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 18:02:39 2023

@author: Utilisateur
"""

import json, utils, yaml
from pymongo import MongoClient
from sqlalchemy import create_engine
import time

#ouverture du fichier de configuration
with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)

#connection à la base mongo
client = MongoClient(config['mongo']['url'])

#Liens vers les collections
forum = client[config['mongo']['database']].forum
user = client[config['mongo']['database']].user

#connection à la base postgres
Postgres_engine = create_engine(config['postgres_mooc_v2_local']['url'])


result = Postgres_engine.execute("""select users."_id" as id from users""")

for _id in result:
    print(_id)
    
    doc = user.find_one(filter=None, projection={'annotated_content_info': 0, '_id': 1})
  
    
    
    for sub_doc in doc:
        if sub_doc != '_id' and sub_doc != 'id' and sub_doc != 'username':
            print(sub_doc)
    #     
            
    #         # Postgres_engine.execute("""INSERT INTO "public"."User" ("_id", "username", "user_id","level_education","gender","year_of_burth","country") VALUES (%s,%s,%s,%s,%s,%s,%s ) ON CONFLICT DO NOTHING;""", 
    #         #                                                         [str(doc['_id']),
    #         #                                                          doc['username'],
    #         #                                                          doc['id'] if 'id' in doc else None,
    #         #                                                          doc['level_education'] if 'level_education' in doc else None,
    #         #                                                          doc['gender'] if 'gender' in doc else None,
    #         #                                                          doc['year_of_burth'] if 'year_of_burth' in doc else None,
    #         #                                                          doc['country'] if 'country' in doc else None
    #         #                                                          ])
    #         pass