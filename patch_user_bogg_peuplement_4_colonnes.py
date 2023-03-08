# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 18:02:39 2023

@author: Utilisateur
"""

import json, utils, yaml
from pymongo import MongoClient
from sqlalchemy import create_engine
import time,sys

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


result = Postgres_engine.execute("""select users."username" as id from users""")

for _id in result:
    
    
    doc = user.find_one(filter={'username': _id[0]})
    # doc = user.find_one(filter={'username': 'Osiatis_FUN'})
    print(_id[0])
    # print(doc)

    # sys.exit()
    
    k=0
    for sub_doc in doc:
       
        k=1
        if k%100 == 0:
            print(k)
        # print(sub_doc)
        
        if sub_doc != '_id' and sub_doc != 'id' and sub_doc != 'username':
            
            
            Postgres_engine.execute("""INSERT INTO "public"."users" ("username", "user_id","level_education","gender","year_of_burth","country") VALUES (%s,%s,%s,%s,%s,%s ) ON CONFLICT DO NOTHING;""", 
                                                                    [str(doc['_id']),
                                                                     doc['id'] if 'id' in doc else None,
                                                                     doc[sub_doc]['level_education'] if 'level_education' in doc else None,
                                                                     doc[sub_doc]['gender'] if 'gender' in doc else None,
                                                                     doc[sub_doc]['year_of_burth'] if 'year_of_burth' in doc else None,
                                                                     doc[sub_doc]['country'] if 'country' in doc else None
                                                                     ])
            
            
        
            # query = """
            #             UPDATE "public"."users"
            #               SET "level_education" = %s,
            #                   "gender" = %s,
            #                   "year_of_burth" = %s,
            #                   "country" = %s
            #               WHERE "username" = %s;
            #         """
            
            # try:
            #     if doc[sub_doc]['year_of_birth'] != None:
            #         new_year_of_burth = int(doc[sub_doc]['year_of_birth'])
            #     else:
            #         new_year_of_burth=-1
            # except:
            #     new_year_of_burth=0
                
            # try:
            #     if doc[sub_doc]['gender'] != None:
            #         new_gender = doc[sub_doc]['gender']
            #     else:
            #         new_gender='N/A'
            # except:
            #     new_gender='None'
                
            # try:
            #     if doc[sub_doc]['level_education'] != None:
            #         new_level_education = doc[sub_doc]['level_education']
            #     else:
            #         new_level_education='N/A'
            # except:
            #     new_level_education='None'
                
            # try:
            #     if doc[sub_doc]['country'] != None:
            #         new_country = doc[sub_doc]['country']
            #     else:
            #         new_country='N/A'
            # except:
            #     new_country='None'
                
            # # print(new_country) #if 'level_education' in doc else None
          
            # record_id =  str(doc['_id'])
 
            # Postgres_engine.execute(query, (new_level_education, new_gender, new_year_of_burth, new_country, record_id))
     