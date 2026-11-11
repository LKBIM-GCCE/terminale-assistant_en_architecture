# -*- coding: utf-8 -*-
"""Site de la classe Terminale Bac Pro TEB-AA.

    python3 build.py

Génère :
  index.html          accueil de la classe (projets, prochaine séance)
  mdqb/               projet Maison de quartier Bagatelle (U22)
  villa/              projet Villa DUPONT (généré par villa/build.py)

Pour modifier un contenu : changer les données ci-dessous, puis relancer le script.
Les fichiers lourds (plans, CCTP, maquettes) restent sur le Drive : coller les liens dans DRIVE.
"""
import os, html, importlib.util

ROOT = os.path.dirname(os.path.abspath(__file__))
e = html.escape

# =====================================================================
# LIENS DRIVE — coller ici les liens de partage (laisser "" si pas prêt)
# =====================================================================
DRIVE = {
    "mdqb_dossier": "",       # dossier Drive complet du projet MDQB
    "mdqb_plans": "",         # PDF : 05 plan RDC, 06 coupes, 07 façades, 09 axonométries
    "mdqb_dwg": "",           # DWG : MDQB-RDC 1-50, MDQB-COUPE A-A
    "mdqb_cctp": "",          # CCTP lots 03, 06, 07, 08
    "mdqb_maquette": "",      # maquette clos-couvert .rvt + .ifc
    "mdqb_depot": "",         # dossier de dépôt des livrables élèves
}

# =====================================================================
# CLASSE ET PROJETS
# =====================================================================
CLASSE = {
    "titre": "Terminale TEB-AA",
    "sous_titre": "Bac Pro Technicien d'études du bâtiment · option B Assistant en architecture",
}

PROJETS = [
    {"slug": "mdqb", "titre": "Maison de quartier Bagatelle", "code": "MDQB",
     "statut": "En cours", "periode": "13/11 → 18/12/2026", "unite": "U22 · Production BIM",
     "resume": "Compléter la maquette clos-couvert d'un ERP avec le second œuvre, puis produire les plans du dossier PRO."},
    {"slug": "villa", "titre": "Villa DUPONT, Quillan", "code": "VILLA",
     "statut": "En attente", "periode": "Après Noël", "unite": "U21 · U22 · U23",
     "resume": "Dossier de permis de construire d'une maison individuelle, en trois pôles."},
]

# =====================================================================
# PROJET MDQB
# =====================================================================
MDQB = {
    "moa": "Mairie de Toulouse, Direction Bâtiments et Énergies",
    "adresse": "Impasse du Bachaga Boualam, 31100 Toulouse",
    "programme": "Maison de quartier : 4 salles polyvalentes, bureau, rangements, cuisine, sanitaires, locaux techniques",
    "type": "ERP en rez-de-chaussée",
    "phase": "Passage de l'APD au dossier PRO",
    "rendu": "Vendredi 18 décembre 2026",
    "situation": ("Vous êtes assistant(e) au service Programmation & Architecture de la Mairie de Toulouse, "
                  "maître d'œuvre de la maison de quartier Bagatelle. Le clos-couvert (structure, enveloppe, toiture, "
                  "menuiseries extérieures) est modélisé. Les CCTP des lots de second œuvre sont rédigés, mais la maquette "
                  "ne les intègre pas encore."),
    "mission": ("Compléter la maquette avec le second œuvre (doublages, cloisons, portes, sols, faux plafonds), puis éditer "
                "le plan plâtrerie n°5 et le plan plafond n°6 auxquels renvoie le CCTP du lot 07."),
    "problematique": ("Comment compléter une maquette clos-couvert pour qu'elle décrive fidèlement le second œuvre "
                      "prescrit par le CCTP et produise les plans d'aménagement du dossier PRO ?"),
}

COMPETENCES = [
    ("C2.3", "Proposer une solution à un problème identifié", [
        "Les solutions sont argumentées et respectent les contraintes techniques et réglementaires",
        "La description de la solution est explicite et complète",
        "Les effets de la solution sur le projet sont identifiés"]),
    ("C3.4", "Traduire graphiquement une solution technique et architecturale", [
        "Les techniques de représentation sont maîtrisées, du croquis à la maquette",
        "La représentation est précise et pertinente",
        "Le type de représentation et l'outil sont adaptés au document",
        "Les normes de représentation sont respectées"]),
]

NOMMAGE = [
    ("Maquette", "TEBAA_MDQB_NOM_Prenom.rvt"),
    ("Export IFC", "TEBAA_MDQB_NOM_Prenom.ifc"),
    ("Plans PDF", "MDQB_NOM_Prenom_P05_Cloisonnement.pdf"),
    ("Tableau", "MDQB_NOM_Prenom_S1_Types.csv"),
]

ARBO = """NOM_Prenom_MDQB/
├─ 01_Ressources/     (copie locale du Drive)
├─ 02_Maquette/       (.rvt, .ifc)
└─ 03_Livrables/
   ├─ S1/  S2/  S3/  S4/
   └─ S5_Rendu/"""

# Séances : chaque "partie" = (durée, titre, contenu HTML)
# Les blocs interactifs : FORM_IDENTITE, MATRICE_MAQUETTE, TABLE_TYPES (définis plus bas)

def drive(key, label):
    url = DRIVE.get(key, "")
    if url:
        return f'<a class="res-link" href="{e(url)}" target="_blank" rel="noopener">{e(label)}</a>'
    return f'<span class="res-link is-missing" title="Lien Drive à ajouter">{e(label)}</span>'

def ul(items, cls="list"):
    return f'<ul class="{cls}">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"

def checklist(page_id, items):
    lis = "".join(
        f'<li><label><input type="checkbox" data-store="{page_id}-chk-{i}"> <span>{t}</span></label></li>'
        for i, t in enumerate(items))
    return f'<ul class="todo">{lis}</ul>'

def methode(titre, contenu):
    return f'<details class="methode"><summary>Méthode · {e(titre)}</summary><div>{contenu}</div></details>'

# ---------------------------------------------------------------------
# Blocs interactifs de la S1
# ---------------------------------------------------------------------
IDENTITE = [
    ("moa", "Maître d'ouvrage"),
    ("moe", "Maître d'œuvre et bureau d'études (BET)"),
    ("adresse", "Adresse du projet"),
    ("usage", "Usage du bâtiment"),
    ("erp", "Type et catégorie d'ERP (à justifier)"),
    ("niveaux", "Nombre de niveaux"),
    ("hsp", "Hauteur sous plafond brute"),
    ("structure", "Structure porteuse (matériaux)"),
    ("toiture", "Type de toiture"),
    ("locaux", "Liste des locaux"),
    ("lots", "Lots du marché (numéro et intitulé)"),
    ("phase", "Phase des CCTP fournis et date d'indice"),
]

def form_identite():
    rows = ""
    for k, lab in IDENTITE:
        tag = "textarea" if k in ("locaux", "lots") else "input"
        field = (f'<textarea id="id-{k}" data-store="s1-id-{k}" rows="3"></textarea>' if tag == "textarea"
                 else f'<input id="id-{k}" type="text" data-store="s1-id-{k}">')
        rows += f'<div class="field"><label for="id-{k}">{e(lab)}</label>{field}</div>'
    return f'<div class="form-grid">{rows}</div>'

MAQUETTE_ELEMENTS = [
    ("Poteaux et poutres béton", "01 Gros œuvre"),
    ("Murs extérieurs", "01 Gros œuvre"),
    ("Toiture-terrasse, acrotères", "01 / 02"),
    ("Menuiseries extérieures", "04 Menuiserie alu"),
    ("Doublages des murs", "07 Plâtrerie"),
    ("Cloisons intérieures", "07 Plâtrerie"),
    ("Portes et châssis intérieurs", "06 Menuiserie bois"),
    ("Sols finis (carrelage)", "03 Carrelage"),
    ("Faux plafonds", "07 Plâtrerie"),
    ("Pièces (nom, surface)", "—"),
]

def matrice_maquette():
    head = "<tr><th scope=\"col\">Élément</th><th scope=\"col\">Lot</th><th scope=\"col\">Présent</th><th scope=\"col\">Partiel</th><th scope=\"col\">Absent</th><th scope=\"col\">Remarque</th></tr>"
    rows = ""
    for i, (el, lot) in enumerate(MAQUETTE_ELEMENTS):
        radios = "".join(
            f'<td class="c"><input type="radio" name="mq{i}" value="{v}" data-store="s1-mq-{i}" aria-label="{e(el)} : {v}"></td>'
            for v in ("présent", "partiel", "absent"))
        rows += (f'<tr><th scope="row">{e(el)}</th><td class="mono small">{e(lot)}</td>{radios}'
                 f'<td><input type="text" data-store="s1-mq-rq-{i}" aria-label="Remarque {e(el)}"></td></tr>')
    return f'<div class="table-scroll"><table class="data matrice"><thead>{head}</thead><tbody>{rows}</tbody></table></div>'

TYPES_COLS = ["Code type Revit", "Lot", "Art. CCTP", "Composition (de l'extérieur vers l'intérieur)", "Épaisseur (mm)", "Hauteur", "Localisation"]
TYPES_EXEMPLE = ["DBL-BA13-COLLE", "07", "2.1", "Plots de MAP + 1 plaque BA13", "≈ 13 + plots", "Faux plafond + 10 cm", "Mur extérieur et agglo salle polyvalente 4, poteaux BA…"]

def table_types():
    th = "".join(f'<th scope="col">{e(c)}</th>' for c in TYPES_COLS) + '<th scope="col"><span class="sr">Supprimer</span></th>'
    ex = "".join(f"<td>{e(c)}</td>" for c in TYPES_EXEMPLE) + "<td></td>"
    return f'''<div class="table-scroll"><table class="data editable" id="types" data-store="s1-types" data-cols="{len(TYPES_COLS)}">
<thead><tr>{th}</tr></thead>
<tbody><tr class="exemple">{ex}</tr></tbody></table></div>
<div class="actions">
  <button type="button" class="btn" data-action="add-row" data-target="types">+ Ajouter une ligne</button>
  <button type="button" class="btn btn-ghost" data-action="export-csv" data-target="types" data-file="MDQB_NOM_Prenom_S1_Types.csv">Télécharger pour Excel (.csv)</button>
</div>'''

# ---------------------------------------------------------------------
# Les séances
# ---------------------------------------------------------------------
SEANCES = [
  {"n": 1, "date": "2026-11-13", "jour": "Ven. 13/11", "duree": "4 h", "type": "TD 01",
   "titre": "Découvrir le projet : quoi modéliser, et où ?",
   "prob": "Que faut-il ajouter à la maquette de l'architecte, et où ?",
   "eval": "Formative",
   "situation": "L'architecte vous confie le dossier. Avant de toucher à la maquette, il veut savoir si vous avez compris le projet, ce qui est déjà modélisé, et ce que demandent les CCTP du second œuvre.",
   "donne": [("mdqb_plans", "Plans PDF (RDC, coupes, façades, axonométries)"), ("mdqb_cctp", "CCTP lots 03, 06, 07, 08"),
             ("mdqb_maquette", "Maquette clos-couvert (.rvt et .ifc)")],
   "parties": [
     ("15 min", "Lancement", "<p>Présentation du projet, de la séquence et du rendu du 18/12. Créez votre arborescence de dossiers (voir l'accueil du projet).</p>"),
     ("45 min", "A · Fiche d'identité du projet",
      "<p>À l'aide des plans et des pages de garde des CCTP, complétez la fiche. Vos réponses restent enregistrées sur ce poste ; imprimez-la en PDF à la fin.</p>"
      "{FORM_IDENTITE}"
      + "{M_ERP}"),
     ("45 min", "B · Ce que contient la maquette",
      "<p>Ouvrez la maquette clos-couvert dans Revit. Parcourez le plan du RDC, une coupe et la vue 3D. Pour chaque élément, indiquez s'il est modélisé.</p>"
      "{MATRICE}"),
     ("60 min", "C · Croquis à main levée des niveaux",
      "<p>Sur une feuille A3, au crayon, sans règle graduée :</p>"
      + ul(["<b>Plan schématique du RDC</b> : murs, poteaux, noms des locaux.",
            "<b>Coupe schématique</b> passant par une salle polyvalente et un local à faux plafond bas : dalle, sol fini (±0,00), faux plafonds, plancher haut, toiture.",
            "<b>Cotez les hauteurs</b> : hauteur sous plafond brute, hauteurs sous faux plafond (HSFP) relevées dans le CCTP du lot 07.",
            "<b>Coloriez par lot</b> où ira chaque ouvrage, avec une légende."])
      + '<div class="legende-lots"><span class="lot l07">Rouge · cloisons et doublages (lot 07)</span><span class="lot l07fp">Bleu · faux plafonds (lot 07)</span>'
        '<span class="lot l03">Vert · sols carrelés (lot 03)</span><span class="lot l06">Marron · portes et châssis (lot 06)</span></div>'
      + "{M_CROQUIS}"),
     ("60 min", "D · Tableau des types de second œuvre",
      "<p>Lisez les articles ci-dessous et créez <b>un type par ligne</b>. Ce tableau sera votre cahier des charges pour modéliser en S2 à S4. La première ligne est un exemple.</p>"
      + ul(["<b>Lot 07</b> : articles 2.1 à 2.7 (doublages, cloisons), 2.9 à 2.12 (faux plafonds)",
            "<b>Lot 06</b> : articles 2.1 à 2.4 (portes, châssis, placards)",
            "<b>Lot 03</b> : articles 2.2 à 2.4 (carrelages)"])
      + "<p>Codes à utiliser : <span class=\"mono\">DBL-</span> doublage, <span class=\"mono\">CLO-</span> cloison, <span class=\"mono\">FP-</span> faux plafond, <span class=\"mono\">SOL-</span> sol, <span class=\"mono\">POR-</span> porte.</p>"
      "{TABLE_TYPES}{M_CCTP}{M_CLOISON}"),
     ("15 min", "Bilan", "<p>Mise en commun : quels ouvrages manquent dans la maquette ? Quelles incohérences avez-vous relevées entre les plans et les CCTP ?</p>"),
   ],
   "livrables": ["Fiche d'identité imprimée en PDF", "Croquis A3 (photo déposée sur le Drive)", "Tableau des types (.csv)"],
   "check": ["Fiche d'identité complète, sources vérifiées", "Matrice de la maquette remplie", "Plan et coupe schématiques, locaux nommés",
             "Hauteurs cotées sur la coupe", "Code couleur par lot et légende", "Un type par article du CCTP, épaisseurs calculées",
             "Fichiers nommés et déposés dans 03_Livrables/S1"]},

  {"n": 2, "date": "2026-11-20", "jour": "Ven. 20/11", "duree": "3 h", "type": "TP 01",
   "titre": "Préparer la maquette : fond de plan et types de parois",
   "prob": "Comment préparer une maquette pour que le second œuvre s'y modélise juste du premier coup ?",
   "eval": "Formative",
   "situation": "Le tableau des types est validé. Vous préparez la maquette avant de modéliser : fond de plan calé, types créés, paramètre de lot.",
   "donne": [("mdqb_maquette", "Maquette clos-couvert (.rvt)"), ("mdqb_dwg", "DWG : RDC 1/50 et coupe A-A")],
   "parties": [
     ("15 min", "Lancement", "<p>Rappel Revit : enregistrer sous votre nom, organisation des vues, sauvegardes.</p>"),
     ("45 min", "A · Niveaux et fond de plan",
      ul(["Enregistrez la maquette sous <span class=\"mono\">TEBAA_MDQB_NOM_Prenom.rvt</span>.",
          "Contrôlez les niveaux et la hauteur sous plafond dans une coupe.",
          "Liez le DWG du RDC : unités en mètres, couche visible seulement, positionnement manuel.",
          "Calez le DWG sur deux poteaux, puis <b>épinglez-le</b>."])
      + "{M_DWG}"),
     ("90 min", "B · Types de murs, sols et plafonds",
      ul(["Dupliquez un type de mur de base pour chaque ligne <span class=\"mono\">DBL-</span> et <span class=\"mono\">CLO-</span> de votre tableau.",
          "Éditez la structure : couches, matériaux, épaisseurs, fonction de chaque couche.",
          "Faites de même pour les types de sol (<span class=\"mono\">SOL-</span>) et de plafond (<span class=\"mono\">FP-</span>).",
          "Vérifiez que l'épaisseur totale de chaque type correspond au tableau."])
      + "{M_TYPES}"),
     ("30 min", "C · Paramètre « Lot CCTP »",
      ul(["Créez le paramètre partagé <span class=\"mono\">Lot CCTP</span> (texte, par type) pour les murs, sols, plafonds et portes.",
          "Renseignez-le pour chaque type créé (07, 06, 03)."])),
   ],
   "livrables": ["Maquette avec DWG calé, types créés, paramètre renseigné"],
   "check": ["Fichier enregistré au bon nom", "DWG lié, calé et épinglé", "Un type par ligne du tableau",
             "Épaisseurs conformes", "Paramètre Lot CCTP renseigné"]},

  {"n": 3, "date": "2026-11-27", "jour": "Ven. 27/11", "duree": "4 h", "type": "TP 02",
   "titre": "Cloisonnement et menuiseries intérieures",
   "prob": "Quelle cloison et quelle porte pour chaque local ?",
   "eval": "Formative",
   "situation": "Vous modélisez le cloisonnement. Certains locaux techniques exigent des parois coupe-feu : le bon type doit être au bon endroit.",
   "donne": [("mdqb_plans", "Plan RDC (PDF)"), ("mdqb_cctp", "CCTP lots 06 et 07")],
   "parties": [
     ("15 min", "Lancement", "<p>Repérage des locaux à risque et des exigences de résistance au feu.</p>"),
     ("120 min", "A · Doublages et cloisons",
      ul(["Modélisez doublages et cloisons sur le fond DWG, ligne de justification adaptée (nu fini).",
          "Choisissez le type selon le local : coupe-feu ½ h, 1 h, 2 h, cloison des sanitaires, supports de cloisons mobiles.",
          "Réglez les hauteurs prescrites : sous plancher, sous faux plafond, ou faux plafond + 10 cm.",
          "Attachez les cloisons au niveau supérieur quand c'est demandé."])),
     ("75 min", "B · Portes et châssis",
      ul(["Insérez les portes coupe-feu, les portes à âme pleine et les châssis fixes (dimensions suivant plan).",
          "Vérifiez les largeurs de passage (accessibilité ERP).",
          "Renseignez le paramètre Lot CCTP."])),
     ("30 min", "C · Contrôle", ul(["Superposez la maquette et le DWG : aucun écart visible.", "Vérifiez une coupe par local technique."])),
   ],
   "livrables": ["Maquette indice B : cloisonnement et menuiseries intérieures"],
   "check": ["Tous les locaux fermés", "Types CF placés aux bons locaux", "Hauteurs conformes au CCTP",
             "Portes et châssis insérés", "Passages PMR vérifiés"]},

  {"n": 4, "date": "2026-12-11", "jour": "Ven. 11/12", "duree": "4 h", "type": "TP 03",
   "titre": "Sols, faux plafonds, pièces et surfaces",
   "prob": "La maquette donne-t-elle les mêmes surfaces que le plan de l'architecte ?",
   "eval": "Formative",
   "situation": "Le cloisonnement est en place. Vous ajoutez les sols et les faux plafonds, puis vous contrôlez les surfaces.",
   "donne": [("mdqb_plans", "Plan RDC avec surfaces (PDF)"), ("mdqb_cctp", "CCTP lots 03 et 07")],
   "parties": [
     ("15 min", "Lancement", "<p>Rappel : sol fini, faux plafond, hauteur sous faux plafond.</p>"),
     ("90 min", "A · Sols et faux plafonds",
      ul(["Modélisez les sols finis par type de carrelage et par local.",
          "Modélisez les faux plafonds par type, à la HSFP prescrite.",
          "Contrôlez en coupe : faux plafond, plénum, plancher haut."])),
     ("75 min", "B · Pièces et surfaces",
      ul(["Créez et nommez les pièces, étiquette nom + surface.",
          "Éditez la nomenclature des pièces.",
          "Comparez avec les surfaces du plan architecte et justifiez chaque écart supérieur à 0,5 m²."])),
     ("60 min", "C · Nomenclature des finitions",
      ul(["Créez une nomenclature par pièce : sol, murs, plafond, HSFP.", "Exportez-la vers Excel."])),
   ],
   "livrables": ["Maquette indice C", "Nomenclatures des pièces et des finitions"],
   "check": ["Sols et faux plafonds dans tous les locaux", "HSFP conformes", "Pièces nommées avec surface",
             "Écarts de surface justifiés", "Nomenclature exportée"]},

  {"n": 5, "date": "2026-12-18", "jour": "Ven. 18/12", "duree": "3 h", "type": "Évaluation",
   "titre": "Rendu du dossier PRO",
   "prob": "Le dossier est-il prêt à être transmis aux entreprises ?",
   "eval": "Sommative",
   "situation": "L'architecte attend les plans de second œuvre pour le dossier PRO. Vous produisez les plans, les exports et un détail.",
   "donne": [("mdqb_depot", "Dossier de dépôt du rendu")],
   "parties": [
     ("75 min", "A · Plans du dossier PRO",
      ul(["<b>Plan plâtrerie n°5</b> : cloisonnement coté, légende des types de cloisons et doublages.",
          "<b>Plan plafond n°6</b> : repérage couleur des types de faux plafond et des HSFP, légende.",
          "Vue 3D plongeante du second œuvre."])),
     ("45 min", "B · Mise en page et exports",
      ul(["Feuilles A3 avec cartouche complété, échelles adaptées.",
          "Exports PDF, IFC et RVT au bon nom dans <span class=\"mono\">03_Livrables/S5_Rendu</span>."])),
     ("60 min", "C · Détail à main levée",
      "<p>Au 1/5, sur papier : jonction entre une cloison coupe-feu et le faux plafond. Désignez tous les matériaux et cotez les couches.</p>"),
   ],
   "livrables": ["Plan plâtrerie n°5 et plan plafond n°6 (PDF A3)", "Maquette .rvt et .ifc", "Détail au 1/5"],
   "check": ["Plans cotés et légendés", "Cartouche complet", "Exports PDF, IFC, RVT nommés", "Détail désigné et coté"],
   "grille": [
     ("C2.3", "Types de parois et de plafonds conformes au CCTP", 2),
     ("C2.3", "Choix coupe-feu et acoustiques cohérents avec les locaux", 2),
     ("C2.3", "Incohérences du dossier relevées, solution proposée", 2),
     ("C3.4", "Maquette du second œuvre complète et juste", 4),
     ("C3.4", "Pièces nommées, surfaces conformes", 2),
     ("C3.4", "Plan plâtrerie n°5 coté et légendé", 2),
     ("C3.4", "Plan plafond n°6 repéré et légendé", 2),
     ("C3.4", "Mise en page, cartouche, exports nommés", 2),
     ("C3.4", "Détail à main levée au 1/5", 2),
   ]},
]

METHODES = {
  "M_ERP": methode("Type et catégorie d'un ERP",
      "<p>Le <b>type</b> (lettre) dépend de l'activité ; la <b>catégorie</b> (1 à 5) dépend de l'effectif accueilli. "
      "Une salle polyvalente relève en général du type L. Cherchez l'effectif ou la catégorie dans le dossier, sinon formulez une hypothèse justifiée.</p>"),
  "M_CROQUIS": methode("Réussir un croquis coté",
      ul(["Commencez par les axes et les poteaux, puis les murs.", "Respectez les proportions : comptez les trames.",
          "Traits forts pour les éléments coupés, traits fins pour les vues.", "Cotez en mètres avec deux décimales (2,50).",
          "Ajoutez un titre, votre nom, la date."])),
  "M_CCTP": methode("Lire un article de CCTP",
      ul(["<b>Description</b> : matériaux, nombre de plaques, isolant, ossature.", "<b>Performances</b> : coupe-feu, acoustique (Rw), résistance thermique (R).",
          "<b>Hauteur</b> : sous plancher, sous faux plafond, faux plafond + 10 cm.", "<b>Localisation</b> : les locaux concernés et le plan de référence."])),
  "M_CLOISON": methode("Calculer l'épaisseur d'une cloison",
      "<p>Épaisseur = ossature + plaques des deux faces. Exemple : Placostil 72/48 = rail de 48 mm + 1 BA13 par face → 48 + 2 × 12,5 ≈ 72 mm. "
      "Si l'épaisseur annoncée ne correspond pas à la composition décrite, notez-le : c'est une incohérence à signaler.</p>"),
  "M_DWG": methode("Lier et caler un DWG",
      ul(["Insérer › Lier CAO : couleurs noir et blanc, unités mètres, positionnement manuel.", "Déplacer le lien en accrochant un point connu (axe de poteau).",
          "Vérifier un deuxième point pour contrôler l'orientation.", "Modifier › Épingler pour éviter tout déplacement."])),
  "M_TYPES": methode("Créer un type de mur composé",
      ul(["Sélectionner un mur › Modifier le type › Dupliquer › nommer avec le code du tableau.", "Structure › Modifier : ajouter les couches, affecter le matériau et l'épaisseur.",
          "Placer l'ossature en noyau, les plaques en finition.", "Contrôler l'épaisseur totale affichée."])),
}

# =====================================================================
# GABARIT HTML
# =====================================================================
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">\n')

def doc(title, body, depth, nav="", brand=("Terminale TEB-AA", "Bac Pro TEB · Assistant en architecture"), footer=""):
    up = "../" * depth
    return f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
{FONTS}<link rel="stylesheet" href="{up}assets/style.css">
</head>
<body>
<header class="site-header">
  <div class="wrap header-inner">
    <a href="{up}index.html" class="brand">
      <span class="brand-mark" aria-hidden="true">AA</span>
      <span class="brand-text"><strong>{e(brand[0])}</strong><span>{e(brand[1])}</span></span>
    </a>
    <nav class="nav" aria-label="Navigation principale">{nav}</nav>
  </div>
</header>
<main>
{body}
</main>
{footer}
<script src="{up}assets/site.js"></script>
</body>
</html>
'''

def nav_mdqb(active):
    items = [("../index.html", "← Classe"), ("index.html", "Projet")] + [(f"s{s['n']}.html", f"S{s['n']}") for s in SEANCES]
    return "".join(
        f'<a href="{h}" class="nav-link{" is-active" if h == active else ""}"{" aria-current=\"page\"" if h == active else ""}>{e(t)}</a>'
        for h, t in items)

def cartouche_mdqb():
    return f'''<footer class="site-footer">
  <div class="wrap">
    <table class="cartouche" aria-label="Cartouche du projet">
      <tr><th>Projet</th><td>Maison de quartier Bagatelle – second œuvre, dossier PRO</td><th>Unité</th><td class="mono">U22</td></tr>
      <tr><th>Maître d'ouvrage</th><td>{e(MDQB["moa"])}</td><th>Séquence</th><td class="mono">13/11 – 18/12/2026</td></tr>
      <tr><th>Classe</th><td>{e(CLASSE["sous_titre"])}</td><th>Rendu</th><td class="mono">18/12/2026</td></tr>
    </table>
  </div>
</footer>'''

# ---------------------------------------------------------------- accueil classe
def page_classe():
    cards = ""
    for p in PROJETS:
        on = p["statut"] == "En cours"
        cards += f'''<a class="projet-card{" is-on" if on else ""}" href="{p["slug"]}/index.html">
  <span class="projet-top"><span class="mono">{e(p["code"])}</span><span class="statut{" is-on" if on else ""}">{e(p["statut"])}</span></span>
  <span class="pole-name">{e(p["titre"])}</span>
  <span class="pole-role">{e(p["resume"])}</span>
  <dl class="kv"><div><dt>Période</dt><dd>{e(p["periode"])}</dd></div><div><dt>Unités</dt><dd>{e(p["unite"])}</dd></div></dl>
  <span class="pole-go">Ouvrir le projet</span>
</a>'''
    agenda = "".join(
        f'<li data-date="{s["date"]}"><a href="mdqb/s{s["n"]}.html"><span class="mono">{e(s["jour"])}</span>'
        f'<span>MDQB · S{s["n"]} — {e(s["titre"])}</span><span class="badge-next">Prochaine</span></a></li>' for s in SEANCES)
    body = f'''
<section class="hero wrap">
  <p class="eyebrow">Site de la classe · 2026-2027</p>
  <h1>{e(CLASSE["titre"])}</h1>
  <p class="lead">Toutes les consignes, séances et ressources de la classe sont ici. Les fichiers lourds (plans, CCTP, maquettes) sont sur le Drive, accessibles depuis chaque séance.</p>
</section>
<section class="wrap section">
  <h2>Projets</h2>
  <div class="poles">{cards}</div>
</section>
<section class="wrap section">
  <h2>Agenda U22</h2>
  <p class="section-lead">La prochaine séance est signalée, les séances passées sont atténuées.</p>
  <ol class="agenda">{agenda}</ol>
</section>
<section class="wrap section two-col">
  <div>
    <h2>Règles de travail</h2>
    {ul(["Un dossier par projet, organisé comme indiqué sur la page du projet.",
         "Vos réponses saisies dans les pages restent sur le poste : <b>exportez ou imprimez avant de partir</b>.",
         "Les livrables se déposent sur le Drive, au nom convenu, à la fin de chaque séance."])}
  </div>
  <div>
    <h2>Épreuve E22</h2>
    {ul(["Production de documents graphiques · 6 h sur poste · coefficient 3.",
         "Compétences évaluées : C2.3 et C3.4.",
         "Toujours demandé : maquette .ifc + format natif, plans mis en page, détail à main levée."])}
  </div>
</section>'''
    return doc(f'{CLASSE["titre"]} – site de la classe', body, 0,
               nav='<a href="index.html" class="nav-link is-active" aria-current="page">Accueil</a><a href="mdqb/index.html" class="nav-link">MDQB</a><a href="villa/index.html" class="nav-link">Villa</a>')

# ---------------------------------------------------------------- accueil MDQB
def page_mdqb():
    cards = ""
    for s in SEANCES:
        cards += f'''<a class="seance-card" href="s{s["n"]}.html" data-date="{s["date"]}">
  <span class="seance-date"><span class="mono">{e(s["jour"])}</span><span>{e(s["duree"])}</span></span>
  <span class="seance-card-title"><span class="seance-num mono">S{s["n"]} · {e(s["type"])}</span>{e(s["titre"])}</span>
  <span class="eval-tag{" is-som" if s["eval"] == "Sommative" else ""}">{e(s["eval"])}</span>
  <span class="badge-next">Prochaine séance</span>
</a>'''
    comps = "".join(
        f'<div class="comp"><p class="comp-code mono">{c}</p><h3>{e(n)}</h3>{ul([e(i) for i in inds], "checks")}</div>'
        for c, n, inds in COMPETENCES)
    nom = "".join(f'<div><dt>{e(a)}</dt><dd class="mono">{e(b)}</dd></div>' for a, b in NOMMAGE)
    res = "".join(f"<li>{drive(k, l)}</li>" for k, l in [
        ("mdqb_dossier", "Dossier Drive du projet"), ("mdqb_plans", "Plans PDF"), ("mdqb_dwg", "Fonds de plan DWG"),
        ("mdqb_cctp", "CCTP lots 03, 06, 07, 08"), ("mdqb_maquette", "Maquette clos-couvert"), ("mdqb_depot", "Dépôt des livrables")])
    body = f'''
<section class="hero wrap hero-u22">
  <p class="eyebrow">Projet 1 · U22 Production BIM · 5 séances, 18 h</p>
  <h1>Maison de quartier Bagatelle</h1>
  <p class="lead">{e(MDQB["situation"])}</p>
  <p class="lead"><b>Mission :</b> {e(MDQB["mission"])}</p>
  <dl class="facts">
    <div><dt>Maître d'ouvrage</dt><dd>{e(MDQB["moa"])}</dd></div>
    <div><dt>Bâtiment</dt><dd>{e(MDQB["type"])}</dd></div>
    <div><dt>Phase</dt><dd>{e(MDQB["phase"])}</dd></div>
    <div><dt>Rendu</dt><dd>{e(MDQB["rendu"])}</dd></div>
  </dl>
  <p class="problematique">« {e(MDQB["problematique"])} »</p>
</section>
<section class="wrap section pole-u22">
  <h2>Séances</h2>
  <div class="seance-cards">{cards}</div>
</section>
<section class="wrap section">
  <h2>Compétences évaluées</h2>
  <div class="comps">{comps}</div>
</section>
<section class="wrap section two-col">
  <div>
    <h2>Ressources (Drive)</h2>
    <ul class="res-list">{res}</ul>
  </div>
  <div>
    <h2>Nommage et dossier</h2>
    <dl class="kv kv-block">{nom}</dl>
    <pre class="tree mono">{e(ARBO)}</pre>
  </div>
</section>'''
    return doc("MDQB – Maison de quartier Bagatelle", body, 1, nav=nav_mdqb("index.html"), footer=cartouche_mdqb())

# ---------------------------------------------------------------- page séance
def page_seance(s):
    pid = f"s{s['n']}"
    parties = ""
    for i, (duree, titre, contenu) in enumerate(s["parties"], 1):
        c = contenu
        c = c.replace("{FORM_IDENTITE}", form_identite()).replace("{MATRICE}", matrice_maquette()).replace("{TABLE_TYPES}", table_types())
        for k, v in METHODES.items():
            c = c.replace("{" + k + "}", v)
        parties += f'''<li class="partie">
  <div class="partie-head"><span class="partie-duree mono">{e(duree)}</span><h3>{e(titre)}</h3></div>
  <div class="partie-body">{c}</div>
</li>'''
    donne = "".join(f"<li>{drive(k, l)}</li>" for k, l in s["donne"])
    grille = ""
    if s.get("grille"):
        rows = "".join(f'<tr><td class="mono">{c}</td><td>{e(cr)}</td><td class="mono c">{p}</td></tr>' for c, cr, p in s["grille"])
        total = sum(p for _, _, p in s["grille"])
        grille = f'''<section class="wrap section">
  <h2>Grille d'évaluation</h2>
  <div class="table-scroll"><table class="data"><thead><tr><th scope="col">Compétence</th><th scope="col">Critère</th><th scope="col">Points</th></tr></thead>
  <tbody>{rows}<tr class="total"><td></td><th scope="row">Total</th><td class="mono c">{total}</td></tr></tbody></table></div>
</section>'''
    prev_link = f'<a class="btn btn-ghost" href="s{s["n"]-1}.html">← S{s["n"]-1}</a>' if s["n"] > 1 else '<a class="btn btn-ghost" href="index.html">← Projet</a>'
    next_link = f'<a class="btn" href="s{s["n"]+1}.html">S{s["n"]+1} →</a>' if s["n"] < len(SEANCES) else ""
    body = f'''
<section class="hero wrap hero-u22" data-date="{s["date"]}">
  <p class="eyebrow">MDQB · Séance {s["n"]} · {e(s["type"])} · {e(s["jour"])} · {e(s["duree"])} · {e(s["eval"])}</p>
  <h1>{e(s["titre"])}</h1>
  <p class="problematique">« {e(s["prob"])} »</p>
  <p class="lead">{e(s["situation"])}</p>
</section>
<section class="wrap section seance-layout">
  <div class="seance-main">
    <h2>Déroulé</h2>
    <ol class="parties">{parties}</ol>
  </div>
  <aside class="seance-aside">
    <div class="box"><p class="label">On vous donne</p><ul class="res-list">{donne}</ul></div>
    <div class="box"><p class="label">Livrables</p>{ul([e(l) for l in s["livrables"]])}</div>
    <div class="box"><p class="label">Avant de partir</p>{checklist(pid, [e(c) for c in s["check"]])}</div>
    <div class="box actions-col">
      <button type="button" class="btn" data-action="print">Imprimer / PDF</button>
      <button type="button" class="btn btn-ghost" data-action="reset" data-prefix="{pid}-">Effacer mes saisies</button>
    </div>
  </aside>
</section>
{grille}
<section class="wrap section pager">{prev_link}{next_link}</section>'''
    return doc(f"MDQB S{s['n']} – {s['titre']}", body, 1, nav=nav_mdqb(f"s{s['n']}.html"), footer=cartouche_mdqb())

# =====================================================================
def write(path, content):
    path = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def build():
    write("index.html", page_classe())
    write("mdqb/index.html", page_mdqb())
    for s in SEANCES:
        write(f"mdqb/s{s['n']}.html", page_seance(s))
    spec = importlib.util.spec_from_file_location("villa_build", os.path.join(ROOT, "villa", "build.py"))
    villa = importlib.util.module_from_spec(spec); spec.loader.exec_module(villa); villa.build()

if __name__ == "__main__":
    build()
    print("ok")
