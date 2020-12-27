from flask import Flask, session, redirect, url_for, request,render_template
import main


app = Flask(__name__)


@app.route('/', methods=['GET'])
def accueil():
    special = main.renvoie_specialites()
    region = main.renvoie_regions()
    concours = main.renvoie_admission()
    return render_template('index.html', special=special,region=region,concours=concours)


@app.route('/', methods=['POST'])
def my_form_post():
    
    #Get data of listbox
    specialites = request.form.getlist('specialite')
    alternance = request.form.getlist('alternance')
    concours = request.form.getlist('concours')
    regions = request.form.getlist('region')
    annee = request.form.getlist('annee')
    



    specialites =main.renvoie_idspe(specialites)
    
    #Check list vide
    if specialites==[]:
        specialites=None
    if alternance==[] or alternance==["Peu importe"]:
        alternance=None
    if concours==[]:
        concours=None
    if regions==[]:
        regions=None
    if annee==[]:
        annee=None

    choix_utilisateur={"specialites":specialites,
                        "alternance":alternance,
                        "concours":concours,
                        "regions":regions,
                        "annee":annee}

    

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

    ecole=main.filtre(choix_utilisateur,notes)
    ecolesdef=[]

    for eco in ecole:
        if eco[5] not in ecolesdef:
            ecolesdef.append(eco[5])



    
    return render_template('affichage.html', ecole=ecolesdef)

@app.route('/prix',methods=['GET'])
def prix():
    text = request.args.get('jsdata').split(",")
    prixboursier=main.prix_ecole(text,"Boursier")
    prixnonboursier=main.prix_ecole(text,"NonBoursier")
    ecole=list(set(main.getinfo(request.form.getlist('ecole'))))

    return render_template('prix.html', prixb=prixboursier,prixnb=prixnonboursier,ecolesinfo=ecole)






    

        
       
