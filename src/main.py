import sys
import os
import ctypes

# Assure que le dossier src est reconnu pour les imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from ui.main_window import MainWindow

def chemin_ressource(chemin_relatif: str) -> str:
    """Trouve le bon chemin de l'icône en mode normal ou compilé (.exe)."""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, chemin_relatif)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, chemin_relatif)

if __name__ == "__main__":
    # Force Windows à afficher votre icône dans la barre des tâches (et non celle de Python)
    if os.name == "nt":
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("universal.mass.converter.1.0")

    app = QApplication(sys.argv)
    
    # Application de l'icône sur toute l'application
    icone = QIcon(chemin_ressource("assets/icon.ico"))
    app.setWindowIcon(icone)

    fenetre = MainWindow()
    fenetre.setWindowIcon(icone)
    fenetre.show()
    sys.exit(app.exec())
