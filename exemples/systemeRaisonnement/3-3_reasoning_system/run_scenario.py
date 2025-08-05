import os
import sys
from aima.logic import FolKB
from aima.utils import expr
from nltk import load_parser

# --- Configuration du chemin
racine = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, racine)
GRAMMAR_DIR = os.path.join(racine, "grammars")

from faits_generes import get_faits

# --- Initialisation de la base de connaissances
kb = FolKB()

# --- Chargement des faits initiaux
for fait in get_faits():
    kb.tell(fait)

# --- Règles de déduction
kb.tell(expr("EstMort(x) ==> Victime(x)"))
kb.tell(expr("MarqueCou(x) ==> ArmeCrime(Corde)"))
kb.tell(expr("Personne_Piece_Heure(x, Phare, 12) ==> Suspect(x)"))
kb.tell(expr("Personne_Piece_Heure(x, Phare, 12) ==> Possede(x, Corde)"))
kb.tell(expr("(Possede(x, Corde) & ArmeCrime(Corde)) ==> SuspectArme(x, Corde)"))
kb.tell(expr("(Suspect(x) & Possede(x, a) & ArmeCrime(a)) ==> Coupable(x)"))

# --- Sélection de la grammaire appropriée
def choisir_grammaire(phrase):
    phrase = phrase.lower()
    if "mort à" in phrase:
        return "personne_morte_heure.fcfg"
    elif "mort" in phrase:
        return "personne_morte.fcfg"
    elif "marque" in phrase:
        return "personne_marque.fcfg"
    elif any(arme in phrase for arme in ["corde", "couteau", "fusil", "clé", "cle", "matraque", "poison"]):
        return "arme_piece.fcfg"
    elif "était dans" in phrase or "est dans" in phrase or "se trouve" in phrase:
        return "personne_piece_heure.fcfg"
    else:
        return None

# --- Lecture d'une phrase et ajout dans la KB
def lire_fait_francais():
    phrase = input("→ Saisis une phrase (ex: Capitaine_Gray était dans le phare à 12h) :\n> ").strip()
    grammar_file = choisir_grammaire(phrase)
    if not grammar_file:
        print("  Aucun fichier de grammaire trouvé pour cette phrase.")
        return

    grammar_path = os.path.join(GRAMMAR_DIR, grammar_file)
    tokens = phrase.split()

    try:
        parser = load_parser(f'file:{grammar_path}', trace=0)
        trees = list(parser.parse(tokens))
        sems = [tree.label()['SEM'] for tree in trees if 'SEM' in tree.label()]
        if sems:
            for sem in sems:
                print(f"  Fait reconnu : {sem}")
                kb.tell(expr(str(sem)))
        else:
            print("  Aucune sémantique détectée pour cette phrase.")
    except Exception as e:
        print(f"  Erreur d'analyse avec {grammar_file} : {e}")

# --- Affichage des résultats sans doublons
def afficher_resultats(titre, requete_expr, *cles):
    print(f"\n{titre} :")
    resultats = list(kb.ask_generator(expr(requete_expr)))
    if not resultats:
        print("  Aucun résultat trouvé.")
        return

    deja_vu = set()
    for res in resultats:
        valeurs = tuple(str(res.get(expr(cle), "inconnue")) for cle in cles)
        if valeurs not in deja_vu:
            deja_vu.add(valeurs)
            print("  - " + " ".join(valeurs))

# --- Interaction principale
print("Saisissez 5 faits (phrases en français) pour alimenter la base de connaissances :")
for i in range(5):
    print(f"\nFait {i + 1} sur 5")
    lire_fait_francais()

# --- Résultats
afficher_resultats("Possession d'arme", "Possede(x, Corde)", "x")
afficher_resultats("Suspects potentiels", "Suspect(x)", "x")
afficher_resultats("Arme du crime", "ArmeCrime(a)", "a")
afficher_resultats("Suspects avec arme du crime", "SuspectArme(x, a)", "x", "a")
afficher_resultats("Coupable", "Coupable(x)", "x")
