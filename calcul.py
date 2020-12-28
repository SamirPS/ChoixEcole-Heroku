#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 19:41:49 2018
@author: samir
"""

import sqlite3
connexion = sqlite3.connect("db/choixecole.db")
curseur = connexion.cursor()


def renvoie_admission():

    return [
        resultat[0]
        for resultat in curseur.execute("SELECT DISTINCT Admission FROM EcoleS")
    ]


def renvoie_specialites():
    return [
        resultat[0]
        for resultat in curseur.execute("SELECT DISTINCT NomSpe FROM Specialite")
    ]


def renvoie_regions():
    return [
        resultat[0]
        for resultat in curseur.execute("SELECT DISTINCT Region FROM EcoleS")
    ]


def prix_ecole(ecoles, filtre):
    prix = 0
    groupe=[]
    for i in ecoles:
        curseur.execute("SELECT Groupe FROM EcoleS WHERE Acronyme=? ",(i,))
        for resultat in curseur.fetchall():
            groupe.append(resultat[0])
            
    for i in list(set(groupe)):
        curseur.execute(f"SELECT  {filtre} FROM Coefficient WHERE Groupe=?",(i,))
        for resultat in curseur.fetchall():
            prix += resultat[0]

    return prix

def getinfo(ecole):
    L=[]
    for i in ecole:
        curseur.execute("SELECT * FROM EcoleS WHERE Acronyme=? ",(i,))
        for resultat in curseur.fetchall():
            L.append(resultat)
            break
    return L

def renvoie_idspe(choix):
    
    return tuple(
        spe[0]
        for i in tuple(choix)
        for spe in curseur.execute(
            "SELECT idspecialite FROM specialite WHERE nomspe=?",(i,)
        )
    )


def creationtuple(liste):
    if len(liste) == 1:
        return f"('{liste[0]}')"
   
    return tuple(liste)


def filtre(choix_utilisateur, notes):
    conds = []

    """Le none correspond au fait que l'utilisateur n'as rien choisi"""
    if choix_utilisateur["specialites"] != None:
        conds.append(["Idspe", "IN", choix_utilisateur["specialites"]])
    if choix_utilisateur["alternance"] != None:
        conds.append(["Alternance", "IN", choix_utilisateur["alternance"]])
    if choix_utilisateur["concours"] != None:
        conds.append(["Admission", "IN", choix_utilisateur["concours"]])
    if choix_utilisateur["regions"] != None:
        conds.append(["Region", "IN", choix_utilisateur["regions"]])

    if choix_utilisateur["annee"] == ("3/2",):
        bonif_str = "Bonification"
    else:
        bonif_str = "0"

    requete = (
        f"""
        SELECT DISTINCT id,Nom,Admission,Commune,Alternance,Acronyme,NomSpe
        FROM EcoleSpe
        JOIN EcoleS on EcoleSpe.IdEcole=EcoleS.id
        JOIN Specialite on EcoleSpe.IdSpe=Specialite.idspecialite
        JOIN Coefficient on Coefficient.Groupe=EcoleS.Groupe
        WHERE {notes["maths"]}*Maths+
        {notes["physique"]}*Physique+
        {notes["si"]}*SI+
        {notes["informatique"]}*Informatique+
        {notes["anglais"]}*Anglais+
        {notes["francais"]}*Francais+
        {notes["modelisation"]}*Modelisation+
        {bonif_str} >= Points """
    )
    
    for var in conds:
        requete += f" AND {var[0]} {var[1]}  {creationtuple(var[2])}"


    return [ecole for ecole in curseur.execute(requete)]
