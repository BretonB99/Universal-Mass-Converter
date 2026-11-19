import shutil

# Détection automatique des moteurs externes sur le système
FFMPEG_DISPONIBLE = shutil.which("ffmpeg") is not None
CALIBRE_DISPONIBLE = shutil.which("ebook-convert") is not None

# Matrice complète classée par catégorie
CATALOGUE_FORMATS = {
    "Images & Icônes": {
        ".png": [".jpg", ".webp", ".bmp", ".tiff", ".ico", ".pdf"],
        ".jpg": [".png", ".webp", ".bmp", ".tiff", ".ico", ".pdf"],
        ".jpeg": [".png", ".webp", ".bmp", ".tiff", ".ico", ".pdf"],
        ".webp": [".png", ".jpg", ".bmp", ".ico", ".gif"],
        ".bmp": [".png", ".jpg", ".webp", ".ico"],
        ".tiff": [".png", ".jpg", ".webp", ".pdf"],
        ".ico": [".png", ".jpg", ".webp"],
        ".heic": [".jpg", ".png", ".webp", ".pdf"],
        ".heif": [".jpg", ".png", ".webp", ".pdf"],
        ".svg": [".png", ".jpg", ".pdf", ".ico"],
        ".gif": [".mp4", ".webp", ".png"],
        ".cr2": [".jpg", ".png", ".tiff"],
        ".nef": [".jpg", ".png", ".tiff"],
        ".arw": [".jpg", ".png", ".tiff"],
        ".dng": [".jpg", ".png", ".tiff"],
    },
    "Vidéo": {
        ".mp4": [".mkv", ".avi", ".mov", ".webm", ".gif", ".mp3", ".wav", ".srt", ".vtt"],
        ".mkv": [".mp4", ".avi", ".mov", ".webm", ".mp3", ".wav", ".srt", ".vtt"],
        ".avi": [".mp4", ".mkv", ".mov", ".webm", ".mp3", ".srt"],
        ".mov": [".mp4", ".mkv", ".avi", ".webm", ".gif", ".mp3"],
        ".webm": [".mp4", ".mkv", ".avi", ".mp3", ".wav"],
        ".flv": [".mp4", ".mkv", ".mp3"],
        ".wmv": [".mp4", ".mkv", ".mp3"],
    },
    "Audio": {
        ".mp3": [".wav", ".ogg", ".flac", ".aac", ".m4a"],
        ".wav": [".mp3", ".ogg", ".flac", ".aac", ".m4a"],
        ".flac": [".mp3", ".wav", ".ogg", ".aac", ".m4a"],
        ".ogg": [".mp3", ".wav", ".flac", ".aac"],
        ".aac": [".mp3", ".wav", ".ogg", ".flac"],
        ".m4a": [".mp3", ".wav", ".ogg", ".flac"],
    },
    "Sous-titres": {
        ".srt": [".vtt", ".ass", ".ssa", ".txt"],
        ".vtt": [".srt", ".ass", ".txt"],
        ".ass": [".srt", ".vtt", ".txt"],
        ".ssa": [".srt", ".vtt", ".txt"],
        ".sub": [".srt", ".vtt"],
    },
    "Documents & E-books": {
        ".pdf": [".png", ".jpg", ".txt", ".docx", ".epub"],
        ".docx": [".pdf", ".txt", ".md", ".html", ".epub"],
        ".md": [".html", ".pdf", ".docx", ".txt"],
        ".html": [".md", ".pdf", ".txt"],
        ".txt": [".pdf", ".md", ".docx", ".epub"],
        ".epub": [".pdf", ".mobi", ".azw3", ".txt"],
        ".mobi": [".epub", ".pdf", ".txt"],
        ".azw3": [".epub", ".pdf", ".txt"],
    },
    "Données & Config": {
        ".csv": [".xlsx", ".json", ".xml", ".html", ".md"],
        ".xlsx": [".csv", ".json", ".xml", ".pdf"],
        ".json": [".yaml", ".xml", ".csv", ".toml"],
        ".yaml": [".json", ".xml", ".toml"],
        ".yml": [".json", ".xml", ".toml"],
        ".xml": [".json", ".yaml", ".csv"],
        ".toml": [".json", ".yaml"],
    },
    "Archives, Polices, 3D & GPS": {
        ".zip": [".tar", ".tar.gz", ".7z"],
        ".7z": [".zip", ".tar", ".tar.gz"],
        ".tar": [".zip", ".7z"],
        ".ttf": [".otf", ".woff", ".woff2"],
        ".otf": [".ttf", ".woff", ".woff2"],
        ".woff": [".ttf", ".otf"],
        ".woff2": [".ttf", ".otf"],
        ".stl": [".obj", ".ply", ".glb"],
        ".obj": [".stl", ".ply", ".glb"],
        ".gpx": [".kml", ".geojson", ".csv"],
        ".kml": [".gpx", ".geojson"],
    }
}

def obtenir_dictionnaire_plat() -> dict[str, list[str]]:
    """Fusionne toutes les catégories en un seul dictionnaire {extension: [sorties]}."""
    resultat = {}
    for formats in CATALOGUE_FORMATS.values():
        for ext_source, sorties in formats.items():
            # Filtre les formats Kindle si Calibre n'est pas installé
            if not CALIBRE_DISPONIBLE:
                sorties = [s for s in sorties if s not in (".mobi", ".azw3")]
            resultat[ext_source] = sorties
    return resultat

def obtenir_categorie(extension: str) -> str | None:
    """Retourne le nom de la catégorie d'une extension donnée."""
    ext = extension.lower()
    for categorie, formats in CATALOGUE_FORMATS.items():
        if ext in formats:
            return categorie
    return None
