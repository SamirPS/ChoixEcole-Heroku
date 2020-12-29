from flask import Flask,Blueprint, session, redirect, url_for, request,render_template
import calcul

bp = Blueprint('main', __name__)


@bp.route('/', methods=['GET'])
def accueil():
    special = calcul.renvoie_specialites()
    region = calcul.renvoie_regions()
    return render_template('index.html', special=special,region=region,lens=len(special)+2,lenr=len(region)+2)


@bp.route('/ecole', methods=['POST'])
def my_form_post():
    
    #Get data of listbox
    specialites = request.form.getlist('specialite')
    alternance = request.form.getlist('alternance')
    concours = None
    regions = request.form.getlist('region')
    annee = request.form.getlist('annee')
    ef=request.form.getlist('typec')
     
  
    specialites =calcul.renvoie_idspe(specialites)
    
    #Check list vide
    if specialites==[]:
        specialites=None
    if alternance==[] or alternance==["Peu importe"]:
        alternance=None
    if regions==[] or "peu importe" in regions:
        regions=None
    if annee==[]:
        annee=None
    if ef==[] or "peu importe" in ef:
        ef=None
        
    choix_utilisateur={"specialites":specialites,
                        "alternance":alternance,
                        "concours":concours,
                        "regions":regions,
                        "annee":annee,
                        "effort":ef}

    

    #Get Notes
    maths = request.form['maths']
    physique=request.form['physique']
    si=request.form['si']
    informatique=request.form['informatique']
    anglais=request.form['anglais']
    francais=request.form['francais']
    modelisation=request.form['modelisation']

    notes={"maths":maths,
            "physique":physique,
            "si":si,
            "informatique":informatique,
            "anglais":anglais,
            "francais":francais,
            "modelisation":modelisation}

    ecole=calcul.filtre(choix_utilisateur,notes)
    ecolesdef=[]

    for eco in ecole:
        if eco[5] not in ecolesdef:
            ecolesdef.append(eco[5])



    
    return render_template('affichage.html', ecole=ecolesdef)

@bp.route('/prix',methods=['GET'])
def prix():
    text = request.args.get('jsdata').split(",")
    prixboursier=calcul.prix_ecole(text,"Boursier")
    prixnonboursier=calcul.prix_ecole(text,"NonBoursier")
    ecole=list(set(calcul.getinfo(text)))

    return render_template('prix.html', prixb=prixboursier,prixnb=prixnonboursier,ecolesinfo=ecole)






    

        
       
