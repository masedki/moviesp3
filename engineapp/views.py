# -*- coding: utf-8 -*-
"""
Created on Sat Jan 19 11:19:07 2019

@author: Nicolas
"""


from flask import Flask, render_template, redirect, request, url_for
import os
import json
import pickle
import pandas

app = Flask(__name__)
app.config["DEBUG"] = True
app.config.from_object('config')

CT_DIR = app.config['BASESAVE']
print(CT_DIR)
def load_obj(name):
    with open(os.path.join(CT_DIR, name), 'rb') as f:
        mon_depickler = pickle.Unpickler(f)
        return mon_depickler.load()

reco_df = load_obj('cluster_list')

def reco_title(nom_film_input):
    dico_reco = {}
    nom_film = nom_film_input+"\xa0"
    num_clust = reco_df[reco_df["movie_title"] == nom_film]["cluster"].values[0]
    groupe = reco_df[reco_df["cluster"] == num_clust].copy()
    masque = groupe["movie_title"] !=nom_film
    reco = groupe[masque].sample(5) #["movie_title"]
    
    
    
    print("Vous avez choisi le film" , nom_film)
    print("Nous vous recommandons aussi :")
    for k in reco.index:
        dico_reco["film id :" + str(reco.loc[k]["movie_id"])] = reco.loc[k]["movie_title"].replace("\xa0","")
    
    return(dico_reco)

def retjson(a):
    python2json = json.dumps(a)
    return python2json


comments = [""]
@app.route('/' , methods=["GET" , "POST"])
def index():
    if request.method == "GET":
        return render_template("movie_main_page.html" , comments = comments )

    a = str(request.form["contents"])
    b = reco_title(a)
    comments[0] = b 
    return retjson(b)
if __name__ == "__main__":
    app.run()
