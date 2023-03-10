from flask import Flask, redirect, url_for, request, render_template
# import plotly
# import plotly.express as px
# import pandas as pd
# import json
# from sqlalchemy import create_engine

import analyses

app = Flask(__name__)

# choix du graph
@app.route('/graph' ,methods = ['POST', 'GET'])
def graph():
    if request.method == 'POST':
       result = request.form
       print(result['form'])  
       if result['form']=="Analyse 1":
           return render_template('notdash.html', 
                                  graphJSON=analyses.nb_threads_by_courses(), 
                                  title="Nombre de threads par cours classés par la moyenne de méssages par threads.")
       elif result['form']=="Analyse 2":
           return render_template('notdash.html', 
                                  graphJSON=analyses.nb_cours_grade_vs_tt_cours(), 
                                  title="Nombre de cours ayant des grades vs tous les cours présents dans les threads.")
       elif result['form']=="Analyse 3":
           return render_template('notdash.html', 
                                  graphJSON=analyses.percentage_reussite_by_courses(), 
                                  title="Pourcentage de réussite par cours.")
       elif result['form']=="Analyse 4":
           return render_template('notdash.html', 
                                  graphJSON=analyses.diagrame_tri_varie(), 
                                  title="Moyenne thread et grade, délivrance de certification par cours.")
      

# page de choix entre les analyses et le machine learning
@app.route('/analyse' ,methods = ['POST', 'GET'])
def analyse():
   if request.method == 'POST':
      result = request.form
      print(result['form'])
      if result['form']=='analyse': 
          return render_template("analyse.html")
      elif result['form']=='ml':
          return render_template("ml.html")
      elif result['form']=="<<<":
          return render_template("analyse.html")
      
# page d'acceuil
@app.route('/', methods = ['POST', 'GET'])
def index():
    return render_template("index.html")
 
if __name__ == '__main__':
   app.run(debug = True)