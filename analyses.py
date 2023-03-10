#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 15:26:37 2023

@author: arscg
"""

import plotly
import plotly.express as px
import pandas as pd
import json
from sqlalchemy import create_engine
# import psycopg2


 
def nb_threads_by_courses():   
    connection = create_engine('postgresql+psycopg2://postgres:greta2023@localhost:5432/mooc_g6_v3')
    result = connection.execute("""select * from vue_stats_resultats_all_with_thread order by avg_message_by_tread desc""")
    
    df = pd.DataFrame(result, columns=['course', 'nb_thread', 'avg_message_by_thread', 
                                       'perc_deliv', 'not_deliv', 'deliv', 'deliv_is_null', 
                                       'avg_grade', 'nb_aprenants', 'nb_aprenants_sur_0_5', 
                                       'nb_aprenants_sur_0_6'])
    fig = px.bar(df, x='course', y='nb_thread', color='avg_message_by_thread', 
           barmode='group')
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def nb_cours_grade_vs_tt_cours():   
    connection = create_engine('postgresql+psycopg2://postgres:greta2023@localhost:5432/mooc_g6_v3')
    result = connection.execute("""select 'nb_course_threads_liée_a_des_grades',count(*) from vue_stats_resultats_all_with_thread
                                        union
                                    select 'nb_cource_threads', count(*) from vue_stats_treads""")
    
    df = pd.DataFrame(result, columns=['colonne', 'comptage'])
    fig = px.bar(df, x='colonne', y='comptage', color='colonne', 
           barmode='group')
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def percentage_reussite_by_courses():   
    connection = create_engine('postgresql+psycopg2://postgres:greta2023@localhost:5432/mooc_g6_v3')
    result = connection.execute("""select * 
                                    from vue_stats_resultats_all_with_thread vsrawt 
                                    order by perc_deliv desc""")
    
    df = pd.DataFrame(result, columns=['course', 'nb_thread', 'avg_message_by_thread', 
                                       'perc_deliv', 'not_deliv', 'deliv', 'deliv_is_null', 
                                       'avg_grade', 'nb_aprenants', 'nb_aprenants_sur_0_5', 
                                       'nb_aprenants_sur_0_6'])
    fig = px.bar(df, x='course', y='perc_deliv', barmode='group')
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def diagrame_tri_varie():   
    connection = create_engine('postgresql+psycopg2://postgres:greta2023@localhost:5432/mooc_g6_v3')
    result = connection.execute("""select * 
                                    from vue_stats_resultats_all_with_thread vsrawt 
                                """)
    
    df = pd.DataFrame(result, columns=['course', 'nb_thread', 'avg_message_by_thread', 
                                       'perc_deliv', 'not_deliv', 'deliv', 'deliv_is_null', 
                                       'avg_grade', 'nb_aprenants', 'nb_aprenants_sur_0_5', 
                                       'nb_aprenants_sur_0_6'])
    # fig = px.bar(df, x='course', y='perc_deliv', barmode='group')
    # df = px.data.iris()
  
    fig = px.scatter_3d(df, x = 'avg_grade', 
                        y = 'avg_message_by_thread', 
                        z = 'perc_deliv',
                        color = 'course')
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
