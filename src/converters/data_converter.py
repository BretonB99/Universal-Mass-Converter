import json
import tomllib
import tomli_w
import yaml
import xmltodict
import pandas as pd
from converters.base_converter import BaseConverter

class DataConverter(BaseConverter):
    """Gère les conversions entre CSV, Excel (XLSX), JSON, YAML, XML et TOML."""

    TABLEURS = {".csv", ".xlsx"}

    def convertir_fichier(self, chemin_source: str) -> tuple[bool, str]:
        chemin_sortie = self.construire_chemin_sortie(chemin_source)

        try:
            # 1. Conversions basées sur des tableaux (CSV, Excel, ou vers HTML/MD/JSON)
            if self.ext_source in self.TABLEURS:
                df = pd.read_csv(chemin_source) if self.ext_source == ".csv" else pd.read_excel(chemin_source)

                if self.ext_cible == ".csv":
                    df.to_csv(chemin_sortie, index=False)
                elif self.ext_cible == ".xlsx":
                    df.to_excel(chemin_sortie, index=False)
                elif self.ext_cible == ".json":
                    df.to_json(chemin_sortie, orient="records", indent=4, force_ascii=False)
                elif self.ext_cible == ".xml":
                    df.to_xml(chemin_sortie, index=False)
                elif self.ext_cible == ".html":
                    df.to_html(chemin_sortie, index=False)
                elif self.ext_cible == ".md":
                    with open(chemin_sortie, "w", encoding="utf-8") as f:
                        f.write(df.to_markdown(index=False))
                return True, chemin_sortie

            # 2. Conversions d'objets structurés (JSON, YAML, XML, TOML)
            donnees = self._charger_structure(chemin_source)

            if self.ext_cible == ".json":
                with open(chemin_sortie, "w", encoding="utf-8") as f:
                    json.dump(donnees, f, indent=4, ensure_ascii=False)
            elif self.ext_cible in {".yaml", ".yml"}:
                with open(chemin_sortie, "w", encoding="utf-8") as f:
                    yaml.safe_dump(donnees, f, allow_unicode=True, sort_keys=False)
            elif self.ext_cible == ".xml":
                racine = donnees if len(donnees) == 1 else {"root": donnees}
                with open(chemin_sortie, "w", encoding="utf-8") as f:
                    f.write(xmltodict.unparse(racine, pretty=True))
            elif self.ext_cible == ".toml":
                with open(chemin_sortie, "wb") as f:
                    tomli_w.dump(donnees, f)
            elif self.ext_cible == ".csv":
                df = pd.json_normalize(donnees)
                df.to_csv(chemin_sortie, index=False)

            return True, chemin_sortie

        except Exception as e:
            return False, f"Erreur données ({chemin_source}) : {str(e)}"

    def _charger_structure(self, chemin: str) -> dict:
        if self.ext_source == ".json":
            with open(chemin, "r", encoding="utf-8") as f:
                return json.load(f)
        elif self.ext_source in {".yaml", ".yml"}:
            with open(chemin, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        elif self.ext_source == ".xml":
            with open(chemin, "r", encoding="utf-8") as f:
                return xmltodict.parse(f.read())
        elif self.ext_source == ".toml":
            with open(chemin, "rb") as f:
                return tomllib.load(f)
        return {}
