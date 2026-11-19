import io
from PIL import Image
import pillow_heif
import rawpy
from converters.base_converter import BaseConverter

# Import sécurisé de CairoSVG (évite le crash sous Windows si libcairo-2.dll est absent)
try:
    import cairosvg
    CAIRO_DISPONIBLE = True
except (ImportError, OSError):
    CAIRO_DISPONIBLE = False

# Active le support des photos Apple (.heic / .heif) dans Pillow
pillow_heif.register_heif_opener()

class ImageConverter(BaseConverter):
    """Gère les conversions d'images, icônes (.ico), SVG et fichiers RAW."""

    EXTENSIONS_RAW = {".cr2", ".nef", ".arw", ".dng"}

    def convertir_fichier(self, chemin_source: str) -> tuple[bool, str]:
        chemin_sortie = self.construire_chemin_sortie(chemin_source)

        try:
            # 1. Lecture de l'image source selon son type
            if self.ext_source == ".svg":
                if not CAIRO_DISPONIBLE:
                    return False, "La bibliothèque système Cairo (GTK) est requise sous Windows pour convertir les .svg."
                png_bytes = cairosvg.svg2png(url=chemin_source)
                img = Image.open(io.BytesIO(png_bytes))
            elif self.ext_source in self.EXTENSIONS_RAW:
                with rawpy.imread(chemin_source) as raw:
                    rgb = raw.postprocess()
                img = Image.fromarray(rgb)
            else:
                img = Image.open(chemin_source)

            # 2. Sauvegarde selon le format cible
            with img:
                if self.ext_cible == ".ico":
                    img_ico = img.convert("RGBA")
                    img_ico.save(
                        chemin_sortie,
                        format="ICO",
                        sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)]
                    )
                elif self.ext_cible in {".jpg", ".jpeg", ".bmp", ".pdf"}:
                    if img.mode in ("RGBA", "LA", "P"):
                        fond = Image.new("RGB", img.size, (255, 255, 255))
                        if img.mode == "P":
                            img = img.convert("RGBA")
                        fond.paste(img, mask=img.split()[-1])
                        img = fond
                    else:
                        img = img.convert("RGB")
                    
                    format_pil = "JPEG" if self.ext_cible in {".jpg", ".jpeg"} else self.ext_cible.lstrip(".").upper()
                    img.save(chemin_sortie, format=format_pil, quality=92)
                else:
                    format_pil = self.ext_cible.lstrip(".").upper()
                    img.save(chemin_sortie, format=format_pil)

            return True, chemin_sortie

        except Exception as e:
            return False, f"Erreur image ({chemin_source}) : {str(e)}"
