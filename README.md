# <img src="assets/icon.png" width="32" align="absmiddle" alt="Logo"> Universal Mass Converter v1.0.0

<p>
  <a href="LICENSE"><img src="assets/badge-mit.svg" alt="Licence MIT"></a>
  <img src="assets/badge-python.svg" alt="Python 3.10+">
  <img src="assets/badge-offline.svg" alt="100% Hors-Ligne">
  <img src="assets/badge-ui.svg" alt="Interface PySide6">
</p>

Convertisseur de fichiers en masse **100 % hors-ligne, gratuit et illimité**. Glissez un dossier pour détecter et convertir automatiquement les formats compatibles.

![Démonstration de l'application](assets/screenshot_video.gif)


---

## 🔒 Pourquoi utiliser ce logiciel plutôt qu'un site en ligne ?

* **Confidentialité totale** : Vos documents, photos et fichiers professionnels ne quittent jamais votre ordinateur.
* **Aucune limite** : Convertissez des centaines de fichiers ou plusieurs gigaoctets en une seule fois, sans file d'attente ni abonnement.
* **Rapidité native** : Exploite directement la puissance de votre processeur et de votre disque dur, sans temps d'envoi (upload).

---

## 🚀 Fonctionnalités principales

* **Détection intelligente** : Scanne le dossier sélectionné et affiche le nombre exact de fichiers compatibles par extension.
* **Menus dynamiques** : La liste des formats de sortie s'adapte automatiquement selon le format d'entrée choisi.
* **Traitement fluide** : Exécution en arrière-plan avec barre de progression en temps réel et génération d'un rapport (`rapport_conversion.txt`).
* **Large compatibilité (50+ formats)** :
  * **Images & Icônes** : `.png`, `.jpg`, `.webp`, `.bmp`, `.tiff`, `.ico`, `.heic` (iPhone), `.svg`, `.gif`, et photos RAW (`.cr2`, `.nef`, `.arw`, `.dng`).
  * **Vidéo & Audio** : `.mp4`, `.mkv`, `.avi`, `.mov`, `.webm`, `.mp3`, `.wav`, `.flac`, `.ogg`, extraction audio et extraction de sous-titres (`.srt`, `.vtt`).
  * **Sous-titres** : `.srt`, `.vtt`, `.ass`, `.ssa`, `.sub`, `.txt`.
  * **Documents & E-books** : `.pdf`, `.docx`, `.md`, `.html`, `.txt`, `.epub` (ainsi que `.mobi`/`.azw3` si Calibre est installé).
  * **Données & Config** : `.csv`, `.xlsx`, `.json`, `.yaml`, `.xml`, `.toml`.
  * **Archives, Polices, 3D & GPS** : `.zip`, `.7z`, `.tar.gz`, `.ttf`, `.otf`, `.woff2`, `.stl`, `.obj`, `.gpx`, `.kml`.

<details>
<summary><b>📋 Cliquer pour afficher la liste complète des conversions (Entrée ➔ Sortie)</b></summary>

```text
1. IMAGES, PHOTOS & ICÔNES
- .png          -> .jpg, .webp, .bmp, .tiff, .ico, .pdf
- .jpg / .jpeg  -> .png, .webp, .bmp, .tiff, .ico, .pdf
- .webp         -> .png, .jpg, .bmp, .ico, .gif
- .bmp          -> .png, .jpg, .webp, .ico
- .tiff         -> .png, .jpg, .webp, .pdf
- .ico          -> .png, .jpg, .webp
- .heic / .heif -> .jpg, .png, .webp, .pdf
- .svg          -> .png, .jpg, .pdf, .ico
- .gif          -> .mp4, .webp, .png
- .cr2 / .nef / .arw / .dng -> .jpg, .png, .tiff

2. VIDÉO
- .mp4          -> .mkv, .avi, .mov, .webm, .gif, .mp3, .wav, .srt, .vtt
- .mkv          -> .mp4, .avi, .mov, .webm, .mp3, .wav, .srt, .vtt
- .avi          -> .mp4, .mkv, .mov, .webm, .mp3, .srt
- .mov          -> .mp4, .mkv, .avi, .webm, .gif, .mp3
- .webm         -> .mp4, .mkv, .avi, .mp3, .wav
- .flv / .wmv   -> .mp4, .mkv, .mp3

3. AUDIO
- .mp3          -> .wav, .ogg, .flac, .aac, .m4a
- .wav          -> .mp3, .ogg, .flac, .aac, .m4a
- .flac         -> .mp3, .wav, .ogg, .aac, .m4a
- .ogg          -> .mp3, .wav, .flac, .aac
- .aac / .m4a   -> .mp3, .wav, .ogg, .flac

4. SOUS-TITRES
- .srt          -> .vtt, .ass, .ssa, .txt
- .vtt          -> .srt, .ass, .txt
- .ass / .ssa   -> .srt, .vtt, .txt
- .sub          -> .srt, .vtt

5. DOCUMENTS & LIVRES NUMÉRIQUES
- .pdf          -> .png, .jpg, .txt, .docx, .epub
- .docx         -> .pdf, .txt, .md, .html, .epub
- .md           -> .html, .pdf, .docx, .txt
- .html         -> .md, .pdf, .txt
- .txt          -> .pdf, .md, .docx, .epub
- .epub         -> .pdf, .mobi, .azw3, .txt
- .mobi / .azw3 -> .epub, .pdf, .txt

6. DONNÉES & CONFIGURATION
- .csv          -> .xlsx, .json, .xml, .html, .md
- .xlsx         -> .csv, .json, .xml, .pdf
- .json         -> .yaml, .xml, .csv, .toml
- .yaml / .yml  -> .json, .xml, .toml
- .xml          -> .json, .yaml, .csv
- .toml         -> .json, .yaml

7. ARCHIVES, POLICES, 3D & GPS
- .zip          -> .tar, .tar.gz, .7z
- .7z           -> .zip, .tar, .tar.gz
- .tar / .tar.gz -> .zip, .7z
- .ttf          -> .otf, .woff, .woff2
- .otf          -> .ttf, .woff, .woff2
- .woff / .woff2 -> .ttf, .otf
- .stl          -> .obj, .ply, .glb
- .obj          -> .stl, .ply, .glb
- .gpx          -> .kml, .geojson, .csv
- .kml          -> .gpx, .geojson
```
</details>

---

## 📦 Installation et Utilisation

### Option 1 : Version prête à l'emploi (Windows)
1. Rendez-vous dans l'onglet **[Releases](https://github.com)** à droite de cette page.
2. Téléchargez **`UniversalMassConverter.exe`** et lancez-le directement (aucune installation de Python requise).

### Option 2 : Lancer depuis le code source
1. Récupérez le projet :
   * **Via Git** :
     ```bash
     git clone https://github.com
     cd Universal-Mass-Converter
     ```
   * **Via GitHub** : Cliquez sur le bouton vert **Code** > **Download ZIP**, extrayez l'archive puis ouvrez un terminal dans le dossier.
2. Installez les dépendances Python :
   ```bash
   pip install -r requirements.txt
   ```
3. Lancez l'application :
   ```bash
   python src/main.py
   ```

### Outils externes recommandés (Optionnels)
* **FFmpeg** : Nécessaire uniquement pour les conversions audio, vidéo et l'extraction de sous-titres (`winget install Gyan.FFmpeg` sous Windows) — [Voir le guide d'installation](docs/INSTALLATION_FFMPEG.md).
* **Calibre** : Nécessaire uniquement pour convertir vers ou depuis les formats Kindle (`.mobi`, `.azw3`).

---

<details>
<summary><b>📐 Cliquer pour voir l'arborescence du projet</b></summary>

```text
Universal-Mass-Converter/
├── src/
│   ├── __init__.py                 # Package principal
│   ├── main.py                     # Point d'entrée du logiciel
│   ├── config/
│   │   ├── __init__.py
│   │   └── formats.py              # Matrice des extensions (entrée -> sortie)
│   ├── ui/
│   │   ├── __init__.py
│   │   └── main_window.py          # Interface graphique dynamique (PySide6)
│   ├── converters/
│   │   ├── __init__.py
│   │   ├── base_converter.py       # Classe modèle commune
│   │   ├── image_converter.py      # Images & Icônes
│   │   ├── media_converter.py      # Audio, Vidéo & extraction sous-titres
│   │   ├── subtitle_converter.py   # Sous-titres
│   │   ├── document_converter.py   # Documents & Livres numériques
│   │   ├── data_converter.py       # Données & Configuration
│   │   └── extra_converter.py      # Archives, Polices, 3D, GPS
│   └── utils/
│       ├── __init__.py
│       ├── file_scanner.py         # Détection des extensions dans un dossier
│       └── logger.py               # Journalisation des opérations
├── tests/
│   ├── __init__.py
│   ├── test_formats.py
│   └── test_converters.py
├── assets/
│   ├── icon.ico
│   ├── logo.png
│   └── screenshot.png
├── docs/
│   └── INSTALLATION_FFMPEG.md
├── .gitignore
├── LICENSE
├── requirements.txt
├── pyproject.toml
└── README.md
```
</details>

---

## 🗺️ Évolutions prévues
Consultez le fichier [modification_futur.md](modification_futur.md) pour découvrir les fonctionnalités prévues dans les prochaines versions.

---

## 🗒️ Licence
Ce projet est distribué sous licence **MIT**. Voir le fichier [LICENSE](LICENSE) pour plus d'informations.
