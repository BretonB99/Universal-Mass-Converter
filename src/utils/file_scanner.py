import os
from collections import Counter
from config.formats import obtenir_dictionnaire_plat

def scanner_dossier(chemin_dossier: str, inclure_sous_dossiers: bool = False) -> dict[str, int]:
    """
    Analyse un dossier et retourne un dictionnaire {extension: nombre_de_fichiers}
    uniquement pour les extensions supportées par le logiciel.
    """
    formats_supportes = obtenir_dictionnaire_plat()
    compteur = Counter()

    if not os.path.isdir(chemin_dossier):
        return {}

    if inclure_sous_dossiers:
        for racine, _, fichiers in os.walk(chemin_dossier):
            for fichier in fichiers:
                ext = _extraire_extension(fichier)
                if ext in formats_supportes:
                    compteur[ext] += 1
    else:
        for fichier in os.listdir(chemin_dossier):
            chemin_complet = os.path.join(chemin_dossier, fichier)
            if os.path.isfile(chemin_complet):
                ext = _extraire_extension(fichier)
                if ext in formats_supportes:
                    compteur[ext] += 1

    return dict(sorted(compteur.items()))

def _extraire_extension(nom_fichier: str) -> str:
    """Gère les extensions simples (.png) et doubles (.tar.gz)."""
    nom_lower = nom_fichier.lower()
    if nom_lower.endswith(".tar.gz"):
        return ".tar.gz"
    return os.path.splitext(nom_lower)[1]
