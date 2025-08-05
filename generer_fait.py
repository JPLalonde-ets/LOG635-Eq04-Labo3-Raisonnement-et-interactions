from nltk import load_parser
from pprint import pprint

GRAMMAR_DIR = "grammars"

# Phrases soigneusement choisies pour déclencher les règles
phrases_grammars = [
    ("Gardien_de_phare_Red est mort", "personne_morte.fcfg"),
    ("Gardien_de_phare_Red est mort à 12h", "personne_morte_heure.fcfg"),
    ("Gardien_de_phare_Red a une marque au cou", "personne_marque.fcfg"),
    ("Capitaine_Gray était dans le phare à 12h", "personne_piece_heure.fcfg"),
    ("La corde est dans le phare", "arme_piece.fcfg")
]

valid_facts = []

for phrase, grammar_file in phrases_grammars:
    grammar_path = f"{GRAMMAR_DIR}/{grammar_file}"
    tokens = phrase.split()

    try:
        parser = load_parser(grammar_path, trace=0)
        trees = list(parser.parse(tokens))
        sems = [tree.label()['SEM'] for tree in trees if 'SEM' in tree.label()]

        if sems:
            for sem in sems:
                valid_facts.append(f"    expr('{sem}'),")
            print(f"✓ {phrase}")
        else:
            print(f"✗ Aucun fait trouvé pour : {phrase}")

    except Exception as e:
        print(f"✗ Erreur pour : {phrase} avec {grammar_file}")
        print(e)

# Écriture dans le fichier
with open("faits_generes.py", "w", encoding="utf-8") as f:
    f.write("from aima.utils import expr\n\n")
    f.write("def get_faits():\n")
    f.write("    return [\n")
    for fact in valid_facts:
        f.write(f"{fact}\n")
        print(fact)
    f.write("    ]\n")

print("\nFichier 'faits_generes.py' généré avec succès.")
