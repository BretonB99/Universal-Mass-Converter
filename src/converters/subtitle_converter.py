import pysubs2
from converters.base_converter import BaseConverter

class SubtitleConverter(BaseConverter):
    """Gère les conversions de sous-titres (.srt, .vtt, .ass, .ssa, .sub) et l'export en .txt."""

    def convertir_fichier(self, chemin_source: str) -> tuple[bool, str]:
        chemin_sortie = self.construire_chemin_sortie(chemin_source)

        try:
            sous_titres = pysubs2.load(chemin_source, encoding="utf-8")

            # Export en texte brut sans les codes temporels (timecodes)
            if self.ext_cible == ".txt":
                lignes_texte = [ligne.plaintext.strip() for ligne in sous_titres if ligne.plaintext.strip()]
                with open(chemin_sortie, "w", encoding="utf-8") as f:
                    f.write("\n".join(lignes_texte))
            else:
                # Conversion directe supportée par pysubs2 (.srt, .vtt, .ass, .ssa)
                sous_titres.save(chemin_sortie)

            return True, chemin_sortie

        except UnicodeDecodeError:
            # Tentative de secours avec l'encodage Windows standard (latin-1)
            try:
                sous_titres = pysubs2.load(chemin_source, encoding="latin-1")
                sous_titres.save(chemin_sortie)
                return True, chemin_sortie
            except Exception as e:
                return False, f"Erreur d'encodage sous-titre : {str(e)}"
        except Exception as e:
            return False, f"Erreur sous-titre ({chemin_source}) : {str(e)}"
