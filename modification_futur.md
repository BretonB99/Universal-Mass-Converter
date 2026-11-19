# 🗺️ Modifications futures & Feuille de route (Roadmap)

Ce document détaille la planification des prochaines évolutions d'**Universal Mass Converter**. Les correctifs mineurs (`v1.0.x`, `v1.1.x`...) seront publiés au fur et à mesure selon les besoins et retours d'utilisation.

---

## 🚀 Version 1.1.0 — Gestion avancée des fichiers et de l'interface
- [ ] **Mode sous-dossiers (Récursif)** : Case à cocher *« Inclure les sous-dossiers »* permettant de traiter toute une arborescence tout en recréant la même structure de dossiers à la sortie.
- [ ] **Glisser-déposer de fichiers multiples** : Autoriser le dépôt d'une sélection de fichiers individuels (en plus des dossiers complets).
- [ ] **Dossier de destination personnalisé** : Permettre de choisir un emplacement de sauvegarde spécifique plutôt que le sous-dossier par défaut (`convertis_...`).
- [ ] **Bouton « Ouvrir le dossier de sortie »** : Accès direct en un clic dans l'explorateur de fichiers dès la fin du traitement.
- [ ] **Bouton Annuler & Pause** : Interrompre proprement une file d'attente en cours sans fermer l'application.
- [ ] **Nettoyage sécurisé (Optionnel)** : Case à cocher (avec double confirmation) pour déplacer les fichiers d'origine vers la corbeille après une conversion réussie.
- [ ] **Renommage par lots intégré** : Ajouter un préfixe, un suffixe ou une numérotation automatique lors de la conversion.

---

## 💻 Version 1.2.0 — Langages de programmation & Développement Web
Ajout d'une nouvelle catégorie dédiée aux développeurs pour transcompiler, minifier ou exporter du code source en masse :
- [ ] **Web & Styles** :
  - `.ts` / `.tsx` (TypeScript) ➔ `.js` / `.jsx` (JavaScript)
  - `.scss` / `.sass` / `.less` ➔ `.css` (et minification `.min.css`)
  - `.pug` / `.ejs` ➔ `.html`
- [ ] **Notebooks & Scripts** :
  - `.ipynb` (Jupyter Notebook) ➔ `.py`, `.html`, `.pdf`, `.md`
- [ ] **Export de code documenté** :
  - `.py`, `.js`, `.cpp`, `.cs`, `.java`, `.rs`, `.go`, `.php` ➔ `.html` ou `.pdf` avec coloration syntaxique propre (via *Pygments*).
- [ ] **Données & Bases de données légères** :
  - `.sqlite` / `.db` ➔ `.csv`, `.xlsx`, `.json`, `.sql` (export complet des tables).
  - `.env` / `.ini` / `.properties` ➔ `.json`, `.yaml`, `.toml`.

---

## 🎨 Version 1.3.0 — Réglages de qualité, compression et métadonnées
- [ ] **Curseurs de qualité et débit** : Réglage du taux de compression (`.jpg`, `.webp`, `.avif`) et du bitrate audio/vidéo (`128 kbps`, `320 kbps`, `CRF`).
- [ ] **Redimensionnement et rotation en masse** : Appliquer une résolution maximale (ex. : `1920x1080`) ou un recadrage carré sur tout un dossier d'images.
- [ ] **Nouveaux formats images nouvelle génération** :
  - Ajout du support complet pour **`.avif`** et **`.jxl`** (JPEG XL) en entrée et en sortie.
  - Conversion d'images vers **`.psd`** (Photoshop) ou **`.eps`**.
- [ ] **Gestion des métadonnées (EXIF / ID3)** : Option pour supprimer les données GPS/EXIF des photos ou conserver les pochettes d'albums et artistes sur les fichiers audio.

---

## 🧠 Version 1.4.0 — Intelligence Artificielle locale (100 % Hors-Ligne)
- [ ] **Génération automatique de sous-titres (Whisper)** : Créer des fichiers `.srt`, `.vtt` ou `.txt` à partir des voix d'une vidéo ou d'un enregistrement audio sans piste de sous-titres intégrée.
- [ ] **Reconnaissance optique de caractères (OCR)** : Extraire le texte exploitable depuis des PDF scannés ou des photos de documents (`.png`, `.jpg`, `.pdf` ➔ `.txt`, `.docx`).
- [ ] **Suppression d'arrière-plan en masse** : Détourer automatiquement un dossier complet d'images (`.jpg` / `.png` ➔ `.png` transparent).

---

## 🛠️ Version 1.5.0 — Outils de fusion, découpage et bureautique
- [ ] **Fusion de fichiers** : Combiner tous les `.pdf` d'un dossier en un seul fichier, ou assembler plusieurs pistes `.mp3` / `.wav` bout à bout.
- [ ] **Découpage de PDF** : Extraire chaque page d'un PDF en fichiers `.pdf` individuels.
- [ ] **Bureautique LibreOffice & OpenDocument** :
  - `.odt` ➔ `.docx`, `.pdf`, `.txt`, `.md`
  - `.ods` ➔ `.xlsx`, `.csv`, `.json`
  - `.odp` / `.pptx` ➔ `.pdf` (export des diapositives).
- [ ] **Extraction vidéo avancée** : Extraire simultanément la piste audio, toutes les langues de sous-titres et des miniatures images d'une vidéo.

---

## 🎵 Version 1.6.0 — Formats spécialisés (Musique, CAO, Retro)
- [ ] **Musique & Partitions** :
  - `.mid` / `.midi` ➔ `.mp3`, `.wav` (synthèse audio via *FluidSynth*).
  - `.m3u` / `.pls` (Listes de lecture) ➔ `.json`, `.csv`, `.txt`.
- [ ] **CAO & Dessin technique** :
  - `.dxf` ➔ `.svg`, `.pdf`, `.png`.
- [ ] **Images disques & Archives avancées** :
  - `.iso` ➔ extraction ou conversion vers `.zip` / `.7z`.
  - `.rar` ➔ `.zip`, `.7z`, `.tar.gz`.

---

## 🌍 Version 2.0.0 — Multiplateforme, Thèmes et Automatisation
- [ ] **Support Multi-OS natif** : Distribution d'installateurs prêts à l'emploi pour **macOS** (`.dmg`) et **Linux** (`.AppImage` / `.deb`).
- [ ] **Profils de conversion (Presets)** : Enregistrer ses configurations favorites (ex. : *« Optimiser photos pour le Web »* ou *« Extraire l'audio des vidéos »*) pour les relancer en un clic.
- [ ] **Surveillance de dossier (Watch Folder)** : Convertir automatiquement tout nouveau fichier déposé dans un dossier surveillé en arrière-plan.
- [ ] **Interface personnalisable** : Sélecteur de langue (Français, Anglais, Espagnol, Allemand) et choix entre Mode Sombre, Mode Clair et Thème Système.

---

### 💡 Proposer une idée ou un format
Une extension manque à cette liste ? N'hésitez pas à ouvrir une **[Issue](../../issues)** sur ce dépôt pour suggérer une nouvelle conversion.
