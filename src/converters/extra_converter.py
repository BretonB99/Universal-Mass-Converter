import os
import json
import shutil
import tempfile
import zipfile
import tarfile
import py7zr
import trimesh
import gpxpy
from fontTools.ttLib import TTFont
from converters.base_converter import BaseConverter

class ExtraConverter(BaseConverter):
    """Gère les Archives, les Polices d'écriture, la 3D et les fichiers GPS."""

    ARCHIVES = {".zip", ".7z", ".tar", ".tar.gz"}
    POLICES = {".ttf", ".otf", ".woff", ".woff2"}
    MODELES_3D = {".stl", ".obj", ".ply", ".glb"}
    GPS = {".gpx", ".kml", ".geojson"}

    def convertir_fichier(self, chemin_source: str) -> tuple[bool, str]:
        chemin_sortie = self.construire_chemin_sortie(chemin_source)

        try:
            if self.ext_source in self.ARCHIVES:
                self._convertir_archive(chemin_source, chemin_sortie)
            elif self.ext_source in self.POLICES:
                self._convertir_police(chemin_source, chemin_sortie)
            elif self.ext_source in self.MODELES_3D:
                maillage = trimesh.load(chemin_source)
                maillage.export(chemin_sortie)
            elif self.ext_source in self.GPS:
                self._convertir_gps(chemin_source, chemin_sortie)

            return True, chemin_sortie

        except Exception as e:
            return False, f"Erreur conversion spécialisée ({chemin_source}) : {str(e)}"

    def _convertir_archive(self, source: str, sortie: str):
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Extraction
            if self.ext_source == ".zip":
                with zipfile.ZipFile(source, "r") as z:
                    z.extractall(tmp_dir)
            elif self.ext_source == ".7z":
                with py7zr.SevenZipFile(source, mode="r") as z:
                    z.extractall(tmp_dir)
            elif self.ext_source in {".tar", ".tar.gz"}:
                with tarfile.open(source, "r:*") as t:
                    t.extractall(tmp_dir)

            # Recompression
            if self.ext_cible == ".zip":
                shutil.make_archive(sortie.removesuffix(".zip"), "zip", tmp_dir)
            elif self.ext_cible == ".tar":
                shutil.make_archive(sortie.removesuffix(".tar"), "tar", tmp_dir)
            elif self.ext_cible == ".tar.gz":
                shutil.make_archive(sortie.removesuffix(".tar.gz"), "gztar", tmp_dir)
            elif self.ext_cible == ".7z":
                with py7zr.SevenZipFile(sortie, "w") as z:
                    z.writeall(tmp_dir, arcname="")

    def _convertir_police(self, source: str, sortie: str):
        police = TTFont(source)
        if self.ext_cible in {".woff", ".woff2"}:
            police.flavor = self.ext_cible.lstrip(".")
        else:
            police.flavor = None
        police.save(sortie)

    def _convertir_gps(self, source: str, sortie: str):
        if self.ext_source == ".gpx":
            with open(source, "r", encoding="utf-8") as f:
                gpx = gpxpy.parse(f)
            points = [(p.longitude, p.latitude) for track in gpx.tracks for seg in track.segments for p in seg.points]
            if self.ext_cible == ".geojson":
                geojson = {
                    "type": "FeatureCollection",
                    "features": [{"type": "Feature", "geometry": {"type": "LineString", "coordinates": points}, "properties": {}}]
                }
                with open(sortie, "w", encoding="utf-8") as f:
                    json.dump(geojson, f, indent=2)
            elif self.ext_cible == ".csv":
                with open(sortie, "w", encoding="utf-8") as f:
                    f.write("longitude,latitude\n" + "\n".join(f"{lon},{lat}" for lon, lat in points))
