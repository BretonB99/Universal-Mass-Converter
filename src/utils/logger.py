import os
from datetime import datetime

class ConversionLogger:
    """Enregistre un rapport clair de la conversion dans le dossier de sortie."""

    def __init__(self, dossier_cible: str):
        self.chemin_log = os.path.join(dossier_cible, "rapport_conversion.txt")
        self.lignes = [
            f"=== RAPPORT DE CONVERSION ({datetime.now().strftime('%d/%m/%Y %H:%M:%S')}) ===\n"
        ]

    def ajouter_succes(self, fichier_source: str, fichier_sortie: str):
        self.lignes.append(f"[OK]     {os.path.basename(fichier_source)} -> {os.path.basename(fichier_sortie)}")

    def ajouter_erreur(self, fichier_source: str, raison: str):
        self.lignes.append(f"[ERREUR] {os.path.basename(fichier_source)} : {raison}")

    def sauvegarder(self):
        with open(self.chemin_log, "w", encoding="utf-8") as f:
            f.write("\n".join(self.lignes) + "\n")
