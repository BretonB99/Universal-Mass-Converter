import subprocess
from config.formats import FFMPEG_DISPONIBLE
from converters.base_converter import BaseConverter

class MediaConverter(BaseConverter):
    """Gère l'audio, la vidéo, les GIF animés et l'extraction de sous-titres via FFmpeg."""

    def convertir_fichier(self, chemin_source: str) -> tuple[bool, str]:
        if not FFMPEG_DISPONIBLE:
            return False, "FFmpeg n'est pas installé ou introuvable sur le système."

        chemin_sortie = self.construire_chemin_sortie(chemin_source)

        try:
            # Cas 1 : Extraction de sous-titres depuis une vidéo (.mp4 / .mkv -> .srt / .vtt)
            if self.ext_cible in {".srt", ".vtt"}:
                commande = [
                    "ffmpeg", "-y", "-i", chemin_source,
                    "-map", "0:s:0", chemin_sortie
                ]
            # Cas 2 : Vidéo vers GIF animé de bonne qualité
            elif self.ext_cible == ".gif":
                commande = [
                    "ffmpeg", "-y", "-i", chemin_source,
                    "-vf", "fps=15,scale=480:-1:flags=lanczos",
                    chemin_sortie
                ]
            # Cas 3 : Conversion Audio ou Vidéo standard
            else:
                commande = [
                    "ffmpeg", "-y", "-i", chemin_source,
                    chemin_sortie
                ]

            # Exécution silencieuse sans ouvrir de fenêtre noire sous Windows
            creation_flags = subprocess.CREATE_NO_WINDOW if hasattr(subprocess, "CREATE_NO_WINDOW") else 0
            resultat = subprocess.run(
                commande,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=creation_flags
            )

            if resultat.returncode != 0:
                if self.ext_cible in {".srt", ".vtt"}:
                    return False, "Aucune piste de sous-titres intégrée trouvée dans cette vidéo."
                return False, f"Erreur FFmpeg : {resultat.stderr.splitlines()[-1]}"

            return True, chemin_sortie

        except Exception as e:
            return False, f"Erreur média ({chemin_source}) : {str(e)}"
