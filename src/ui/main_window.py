import os
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont, QDragEnterEvent, QDropEvent
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QComboBox, QProgressBar,
    QFileDialog, QMessageBox, QFrame
)

from config.formats import (
    FFMPEG_DISPONIBLE, CALIBRE_DISPONIBLE,
    obtenir_dictionnaire_plat, obtenir_categorie
)
from utils.file_scanner import scanner_dossier
from utils.logger import ConversionLogger
from converters.image_converter import ImageConverter
from converters.media_converter import MediaConverter
from converters.subtitle_converter import SubtitleConverter
from converters.document_converter import DocumentConverter
from converters.data_converter import DataConverter
from converters.extra_converter import ExtraConverter


STYLESHEET = """
QMainWindow {
    background-color: #18181b;
}
QLabel {
    color: #f4f4f5;
    font-family: 'Segoe UI', Arial, sans-serif;
}
QFrame#DropZone {
    background-color: #27272a;
    border: 2px dashed #52525b;
    border-radius: 12px;
}
QFrame#DropZone:hover {
    border-color: #3b82f6;
    background-color: #2e2e32;
}
QFrame#Card {
    background-color: #27272a;
    border-radius: 12px;
}
QPushButton {
    background-color: #3b82f6;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 18px;
    font-weight: bold;
    font-size: 13px;
}
QPushButton:hover {
    background-color: #2563eb;
}
QPushButton:disabled {
    background-color: #3f3f46;
    color: #71717a;
}
QPushButton#ActionBtn {
    background-color: #10b981;
    font-size: 15px;
    padding: 14px;
}
QPushButton#ActionBtn:hover {
    background-color: #059669;
}
QComboBox {
    background-color: #18181b;
    color: #ffffff;
    border: 1px solid #3f3f46;
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 14px;
    min-width: 170px;
}
QComboBox:hover {
    border-color: #3b82f6;
}
QComboBox:disabled {
    color: #71717a;
    border-color: #27272a;
}
QComboBox QAbstractItemView {
    background-color: #27272a;
    color: #ffffff;
    selection-background-color: #3b82f6;
    selection-color: #ffffff;
    border: 1px solid #3f3f46;
    outline: 0px;
}
QProgressBar {
    background-color: #27272a;
    border-radius: 6px;
    height: 12px;
    text-align: center;
    color: transparent;
}
QProgressBar::chunk {
    background-color: #10b981;
    border-radius: 6px;
}
"""
class ConversionWorker(QThread):
    """Exécute les conversions en arrière-plan pour ne pas figer l'interface."""
    progression = Signal(int, int, str)  # (actuel, total, nom_fichier)
    termine = Signal(int, int, str)      # (succes, erreurs, dossier_sortie)

    def __init__(self, dossier: str, ext_source: str, ext_cible: str):
        super().__init__()
        self.dossier = dossier
        self.ext_source = ext_source
        self.ext_cible = ext_cible

    def _selectionner_moteur(self):
        categorie = obtenir_categorie(self.ext_source)
        if categorie == "Images & Icônes":
            return ImageConverter(self.dossier, self.ext_source, self.ext_cible)
        elif categorie in {"Vidéo", "Audio"}:
            return MediaConverter(self.dossier, self.ext_source, self.ext_cible)
        elif categorie == "Sous-titres":
            return SubtitleConverter(self.dossier, self.ext_source, self.ext_cible)
        elif categorie == "Documents & E-books":
            return DocumentConverter(self.dossier, self.ext_source, self.ext_cible)
        elif categorie == "Données & Config":
            return DataConverter(self.dossier, self.ext_source, self.ext_cible)
        else:
            return ExtraConverter(self.dossier, self.ext_source, self.ext_cible)

    def run(self):
        moteur = self._selectionner_moteur()
        logger = ConversionLogger(moteur.dossier_sortie)

        fichiers = [
            os.path.join(self.dossier, f)
            for f in os.listdir(self.dossier)
            if os.path.isfile(os.path.join(self.dossier, f))
            and f.lower().endswith(self.ext_source)
        ]

        total = len(fichiers)
        succes = 0
        erreurs = 0

        for index, chemin in enumerate(fichiers, start=1):
            self.progression.emit(index, total, os.path.basename(chemin))
            ok, resultat = moteur.convertir_fichier(chemin)
            if ok:
                succes += 1
                logger.ajouter_succes(chemin, resultat)
            else:
                erreurs += 1
                logger.ajouter_erreur(chemin, resultat)

        logger.sauvegarder()
        self.termine.emit(succes, erreurs, moteur.dossier_sortie)
class DropZoneWidget(QFrame):
    """Zone permettant de glisser-déposer un dossier."""
    def __init__(self, callback_dossier):
        super().__init__()
        self.setObjectName("DropZone")
        self.setAcceptDrops(True)
        self.callback_dossier = callback_dossier

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(10)

        self.label_icone = QLabel("📁")
        self.label_icone.setFont(QFont("Segoe UI", 28))
        self.label_icone.setAlignment(Qt.AlignCenter)

        self.label_texte = QLabel("Glissez-déposez un dossier ici\nou cliquez sur le bouton ci-dessous")
        self.label_texte.setAlignment(Qt.AlignCenter)
        self.label_texte.setStyleSheet("color: #a1a1aa; font-size: 13px;")

        self.btn_parcourir = QPushButton("Parcourir les dossiers")
        self.btn_parcourir.setCursor(Qt.PointingHandCursor)
        self.btn_parcourir.clicked.connect(self.ouvrir_explorateur)

        layout.addWidget(self.label_icone)
        layout.addWidget(self.label_texte)
        layout.addWidget(self.btn_parcourir, alignment=Qt.AlignCenter)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls:
            chemin = urls[0].toLocalFile()
            if os.path.isdir(chemin):
                self.callback_dossier(chemin)
            else:
                QMessageBox.warning(self, "Erreur", "Veuillez déposer un dossier, pas un fichier isolé.")

    def ouvrir_explorateur(self):
        dossier = QFileDialog.getExistingDirectory(self, "Sélectionner le dossier à convertir")
        if dossier:
            self.callback_dossier(dossier)
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Universal Mass Converter")
        self.setFixedSize(700, 540)
        self.setStyleSheet(STYLESHEET)

        self.dossier_actuel = ""
        self.compatibilites = obtenir_dictionnaire_plat()
        self.worker = None

        self._initialiser_ui()

    def _initialiser_ui(self):
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        layout_principal = QVBoxLayout(widget_central)
        layout_principal.setContentsMargins(30, 25, 30, 25)
        layout_principal.setSpacing(18)

        # En-tête + Badges d'état
        header_layout = QHBoxLayout()
        titre = QLabel("Universal Mass Converter")
        titre.setFont(QFont("Segoe UI", 18, QFont.Bold))
        header_layout.addWidget(titre)
        header_layout.addStretch()

        badge_ffmpeg = QLabel("● FFmpeg prêt" if FFMPEG_DISPONIBLE else "● FFmpeg absent")
        badge_ffmpeg.setStyleSheet(f"color: {'#10b981' if FFMPEG_DISPONIBLE else '#ef4444'}; font-weight: bold;")
        header_layout.addWidget(badge_ffmpeg)

        badge_calibre = QLabel("● Calibre prêt" if CALIBRE_DISPONIBLE else "● Calibre absent")
        badge_calibre.setStyleSheet(f"color: {'#10b981' if CALIBRE_DISPONIBLE else '#71717a'}; margin-left: 10px;")
        header_layout.addWidget(badge_calibre)

        layout_principal.addLayout(header_layout)

        # 1. Zone de Glisser-Déposer
        self.drop_zone = DropZoneWidget(self.definir_dossier)
        self.drop_zone.setMinimumHeight(160)
        layout_principal.addWidget(self.drop_zone)

        # 2. Carte de sélection des formats
        card_formats = QFrame()
        card_formats.setObjectName("Card")
        formats_layout = QHBoxLayout(card_formats)
        formats_layout.setContentsMargins(25, 20, 25, 20)

        col_entree = QVBoxLayout()
        lbl_entree = QLabel("Format détecté dans le dossier :")
        lbl_entree.setStyleSheet("color: #a1a1aa; font-size: 12px;")
        self.combo_source = QComboBox()
        self.combo_source.setEnabled(False)
        self.combo_source.currentIndexChanged.connect(self.mettre_a_jour_sorties)
        col_entree.addWidget(lbl_entree)
        col_entree.addWidget(self.combo_source)

        fleche = QLabel("➔")
        fleche.setFont(QFont("Segoe UI", 20, QFont.Bold))
        fleche.setStyleSheet("color: #3b82f6;")
        fleche.setAlignment(Qt.AlignCenter)

        col_sortie = QVBoxLayout()
        lbl_sortie = QLabel("Convertir vers :")
        lbl_sortie.setStyleSheet("color: #a1a1aa; font-size: 12px;")
        self.combo_cible = QComboBox()
        self.combo_cible.setEnabled(False)
        col_sortie.addWidget(lbl_sortie)
        col_sortie.addWidget(self.combo_cible)

        formats_layout.addLayout(col_entree)
        formats_layout.addWidget(fleche)
        formats_layout.addLayout(col_sortie)
        layout_principal.addWidget(card_formats)

        # 3. Barre de progression et statut
        self.label_statut = QLabel("En attente d'un dossier...")
        self.label_statut.setStyleSheet("color: #a1a1aa; font-size: 12px;")
        layout_principal.addWidget(self.label_statut)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout_principal.addWidget(self.progress_bar)

        # 4. Bouton de lancement
        self.btn_lancer = QPushButton("Lancer la conversion en masse")
        self.btn_lancer.setObjectName("ActionBtn")
        self.btn_lancer.setCursor(Qt.PointingHandCursor)
        self.btn_lancer.setEnabled(False)
        self.btn_lancer.clicked.connect(self.lancer_conversion)
        layout_principal.addWidget(self.btn_lancer)

    def definir_dossier(self, chemin: str):
        self.dossier_actuel = chemin
        self.drop_zone.label_texte.setText(f"Dossier sélectionné :\n{chemin}")
        self.drop_zone.label_texte.setStyleSheet("color: #f4f4f5; font-weight: bold; font-size: 13px;")

        fichiers_trouves = scanner_dossier(chemin)
        self.combo_source.clear()
        self.combo_cible.clear()
        self.progress_bar.setValue(0)

        if not fichiers_trouves:
            self.combo_source.setEnabled(False)
            self.combo_cible.setEnabled(False)
            self.btn_lancer.setEnabled(False)
            self.label_statut.setText("Aucun fichier supporté trouvé dans ce dossier.")
            self.label_statut.setStyleSheet("color: #ef4444; font-size: 12px;")
            return

        self.combo_source.setEnabled(True)
        for ext, nombre in fichiers_trouves.items():
            self.combo_source.addItem(f"{ext}  ({nombre} fichier{'s' if nombre > 1 else ''})", userData=ext)

        self.label_statut.setText(f"{sum(fichiers_trouves.values())} fichier(s) compatible(s) détecté(s).")
        self.label_statut.setStyleSheet("color: #a1a1aa; font-size: 12px;")

    def mettre_a_jour_sorties(self):
        self.combo_cible.clear()
        ext_source = self.combo_source.currentData()
        if not ext_source:
            self.combo_cible.setEnabled(False)
            self.btn_lancer.setEnabled(False)
            return

        sorties = self.compatibilites.get(ext_source, [])
        if sorties:
            self.combo_cible.setEnabled(True)
            self.combo_cible.addItems(sorties)
            self.btn_lancer.setEnabled(True)
        else:
            self.combo_cible.setEnabled(False)
            self.btn_lancer.setEnabled(False)

    def lancer_conversion(self):
        ext_source = self.combo_source.currentData()
        ext_cible = self.combo_cible.currentText()

        if not self.dossier_actuel or not ext_source or not ext_cible:
            return

        self.btn_lancer.setEnabled(False)
        self.combo_source.setEnabled(False)
        self.combo_cible.setEnabled(False)
        self.progress_bar.setValue(0)

        self.worker = ConversionWorker(self.dossier_actuel, ext_source, ext_cible)
        self.worker.progression.connect(self.actualiser_progression)
        self.worker.termine.connect(self.conversion_terminee)
        self.worker.start()

    def actualiser_progression(self, actuel: int, total: int, nom_fichier: str):
        pourcentage = int((actuel / total) * 100)
        self.progress_bar.setValue(pourcentage)
        self.label_statut.setText(f"Conversion ({actuel}/{total}) : {nom_fichier}...")
        self.label_statut.setStyleSheet("color: #3b82f6; font-size: 12px;")

    def conversion_terminee(self, succes: int, erreurs: int, dossier_sortie: str):
        self.btn_lancer.setEnabled(True)
        self.combo_source.setEnabled(True)
        self.combo_cible.setEnabled(True)

        self.label_statut.setText(f"Terminé : {succes} réussi(s), {erreurs} erreur(s).")
        self.label_statut.setStyleSheet("color: #10b981; font-weight: bold; font-size: 12px;")

        QMessageBox.information(
            self,
            "Conversion terminée",
            f"Opération terminée !\n\n"
            f"• Fichiers convertis : {succes}\n"
            f"• Erreurs : {erreurs}\n\n"
            f"Les fichiers et le rapport ont été enregistrés dans :\n{dossier_sortie}"
        )
