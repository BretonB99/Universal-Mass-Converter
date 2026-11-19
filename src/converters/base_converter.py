import os
from abc import ABC, abstractmethod

class BaseConverter(ABC):
    """Classe de base dont héritent tous les convertisseurs spécifiques."""

    def __init__(self, dossier_source: str, ext_source: str, ext_cible: str):
        self.dossier_source = dossier_source
        self.ext_source = ext_source.lower()
        self.ext_cible = ext_cible.lower()
        
        # Crée un sous-dossier propre pour ne pas mélanger les originaux et les convertis
        nom_dossier_sortie = f"convertis_{self.ext_cible.lstrip('.')}"
        self.dossier_sortie = os.path.join(self.dossier_source, nom_dossier_sortie)
        os.makedirs(self.dossier_sortie, exist_ok=True)

    def construire_chemin_sortie(self, chemin_fichier_source: str) -> str:
        """Génère le chemin complet du fichier converti dans le dossier de sortie."""
        nom_fichier = os.path.basename(chemin_fichier_source)
        nom_sans_ext = os.path.splitext(nom_fichier)[0]
        return os.path.join(self.dossier_sortie, f"{nom_sans_ext}{self.ext_cible}")

    @abstractmethod
    def convertir_fichier(self, chemin_source: str) -> tuple[bool, str]:
        """
        Convertit un fichier unique.
        Doit retourner (True, chemin_sortie) en cas de succès,
        ou (False, message_erreur) en cas d'échec.
        """
        pass
