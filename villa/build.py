# -*- coding: utf-8 -*-
"""Générateur du site Projet Villa DUPONT – Terminale TEB-AA.
Écrit les pages dans villa/. Lancé par ../build.py
"""
import os, html, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")

# ---------------------------------------------------------------- données
PROJET = {
    "titre": "Villa DUPONT",
    "adresse": "71 avenue Maurice Sarraut, 11500 Quillan",
    "parcelles": "AD 276 et AD 277",
    "surface": "2 549 m²",
    "zone": "UB",
    "plu": "PLUi Communauté de communes des Pyrénées Audoises (19/12/2019)",
    "rendu": "Vendredi 18 décembre 2026",
}

POLES = {
    "u21": {"code": "U21", "nom": "Urbanisme et réglementation", "role": "Chef de projet : conformité et autorisations",
            "epreuve": "E21 · Analyse d'un programme de construction · écrit 4 h · coef. 2",
            "creneau": "Lundi 9 h 10 – 12 h 10", "volume": "18 h",
            "enseignant": "À définir",
            "competences": [
                ("C2.1", "Analyser un dossier", [
                    "L'inventaire des pièces écrites et graphiques est complet et exact",
                    "Les plans, coupes et façades sont lus et interprétés correctement",
                    "Les contraintes techniques, réglementaires et environnementales sont repérées",
                    "Les documents administratifs sont renseignés"]),
                ("C2.2", "Vérifier la cohérence du projet avec les contraintes réglementaires et techniques", [
                    "La compatibilité entre choix architecturaux et règles (PLU, RE2020) est analysée",
                    "Les incohérences entre les pièces du dossier sont identifiées",
                    "Les solutions proposées sont cohérentes"])],
            "recoit": [("U22", "Vendredi 4/12 et 11/12", "Surfaces issues de la maquette, pièces graphiques PDF pour le contrôle"),
                       ("U23", "Jeudi 10/12", "Notice PC04 pour le contrôle")],
            "transmet": [("U22 et U23", "Lundi 16/11", "Fiches de demande de modification de l'esquisse"),
                         ("U23", "Lundi 23/11", "Règles d'aspect extérieur (note d'études)"),
                         ("U22 et U23", "Lundi 14/12", "Grilles du contrôle instructeur")],
            "livrables": ["Fiche de recueil des données du terrain", "Tableau des contraintes et fiches de modification",
                          "Note d'études (2 pages)", "Tableau des surfaces et de la pleine terre",
                          "Cerfa 13406 et attestation RE2020 (PC16-1)", "Grille de contrôle du dossier d'un autre élève"],
            "seances": [
                ("2026-11-09", "Lun. 9/11", "3 h", "Lancement et acte de construire",
                 "Quelles démarches et quels documents faut-il pour avoir le droit de construire cette maison ?",
                 ["Découvrir l'agence, ses trois pôles et le dossier client",
                  "Identifier les acteurs, les phases d'un projet et l'autorisation adaptée (DP, PC, PA)",
                  "Relever le zonage sur le Géoportail de l'urbanisme, la référence et la contenance sur cadastre.gouv.fr, les risques sur Géorisques"],
                 "Fiche activité « acte de construire » · Fiche de recueil des données du terrain",
                 "S1-00 Activité découverte · Dossier client · Rapport Géorisques · Plan cadastral"),
                ("2026-11-16", "Lun. 16/11", "3 h", "PLU et conformité de l'esquisse",
                 "L'esquisse est-elle constructible telle quelle sur ce terrain ?",
                 ["Relever dans la zone UB les règles d'implantation, hauteur, toiture, façades, clôtures, pleine terre, stationnement, réseaux",
                  "Tenir compte des deux parcelles",
                  "Confronter l'esquisse aux règles et lister les non-conformités",
                  "Rédiger une fiche de demande de modification par non-conformité"],
                 "Tableau des contraintes · Fiches de modification (transmises à U22 et U23 en fin de séance)",
                 "M01 Lire un PLU · Règlement PLUi zone UB et lexique · Esquisse ESQ01 à ESQ03"),
                ("2026-11-23", "Lun. 23/11", "3 h", "Note d'études",
                 "Le projet répond-il au programme, au site et aux réglementations ?",
                 ["Comparer le programme du client aux surfaces de l'esquisse, analyser circulations et séparation jour / nuit",
                  "Situer le projet dans l'architecture locale de la haute vallée de l'Aude",
                  "Identifier les autres réglementations : RE2020, sismique, acoustique, accessibilité",
                  "Rédiger la note d'études à destination du chef de projet"],
                 "Note d'études 2 pages (PDF) · Règles d'aspect transmises à U23",
                 "Trame de note d'études · Dossier client"),
                ("2026-11-30", "Lun. 30/11", "3 h", "Surfaces réglementaires",
                 "Quelles surfaces le projet génère-t-il et quelles obligations déclenchent-elles ?",
                 ["Calculer la surface de plancher, l'emprise au sol et la surface taxable",
                  "Vérifier le seuil de recours obligatoire à l'architecte (150 m² de surface de plancher)",
                  "Calculer la pleine terre et vérifier le minimum du PLU"],
                 "Tableau Excel des surfaces et de la pleine terre",
                 "M02 Surfaces et espaces libres · Tableau des surfaces · Esquisse"),
                ("2026-12-07", "Lun. 7/12", "3 h", "Cerfa et attestation RE2020",
                 "Quelles informations le service instructeur attend-il ?",
                 ["Choisir et remplir le Cerfa 13406 en cohérence avec les surfaces",
                  "Renseigner l'attestation RE2020 à partir des données du bureau d'études thermiques",
                  "Établir la liste des pièces à joindre (bordereau)"],
                 "Cerfa 13406 · Attestation RE2020 (PC16-1)",
                 "M04 Cerfa 13406 · M05 Attestation RE2020 · Données thermiques du dossier client"),
                ("2026-12-14", "Lun. 14/12", "3 h", "Contrôle instructeur croisé",
                 "Le dossier est-il complet et cohérent avant son dépôt ?",
                 ["Échanger son dossier avec un autre élève et le contrôler comme le service instructeur",
                  "Comparer les surfaces calculées à la main et celles de la maquette, expliquer les écarts",
                  "Rédiger la grille de validation et la demande de pièces complémentaires",
                  "Identifier les étapes du dépôt dématérialisé"],
                 "Grille de validation du dossier d'un autre élève (transmise à U22 et U23)",
                 "Liste de contrôle du dossier PC · M07 Dépôt dématérialisé · Règlement PLUi"),
            ]},
    "u22": {"code": "U22", "nom": "Production BIM", "role": "Pôle études et maquette",
            "epreuve": "E22 · Production de documents graphiques · 6 h sur poste · coef. 3",
            "creneau": "Vendredi, 3 h", "volume": "18 h",
            "enseignant": "Kevin Lormeau",
            "competences": [
                ("C2.3", "Proposer une solution à un problème identifié", [
                    "Les solutions sont argumentées et respectent les contraintes techniques, réglementaires et environnementales",
                    "La description de la solution est explicite et complète",
                    "Les effets de la solution sur le projet sont identifiés"]),
                ("C3.4", "Traduire graphiquement une solution technique et architecturale", [
                    "Les techniques de représentation sont maîtrisées, du croquis à la maquette",
                    "La représentation est précise et pertinente",
                    "Le type de représentation et l'outil sont adaptés au document",
                    "Les normes de représentation sont respectées"])],
            "recoit": [("U21", "Lundi 16/11", "Fiches de demande de modification de l'esquisse"),
                       ("U21", "Lundi 14/12", "Grilles du contrôle instructeur")],
            "transmet": [("U23", "Vendredi 27/11", "Maquette .rvt indicée pour Twinmotion"),
                         ("U21", "Vendredi 4/12 et 11/12", "Surfaces et pièces graphiques PDF pour le contrôle")],
            "livrables": ["Maquette .rvt et export .ifc", "PC01 plan de situation", "PC02 plan de masse",
                          "PC03 coupe", "PC05 façades", "Plan du rez-de-chaussée coté",
                          "Justification de la surface de plancher", "Détail à main levée"],
            "seances": [
                ("2026-11-13", "Ven. 13/11", "3 h", "Démarrer la maquette",
                 "Comment démarrer une maquette fiable à partir de l'esquisse ?",
                 ["Ouvrir le gabarit fourni et enregistrer la maquette selon la convention de nommage",
                  "Vérifier le fond de plan lié, les niveaux et le quadrillage",
                  "Modéliser les murs extérieurs et les cloisons de l'esquisse telle quelle"],
                 "Maquette indice A",
                 "Gabarit TEBAA_Villa · G01 Démarrer le projet · G02 Fond de plan · G03 Murs et cloisons"),
                ("2026-11-20", "Ven. 20/11", "3 h", "Modifications, plancher et menuiseries",
                 "Comment intégrer une demande de modification sans casser la maquette ?",
                 ["Appliquer les fiches de modification d'U21 et justifier la solution retenue",
                  "Modéliser le plancher bas et la dalle du garage",
                  "Placer menuiseries et équipements, renseigner les repères"],
                 "Maquette indice B · Fiches de modification visées",
                 "G04 Plancher bas · G06 Menuiseries et équipements · Fiches de modification"),
                ("2026-11-27", "Ven. 27/11", "3 h", "Toiture et contrôle",
                 "La maquette est-elle conforme au PLU et exploitable par les autres pôles ?",
                 ["Modéliser la toiture 4 pentes à 30 % en tuiles terre cuite, attacher les murs",
                  "Contrôler la maquette en 3D et en coupe avec la liste de contrôle",
                  "Transmettre la maquette à U23"],
                 "Maquette indice C transmise à U23",
                 "G05 Toiture 4 pentes · T4 Liste de contrôle de la maquette"),
                ("2026-12-04", "Ven. 4/12", "3 h", "Site, plan de masse et surfaces",
                 "Comment démontrer sur le plan de masse que l'implantation respecte le PLU ?",
                 ["Modéliser le terrain et les limites des parcelles, implanter la maison (reculs 3 m sur voie, H/2 et 3 m minimum en limites)",
                  "Vérifier la place de stationnement 2,5 × 5 m",
                  "Produire le plan de masse PC02 et le plan du RdC coté",
                  "Créer les pièces et la nomenclature de surface de plancher"],
                 "PC02 · Plan RdC · Nomenclature de surface de plancher",
                 "G07 Site et plan de masse · G08 Vues et cotation · G09 Pièces et surfaces · M03 Plan de masse"),
                ("2026-12-11", "Ven. 11/12", "3 h", "Façades, coupes et mises en page",
                 "Comment représenter les volumes du projet de façon lisible et conforme ?",
                 ["Annoter les 4 façades : matériaux, teintes, niveaux TN, égout, faîtage",
                  "Produire la coupe AA' et la coupe sur terrain",
                  "Mettre en page PC01, PC02, PC03, PC05 sur A3 avec cartouche et exporter en PDF"],
                 "PC01 · PC03 · PC05 (PDF)",
                 "R07 Coupes, façades, annotations · G11 Pièces graphiques du PC · M09 Feuilles"),
                ("2026-12-18", "Ven. 18/12", "3 h", "Corrections, détail et rendu",
                 "Le dossier graphique est-il prêt à être déposé ?",
                 ["Corriger les anomalies relevées au contrôle instructeur",
                  "Dessiner à main levée le détail du seuil de baie sans marche, échelle 1/5, matériaux désignés",
                  "Exporter la maquette en .ifc et en .rvt, déposer les livrables"],
                 "Rendu final : maquette, pièces graphiques, détail",
                 "Grille de validation d'U21 · Conventions de nommage"),
            ]},
    "u23": {"code": "U23", "nom": "Présentation et communication", "role": "Pôle image",
            "epreuve": "E23 · Élaboration d'éléments de présentation · pratique et écrit 4 h · coef. 2",
            "creneau": "Mercredi et jeudi 8 h 15 – 10 h 05", "volume": "≈ 20 h",
            "enseignant": "À définir",
            "competences": [
                ("C3.5", "Rédiger une notice architecturale", [
                    "La notice est claire, structurée et argumentée",
                    "Les choix architecturaux sont justifiés par rapport au programme et au site"]),
                ("C3.6", "Élaborer des éléments de présentation architecturale", [
                    "Les documents de présentation sont visuellement efficaces et professionnels",
                    "Les outils de représentation et de rendu sont adaptés"]),
                ("C3.7", "Réaliser une maquette d'étude", [
                    "La maquette est à l'échelle et cohérente avec les documents graphiques",
                    "Le travail est soigné, solide et adapté à la présentation"])],
            "recoit": [("U21", "Lundi 16/11", "Fiches de modification de l'esquisse"),
                       ("U21", "Lundi 23/11", "Règles d'aspect extérieur"),
                       ("U22", "Vendredi 27/11", "Maquette .rvt pour Twinmotion"),
                       ("U21", "Lundi 14/12", "Grilles du contrôle instructeur")],
            "transmet": [("U22", "Vendredi 27/11 (synthèse)", "Teintes et matériaux validés"),
                         ("U21", "Jeudi 10/12", "Notice PC04 pour le contrôle")],
            "livrables": ["Notice PC04", "Perspective conique en couleur", "Maquette d'étude au 1/100",
                          "Insertion PC06 sous Twinmotion", "Photos PC07 et PC08", "Planche de présentation A3"],
            "seances": [
                ("2026-11-12", "Jeu. 12/11", "1 h 50", "Analyse du site",
                 "Dans quel paysage la maison va-t-elle s'insérer ?",
                 ["Parcourir le site sur Street View, relever matériaux, teintes et volumes du voisinage",
                  "Choisir les points de vue des photos PC07 (proche) et PC08 (lointain) et les repérer sur le plan de situation"],
                 "Fiche d'analyse du site · Repérage PC07 et PC08",
                 "Plan cadastral · Street View · M06 PC04, PC06, PC07, PC08"),
                ("2026-11-18", "Mer. 18/11", "1 h 50", "Principes de la perspective",
                 "Comment représenter un volume tel que l'œil le perçoit ?",
                 ["Identifier ligne d'horizon, point de vue et points de fuite",
                  "S'entraîner sur des volumes simples en perspective conique à 2 points de fuite"],
                 "Exercices de perspective",
                 "Fiche méthode perspective (à créer)"),
                ("2026-11-19", "Jeu. 19/11", "1 h 50", "Construction de la perspective",
                 "Comment construire la perspective de la villa depuis la rue ?",
                 ["Placer le point de vue du futur PC06 sur le plan",
                  "Construire la perspective à partir du plan et des façades de l'esquisse",
                  "Intégrer les fiches de modification d'U21"],
                 "Perspective construite au crayon",
                 "Esquisse ESQ01 à ESQ03 · Fiches de modification"),
                ("2026-11-25", "Mer. 25/11", "1 h 50", "Mise au net de la perspective",
                 "La perspective est-elle juste et conforme aux règles d'aspect ?",
                 ["Mettre au net le trait, ajouter terrain, clôture, végétation",
                  "Vérifier la conformité avec les règles d'aspect transmises par U21"],
                 "Perspective mise au net",
                 "Note d'études U21"),
                ("2026-11-26", "Jeu. 26/11", "1 h 50", "Rendu couleur",
                 "Comment rendre lisibles matériaux et teintes pour le client ?",
                 ["Mettre en couleur : enduits gris clair et anthracite, tuiles terre cuite, menuiseries anthracite",
                  "Proposer la planche de teintes et matériaux validée en synthèse"],
                 "Perspective en couleur · Planche teintes et matériaux",
                 "Dossier client (souhaits architecturaux)"),
                ("2026-12-02", "Mer. 2/12", "1 h 50", "Maquette d'étude : volumes",
                 "Quels éléments représenter et à quelle échelle ?",
                 ["Établir les gabarits de découpe au 1/100",
                  "Découper et assembler les volumes et le socle du terrain"],
                 "Maquette en cours",
                 "Plans et façades de l'esquisse · Carton plume"),
                ("2026-12-03", "Jeu. 3/12", "1 h 50", "Maquette d'étude : finitions",
                 "La maquette est-elle cohérente avec les plans ?",
                 ["Réaliser la toiture 4 pentes et les finitions",
                  "Contrôler les cotes, photographier la maquette"],
                 "Maquette d'étude au 1/100 et sa photo",
                 "Plans de la maquette U22"),
                ("2026-12-09", "Mer. 9/12", "1 h 50", "Notice PC04",
                 "Comment présenter le parti architectural au service instructeur ?",
                 ["Décrire l'état initial et l'insertion du projet",
                  "Justifier matériaux, teintes, traitement des abords, accès, eaux pluviales"],
                 "Notice PC04 (transmise à U21 pour le contrôle)",
                 "Trame notice PC04 · M06 · Note d'études U21 · Rapport Géorisques"),
                ("2026-12-10", "Jeu. 10/12", "1 h 50", "Twinmotion : préparation",
                 "Comment passer de la maquette BIM à une image de présentation ?",
                 ["Importer la maquette Revit dans Twinmotion",
                  "Affecter les matériaux, placer végétation et éclairage"],
                 "Scène Twinmotion",
                 "Maquette U22 indice C · R10 Export 3D et insertion"),
                ("2026-12-16", "Mer. 16/12", "1 h 50", "Insertion paysagère PC06",
                 "Comment montrer le projet dans son environnement réel ?",
                 ["Caler la vue sur la photo du site, exporter l'image",
                  "Finaliser les photos PC07 et PC08"],
                 "PC06 · PC07 · PC08",
                 "R10 Export 3D et insertion · Photos du site"),
                ("2026-12-17", "Jeu. 17/12", "1 h 50", "Planche de présentation",
                 "Comment présenter le projet au client sur une seule planche ?",
                 ["Composer la planche A3 : perspective manuelle, rendu Twinmotion, photo de la maquette",
                  "Corriger selon la grille du contrôle instructeur"],
                 "Planche de présentation A3 · Rendu final",
                 "Grille de validation d'U21"),
            ]},
}

PLANNING = [
    ("S46", "9-13/11", "2026-11-09", "Lancement, acte de construire, dossier client, cadastre, Géoportail, Géorisques",
     "Mer. férié. Jeu. : analyse du site, Street View, points de vue PC07 et PC08",
     "Gabarit, fond de plan, niveaux, murs et cloisons de l'esquisse", "Synthèse 1 · 13/11"),
    ("S47", "16-20/11", "2026-11-16", "PLU zone UB, conformité de l'esquisse, fiches de modification",
     "Principes de la perspective, construction depuis la rue",
     "Intégration des modifications, plancher bas, menuiseries, équipements", ""),
    ("S48", "23-27/11", "2026-11-23", "Note d'études : réglementaire, fonctionnel, culturel",
     "Perspective : mise au net, rendu couleur",
     "Toiture 4 pentes, contrôle 3D, maquette transmise à U23", "Synthèse 2 · 27/11"),
    ("S49", "30/11-4/12", "2026-11-30", "Surfaces réglementaires, pleine terre",
     "Maquette d'étude au 1/100",
     "Terrain, implantation, plan de masse PC02, plan RdC, surfaces", ""),
    ("S50", "7-11/12", "2026-12-07", "Cerfa 13406, attestation RE2020",
     "Notice PC04, préparation Twinmotion",
     "Façades PC05, coupes PC03, plan de situation PC01, mises en page", "Synthèse 3 · 11/12"),
    ("S51", "14-18/12", "2026-12-14", "Contrôle instructeur croisé, comparaison des surfaces",
     "Insertion PC06, PC07, PC08, planche de présentation",
     "Corrections, détail à main levée, export IFC et natif", "Rendu final · 18/12"),
]

ECHANGES = [
    ("Lun. 16/11", "U21", "U22 et U23", "Non-conformités de l'esquisse : reculs, toiture, stationnement, pleine terre", "Fiche de demande de modification"),
    ("Lun. 23/11", "U21", "U23", "Règles d'aspect extérieur : façades, teintes, toiture, clôtures", "Note d'études"),
    ("Ven. 27/11", "U22", "U23", "Maquette pour Twinmotion", "Fichier .rvt indicé"),
    ("Lun. 14/12", "U21", "U22 et U23", "Anomalies relevées au contrôle instructeur", "Grille de validation du dossier PC"),
]

PIECES_PC = [
    ("Cerfa 13406", "Demande de permis de construire pour une maison individuelle", "U21"),
    ("PC01", "Plan de situation", "U22"),
    ("PC02", "Plan de masse", "U22"),
    ("PC03", "Plan en coupe du terrain et de la construction", "U22"),
    ("PC04", "Notice décrivant le terrain et le projet", "U23"),
    ("PC05", "Plans des façades et des toitures", "U22"),
    ("PC06", "Document graphique d'insertion du projet", "U23"),
    ("PC07", "Photographie de l'environnement proche", "U23"),
    ("PC08", "Photographie de l'environnement lointain", "U23"),
    ("PC16-1", "Attestation de prise en compte de la RE2020", "U21"),
]

PROGRAMME = [
    ("Séjour – salle à manger", "≈ 50 m²", "Grandes baies ouvrant sur le jardin et la terrasse"),
    ("Cuisine", "≈ 8 m²", "Ouverte sur le séjour, accès direct à la buanderie"),
    ("Buanderie", "≈ 4 m²", "Proche du garage"),
    ("Suite parentale", "≈ 25 m²", "Chambre, salle de bains, dressing, à l'écart des enfants"),
    ("Chambres enfants (×3)", "13 à 16 m² chacune", "Regroupées dans une même aile"),
    ("Salle d'eau", "≈ 9 m²", "Partagée par les chambres des enfants"),
    ("WC séparé", "≈ 2 m²", ""),
    ("Garage", "≈ 16 m²", "1 véhicule, accès direct à la maison"),
    ("Terrasse", "—", "Côté séjour, dans le prolongement des baies"),
    ("Piscine (option)", "≈ 8 × 4 m", "Extension pour les élèves en avance"),
]

DOCUMENTS = [
    ("Dossier client Villa DUPONT", "DOCX", "Toutes les séances"),
    ("Esquisse : plan RdC, façades, coupe AA (ESQ01 à ESQ03)", "PDF et DWG", "U21, U22, U23"),
    ("Plan cadastral et fond cadastral AD 276 – AD 277", "PDF et DWG", "U21, U22"),
    ("Informations littérales des parcelles", "PDF", "U21 (Cerfa)"),
    ("Règlement du PLUi, zone UB et lexique", "PDF", "U21, U22, U23"),
    ("Rapport Géorisques", "PDF", "U21, U23 (PC04)"),
    ("Données du bureau d'études thermiques", "Dossier client § 5", "U21 (PC16-1)"),
    ("Gabarit Revit TEBAA_Villa", "RTE", "U22"),
]

NAV = [("index.html", "Accueil"), ("dossier.html", "Dossier client"),
       ("u21.html", "U21"), ("u22.html", "U22"), ("u23.html", "U23")]

# ---------------------------------------------------------------- helpers
e = html.escape

def head(title):
    return (f'<title>{e(title)}</title>\n'
            '<meta name="claude:viewport-fit-sides" content="cover">\n'
            '<meta name="description" content="Projet fil rouge Terminale Bac Pro TEB-AA : villa DUPONT, Quillan.">\n'
            '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
            '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">\n'
            '<link rel="stylesheet" href="../assets/style.css">\n')

def header(active):
    links = "".join(
        f'<a href="{h}" class="nav-link{" is-active" if h == active else ""}{" pole-" + h[:3] if h.startswith("u2") else ""}"'
        f'{" aria-current=\"page\"" if h == active else ""}>{e(t)}</a>'
        for h, t in NAV)
    return f'''<header class="site-header">
  <div class="wrap header-inner">
    <a href="index.html" class="brand">
      <span class="brand-mark" aria-hidden="true">PC</span>
      <span class="brand-text"><strong>Projet Villa</strong><span>Terminale TEB-AA</span></span>
    </a>
    <nav class="nav" aria-label="Navigation principale"><a href="../index.html" class="nav-link">← Classe</a>{links}</nav>
  </div>
</header>'''

def cartouche():
    return f'''<footer class="site-footer">
  <div class="wrap">
    <table class="cartouche" aria-label="Cartouche du projet">
      <tr><th>Projet</th><td>Construction d'une maison individuelle – {e(PROJET["titre"])}</td><th>Indice</th><td class="mono">A</td></tr>
      <tr><th>Adresse</th><td>{e(PROJET["adresse"])} · parcelles {e(PROJET["parcelles"])}</td><th>Date</th><td class="mono">04/11/2026</td></tr>
      <tr><th>Classe</th><td>Terminale Bac Pro Technicien d'études du bâtiment, option assistant en architecture</td><th>Rendu</th><td class="mono">18/12/2026</td></tr>
    </table>
  </div>
</footer>'''

def page(fname, title, body, active, skeleton=True):
    inner = head(title) + "\n" + header(active) + "\n<main>\n" + body + "\n</main>\n" + cartouche() + SCRIPT
    if skeleton:
        return ('<!doctype html>\n<html lang="fr">\n<head>\n<meta charset="utf-8">\n'
                '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
                + head(title) + '</head>\n<body>\n' + header(active) + "\n<main>\n" + body +
                "\n</main>\n" + cartouche() + SCRIPT + "\n</body>\n</html>\n")
    return inner

SCRIPT = '''
<script>
(function(){
  // Met en évidence la semaine et les séances en cours
  var today = new Date(); today.setHours(0,0,0,0);
  document.querySelectorAll('[data-week]').forEach(function(row){
    var start = new Date(row.getAttribute('data-week') + 'T00:00:00');
    var end = new Date(start); end.setDate(end.getDate() + 6);
    if (today >= start && today <= end) row.classList.add('is-now');
  });
  var next = null;
  document.querySelectorAll('[data-date]').forEach(function(card){
    var d = new Date(card.getAttribute('data-date') + 'T00:00:00');
    if (d < today) card.classList.add('is-past');
    else if (!next) { next = card; card.classList.add('is-next'); }
  });
})();
</script>'''

def ul(items, cls=""):
    return f'<ul class="{cls}">' + "".join(f"<li>{e(i)}</li>" for i in items) + "</ul>"

def table(headers, rows, cls="", numeric=None):
    th = "".join(f"<th scope=\"col\">{e(h)}</th>" for h in headers)
    body = ""
    for r in rows:
        body += "<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>"
    return f'<div class="table-scroll"><table class="data {cls}"><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>'

def pole_tag(code):
    c = code.lower()[:3]
    return f'<span class="tag tag-{c}">{e(code)}</span>' if c in POLES else e(code)

def tags(text):
    return " ".join(pole_tag(t.strip()) if t.strip() in ("U21", "U22", "U23") else e(t) for t in text.replace(" et ", ",").split(",")) if any(u in text for u in ("U21","U22","U23")) else e(text)

# ---------------------------------------------------------------- pages
def page_index():
    poles = ""
    for k, p in POLES.items():
        poles += f'''<a class="pole-card pole-{k}" href="{k}.html">
  <span class="pole-code">{p["code"]}</span>
  <span class="pole-name">{e(p["nom"])}</span>
  <span class="pole-role">{e(p["role"])}</span>
  <dl class="kv">
    <div><dt>Créneau</dt><dd>{e(p["creneau"])}</dd></div>
    <div><dt>Volume</dt><dd>{e(p["volume"])}</dd></div>
    <div><dt>Compétences</dt><dd class="mono">{" · ".join(c[0] for c in p["competences"])}</dd></div>
    <div><dt>Enseignant</dt><dd>{e(p["enseignant"])}</dd></div>
  </dl>
  <span class="pole-go">Voir les séances</span>
</a>'''
    rows = ""
    for s, d, start, a, b, c, syn in PLANNING:
        syn_html = f'<span class="milestone{" is-final" if "Rendu" in syn else ""}">{e(syn)}</span>' if syn else ""
        rows += (f'<tr data-week="{start}"><th scope="row"><span class="mono">{s}</span><small>{d}</small></th>'
                 f'<td>{e(a)}</td><td>{e(b)}</td><td>{e(c)}</td><td>{syn_html}</td></tr>')
    plan = f'''<div class="table-scroll"><table class="data planning">
<thead><tr><th scope="col">Semaine</th><th scope="col" class="h-u21">Lundi · U21</th><th scope="col" class="h-u23">Mer. et jeu. · U23</th><th scope="col" class="h-u22">Vendredi · U22</th><th scope="col">Jalon</th></tr></thead>
<tbody>{rows}</tbody></table></div>'''
    ech = table(["Échéance", "De", "Vers", "Contenu", "Support"],
                [(f'<span class="mono">{e(a)}</span>', tags(b), tags(c), e(d), e(f)) for a, b, c, d, f in ECHANGES])
    pc = table(["Pièce", "Intitulé", "Pôle"], [(f'<span class="mono">{e(a)}</span>', e(b), pole_tag(c)) for a, b, c in PIECES_PC])
    body = f'''
<section class="hero wrap">
  <p class="eyebrow">Projet d'introduction · Terminale · 6 semaines</p>
  <h1>Villa DUPONT, Quillan</h1>
  <p class="lead">Vous êtes technicien(ne) d'études dans une agence de maîtrise d'œuvre. M. et Mme DUPONT veulent faire construire leur maison de plain-pied avec garage. L'agence doit déposer le permis de construire : trois pôles y travaillent en même temps.</p>
  <dl class="facts">
    <div><dt>Terrain</dt><dd>{e(PROJET["parcelles"])} · {e(PROJET["surface"])}</dd></div>
    <div><dt>Zonage</dt><dd>Zone {e(PROJET["zone"])} du PLUi</dd></div>
    <div><dt>Objectif</dt><dd>Dossier de permis de construire complet</dd></div>
    <div><dt>Rendu</dt><dd>{e(PROJET["rendu"])}</dd></div>
  </dl>
</section>

<section class="wrap section">
  <h2>Les trois pôles de l'agence</h2>
  <p class="section-lead">Chaque pôle correspond à une unité du diplôme. Les trois avancent en parallèle et s'échangent des informations à dates fixes.</p>
  <div class="poles">{poles}</div>
</section>

<section class="wrap section">
  <h2>Planning</h2>
  <p class="section-lead">La semaine en cours est surlignée. Les synthèses du vendredi (1 h) réunissent les trois pôles.</p>
  {plan}
</section>

<section class="wrap section two-col">
  <div>
    <h2>Échanges entre pôles</h2>
    <p class="section-lead">Une transmission en retard bloque le pôle suivant : respectez ces dates.</p>
    {ech}
  </div>
  <div>
    <h2>Pièces du permis de construire</h2>
    <p class="section-lead">Le rendu final rassemble ces pièces, dans l'ordre du bordereau du Cerfa.</p>
    {pc}
  </div>
</section>
'''
    return body

def page_dossier():
    prog = table(["Local", "Surface souhaitée", "Exigences du client"],
                 [(e(a), f'<span class="mono">{e(b)}</span>', e(c)) for a, b, c in PROGRAMME])
    docs = table(["Document", "Format", "Utilisé par"], [(e(a), e(b), tags(c)) for a, b, c in DOCUMENTS])
    body = f'''
<section class="hero wrap">
  <p class="eyebrow">Données d'entrée · commun aux trois pôles</p>
  <h1>Dossier client</h1>
  <p class="lead">M. et Mme DUPONT, couple avec trois enfants, souhaitent une maison de plain-pied, lumineuse, ouverte sur le jardin et sans aucune marche entre les pièces. Les analyses ne sont pas données : c'est à vous de les réaliser.</p>
</section>

<section class="wrap section two-col">
  <div>
    <h2>Le terrain</h2>
    <dl class="kv kv-block">
      <div><dt>Adresse</dt><dd>{e(PROJET["adresse"])}</dd></div>
      <div><dt>Cadastre</dt><dd>Section AD, parcelles 276 (1 271 m²) et 277 (1 278 m²)</dd></div>
      <div><dt>Urbanisme</dt><dd>{e(PROJET["plu"])}, zone UB</dd></div>
      <div><dt>Topographie</dt><dd>Terrain considéré comme plat, TN à −0,20 m du sol fini du RdC</dd></div>
      <div><dt>Réseaux</dt><dd>Eau, assainissement collectif, électricité, télécom en limite de terrain</dd></div>
      <div><dt>Eaux pluviales</dt><dd>Pas de réseau public : gestion à la parcelle</dd></div>
    </dl>
  </div>
  <div>
    <h2>Souhaits architecturaux</h2>
    {ul(["Toiture à 4 pentes en tuiles, conforme aux règles de la commune",
         "Façades enduites en deux teintes : gris clair et gris anthracite",
         "Menuiseries gris anthracite, volets roulants à coffres intégrés",
         "Jardin le plus végétalisé possible, clôture discrète, portail coulissant",
         "Maison économe en énergie, chauffage par pompe à chaleur"], "list")}
  </div>
</section>

<section class="wrap section">
  <h2>Programme</h2>
  <p class="section-lead">Surfaces indicatives à comparer aux surfaces réellement obtenues dans l'esquisse.</p>
  {prog}
</section>

<section class="wrap section">
  <h2>Documents fournis</h2>
  {docs}
</section>

<section class="wrap section two-col">
  <div>
    <h2>Conventions de nommage</h2>
    <dl class="kv kv-block">
      <div><dt>Maquette</dt><dd class="mono">TEBAA_NOM_Prenom_Villa.rvt</dd></div>
      <div><dt>Pièces PDF</dt><dd class="mono">NOM_Prenom_PC02_Plan-de-masse.pdf</dd></div>
      <div><dt>Indice</dt><dd>A à la création, puis B, C… à chaque modification transmise</dd></div>
    </dl>
  </div>
  <div>
    <h2>Arborescence de votre dossier</h2>
<pre class="tree mono">NOM_Prenom_Villa/
├─ 01_Ressources/
├─ 02_Maquette/
└─ 03_Livrables/
   ├─ U21/
   ├─ U22/
   └─ U23/</pre>
  </div>
</section>

<section class="wrap section">
  <h2>Registre des modifications</h2>
  <p class="section-lead">À tenir à jour par chaque élève : toute modification transmise d'un pôle à l'autre y figure.</p>
  {table(["Indice", "Date", "Pôle émetteur", "Pièce concernée", "Modification"],
         [('<span class="mono">A</span>', '<span class="mono">13/11</span>', pole_tag("U22"), "Maquette", "Création à partir de l'esquisse"),
          ('<span class="mono">B</span>', '<span class="mono">20/11</span>', pole_tag("U21"), "Maquette", "Exemple : recul porté à 3 m sur la voie"),
          ('<span class="mono">…</span>', "", "", "", "")], "register")}
</section>
'''
    return body

def page_pole(k):
    p = POLES[k]
    comps = ""
    for code, nom, inds in p["competences"]:
        comps += f'<div class="comp"><p class="comp-code mono">{code}</p><h3>{e(nom)}</h3>{ul(inds, "checks")}</div>'
    seances = ""
    for i, (iso, date, duree, titre, prob, act, livr, res) in enumerate(p["seances"], 1):
        seances += f'''<article class="seance" data-date="{iso}" id="s{i}">
  <header class="seance-head">
    <p class="seance-date"><span class="mono">{e(date)}</span><span>{e(duree)}</span></p>
    <h3><span class="seance-num mono">{p["code"]}-{i:02d}</span> {e(titre)}</h3>
    <span class="badge-next">Prochaine séance</span>
  </header>
  <p class="prob">{e(prob)}</p>
  <div class="seance-grid">
    <div><p class="label">On demande</p>{ul(act, "list")}</div>
    <div class="seance-side">
      <p class="label">Livrables</p><p>{e(livr)}</p>
      <p class="label">Ressources</p><p class="res">{e(res)}</p>
    </div>
  </div>
</article>'''
    rec = table(["De", "Quand", "Contenu"], [(tags(a), f'<span class="mono">{e(b)}</span>', e(c)) for a, b, c in p["recoit"]])
    tra = table(["Vers", "Quand", "Contenu"], [(tags(a), f'<span class="mono">{e(b)}</span>', e(c)) for a, b, c in p["transmet"]])
    body = f'''
<section class="hero wrap hero-{k}">
  <p class="eyebrow">{e(p["epreuve"])}</p>
  <h1><span class="code-big">{p["code"]}</span> {e(p["nom"])}</h1>
  <p class="lead">{e(p["role"])}.</p>
  <dl class="facts">
    <div><dt>Créneau</dt><dd>{e(p["creneau"])}</dd></div>
    <div><dt>Volume</dt><dd>{e(p["volume"])}</dd></div>
    <div><dt>Séances</dt><dd>{len(p["seances"])}</dd></div>
    <div><dt>Enseignant</dt><dd>{e(p["enseignant"])}</dd></div>
  </dl>
</section>

<section class="wrap section">
  <h2>Compétences évaluées</h2>
  <div class="comps">{comps}</div>
</section>

<section class="wrap section pole-{k}">
  <h2>Séances</h2>
  <p class="section-lead">La prochaine séance est signalée ; les séances passées sont atténuées.</p>
  <div class="seances">{seances}</div>
</section>

<section class="wrap section two-col">
  <div><h2>Je reçois</h2>{rec}</div>
  <div><h2>Je transmets</h2>{tra}</div>
</section>

<section class="wrap section">
  <h2>Livrables évalués</h2>
  {ul(p["livrables"], "deliverables")}
</section>
'''
    return body

PAGES = [
    ("index.html", "Projet Villa DUPONT", page_index),
    ("dossier.html", "Dossier client – Villa DUPONT", page_dossier),
    ("u21.html", "U21 – Villa DUPONT", lambda: page_pole("u21")),
    ("u22.html", "U22 – Villa DUPONT", lambda: page_pole("u22")),
    ("u23.html", "U23 – Villa DUPONT", lambda: page_pole("u23")),
]

def build():
    """Écrit les pages de la Villa dans ce dossier (villa/). Le style est partagé : ../assets/style.css"""
    for fname, title, fn in PAGES:
        with open(os.path.join(ROOT, fname), "w", encoding="utf-8") as f:
            f.write(page(fname, title, fn(), fname, True))

if __name__ == "__main__":
    build()
    print("ok")
