# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 17:53:21 2023

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
Postgres_engine = create_engine(config['postgres']['url'])


def traitement(msg, parent_id=None):
    '''
    Effectue un traitement sur l'obj passé (Message)
    :param msg: Message
    :return:
    '''
    username = msg['username'] if 'username' in msg else None
    dt = msg['created_at']
    dt = dt[:10]+' '+dt[11:19]
    # print("Recurse ", msg['id'], msg['depth'] if 'depth' in msg else '-', parent_id, dt)

    if not msg['anonymous']:
        Postgres_engine.execute("""INSERT INTO "public"."User"  (username, user_id) VALUES (%s,%s) ON CONFLICT DO NOTHING;""", [msg['username'], msg['user_id']])
    
    # Postgres_engine.execute("""INSERT INTO Messages 
    #                     (id, type, created_at, username, depth, body, parent_id) 
    #                     VALUES (%s,%s,%s,%s,%s,%s,%s)
    #                     ON CONFLICT DO UPDATE SET parent_id=VALUES(parent_id), depth=VALUES(depth);""",
    #                     [msg['id'], msg['type'], dt, username, msg['depth'] if 'depth' in msg else None, msg['body'], parent_id])
    
    Postgres_engine.execute("""INSERT INTO Message 
                        (id, type, created_at, username, depth, body, parent_id) 
                        VALUES (%s,%s,%s,%s,%s,%s,%s)
                        ON CONFLICT DO NOTHING;""",
                        [msg['id'], msg['type'], dt, username, msg['depth'] if 'depth' in msg else None, msg['body'], parent_id])

def extract_document_mongo_forum_collecton_to_postgress_data(semple=None):
    '''
    Effectue l'extraction de documments mongo et les transfère sous formr de données vers postgres'
    :param semple: spécifie un nombre de documents à extraire, dans l'ordre d'apparition
        si None tous les documents sont extraits
    :return:
    '''

    #extractions des documents mongo
    if semple is None:
        cursor = forum.find(filter=None, projection={'annotated_content_info': 0, '_id': 1})
    else:
        cursor = forum.find(filter=None, projection={'annotated_content_info': 0, '_id': 1}).limit(semple)
    
    k=0
    
    #insetion des données dans la base
    for doc in cursor:
     
        if k%1000 == 0:
            print(k)
        k+=1
        #print(json.dumps(doc, indent=4))
        
        extract_document_mongo_user_collecton_to_postgress_data({'username':doc['content']['username']})
        
        #insersion table course
        # Postgres_engine.execute("INSERT INTO PUBLIC.course (course_id) VALUES (%s) ON CONFLICT DO NOTHING;", [doc['content']['course_id']])
        
        #insersion table User
        # Postgres_engine.execute("""INSERT INTO "public"."User" ("username", "user_id") VALUES (%s,%s) ON CONFLICT DO NOTHING;""", [doc['content']['username'], doc['content']['user_id']])
    
        #insersion table Treads
        Postgres_engine.execute("""INSERT INTO "public"."Threads" ("_id", "title","course_id","username") VALUES (%s,%s,%s,%s) ON CONFLICT DO NOTHING;""", [doc['_id'], doc['content']['title'], doc['content']['course_id'], doc['content']['username']])
    
        #insersion récursive table message
        utils.recur_message(doc['content'], traitement)

            
def extract_document_mongo_user_collecton_to_postgress_data(filter_={},semple=None):
    start_time = time.time()

    if semple is None:
        cursor = user.find(filter=filter_)
    else:
        cursor = user.find(filter=filter_).limit(semple)
    
    k=0
    for doc in cursor:
        # print(doc['_id'])
        # print(doc['id'])
        
        start_time_op = time.time()
        
        Postgres_engine.execute("""INSERT INTO "public"."User" ("_id", "username", "user_id") VALUES (%s,%s,%s) ON CONFLICT DO NOTHING;""", 
                                                                [str(doc['_id']),
                                                                 doc['username'],
                                                                 doc['id'] if 'id' in doc else None
                                                                 ])

        for sub_doc in doc:
            try:
                if sub_doc != '_id' and sub_doc != 'id' and sub_doc != 'username':
                    # print('table course:' + sub_doc)
                    Postgres_engine.execute("INSERT INTO PUBLIC.course (course_id) VALUES (%s) ON CONFLICT DO NOTHING;", [sub_doc])
                    Postgres_engine.execute("""INSERT INTO "public"."Result" ("course_id","username", "grade", "certificate_delivered", "certificate_eligible","certificate_type") VALUES (%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING;""", 
                                                                            [sub_doc,
                                                                             doc['username'], 
                                                                             doc[sub_doc]['grade'] if 'grade' in doc[sub_doc] else None,
                                                                             doc[sub_doc]['Certificate Delivered'] if 'Certificate Delivered' in doc[sub_doc] else None,
                                                                             doc[sub_doc]['Certificate Eligible'] if 'Certificate Eligible' in doc[sub_doc] else None,
                                                                             doc[sub_doc]['Certificate Type'] if 'Certificate Type' in doc[sub_doc] else None
                                                                             ])
                    pass
            except:
                print("----------------------------------------------------------------------")  
                print(f"error extract_document_mongo_user_collecton_to_postgress_data --> {sub_doc}  !!!!")  
                print("----------------------------------------------------------------------")   
            
        
        k+=1
        
        if k%1 == 0:
            print(k,
                  "  -Temps d'exécution courent: {:.1f} secondes".format(time.time() - start_time),
                  "  -Temps d'exécution operation: {:.1f} secondes".format(time.time() - start_time_op))
            
def main():
    extract_document_mongo_forum_collecton_to_postgress_data(1)
    
    # extract_document_mongo_user_collecton_to_postgress_data()


main()


