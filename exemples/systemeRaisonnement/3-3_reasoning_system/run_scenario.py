import os
import sys
from aima.logic import FolKB
from aima.utils import expr

# Chemin vers le dossier racine
racine = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, racine)

from faits_generes import get_faits

# --- KB ---
kb = FolKB()

# --- Faits ---
print("Faits chargés :")
for fait in get_faits():
    print("  -", fait)
    kb.tell(fait)


# --- Règles ---
kb.tell(expr("EstMort(x) ==> Victime(x)"))
kb.tell(expr("MarqueCou(x) ==> ArmeCrime(Corde)"))
kb.tell(expr("Personne_Piece_Heure(x, Phare, 12) ==> Suspect(x)"))
kb.tell(expr("Personne_Piece_Heure(x, Phare, 12) ==> Possede(x, Corde)"))
kb.tell(expr("(Possede(x, Corde) & ArmeCrime(Corde)) ==> SuspectArme(x, Corde)"))
kb.tell(expr("(Suspect(x) & Possede(x, a) & ArmeCrime(a)) ==> Coupable(x)"))

def afficher_resultats(titre, requete_expr, *cles):
    print(f"{titre} :")
    resultats = list(kb.ask_generator(expr(requete_expr)))
    if not resultats:
        print("  Aucun résultat trouvé.")
        return
    for res in resultats:
        valeurs = [str(res.get(expr(cle), 'inconnue')) for cle in cles]

        print("  - " + " ".join(valeurs))


afficher_resultats("Possession d'arme", "Possede(x, Corde)", "x")
afficher_resultats("Suspects potentiels", "Suspect(x)", "x")
afficher_resultats("Arme du crime", "ArmeCrime(a)", "a")
afficher_resultats("Suspects avec arme du crime", "SuspectArme(x, a)", "x", "a")
afficher_resultats("Coupable", "Coupable(x)", "x")
