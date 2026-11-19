import os
import subprocess
import fitz  # PyMuPDF
import docx
import markdown
from markdownify import markdownify as html_to_md
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from ebooklib import epub
from bs4 import BeautifulSoup
from config.formats import CALIBRE_DISPONIBLE
from converters.base_converter import BaseConverter

class DocumentConverter(BaseConverter):
    """Gère les PDF, DOCX, Markdown, HTML, TXT et livres numériques (EPUB, MOBI, AZW3)."""

    def convertir_fichier(self, chemin_source: str) -> tuple[bool, str]:
        chemin_sortie = self.construire_chemin_sortie(chemin_source)

        try:
            # Cas 1 : Conversions impliquant Kindle (.mobi / .azw3) via Calibre
            if self.ext_source in {".mobi", ".azw3"} or self.ext_cible in {".mobi", ".azw3"}:
                if not CALIBRE_DISPONIBLE:
                    return False, "Calibre (ebook-convert) est requis pour les formats .mobi et .azw3."
                subprocess.run(["ebook-convert", chemin_source, chemin_sortie], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                return True, chemin_sortie

            # Cas 2 : Extraction du texte brut depuis n'importe quel document
            texte = self._extraire_texte(chemin_source)

            if self.ext_cible == ".txt":
                with open(chemin_sortie, "w", encoding="utf-8") as f:
                    f.write(texte)

            elif self.ext_cible == ".md":
                if self.ext_source == ".html":
                    with open(chemin_source, "r", encoding="utf-8") as f:
                        md_contenu = html_to_md(f.read())
                    with open(chemin_sortie, "w", encoding="utf-8") as f:
                        f.write(md_contenu)
                else:
                    with open(chemin_sortie, "w", encoding="utf-8") as f:
                        f.write(texte)

            elif self.ext_cible == ".html":
                html_contenu = markdown.markdown(texte) if self.ext_source == ".md" else f"<html><body><pre>{texte}</pre></body></html>"
                with open(chemin_sortie, "w", encoding="utf-8") as f:
                    f.write(html_contenu)

            elif self.ext_cible == ".docx":
                doc = docx.Document()
                for paragraphe in texte.split("\n"):
                    doc.add_paragraph(paragraphe)
                doc.save(chemin_sortie)

            elif self.ext_cible == ".pdf":
                self._generer_pdf_simple(texte, chemin_sortie)

            elif self.ext_cible == ".epub":
                self._generer_epub(texte, os.path.basename(chemin_source), chemin_sortie)

            elif self.ext_source == ".pdf" and self.ext_cible in {".png", ".jpg"}:
                # Convertit chaque page du PDF en image
                doc_pdf = fitz.open(chemin_source)
                nom_base = os.path.splitext(os.path.basename(chemin_source))[0]
                for index, page in enumerate(doc_pdf):
                    pix = page.get_pixmap(dpi=150)
                    img_path = os.path.join(self.dossier_sortie, f"{nom_base}_page_{index + 1}{self.ext_cible}")
                    pix.save(img_path)
                return True, self.dossier_sortie

            return True, chemin_sortie

        except Exception as e:
            return False, f"Erreur document ({chemin_source}) : {str(e)}"

    def _extraire_texte(self, chemin: str) -> str:
        if self.ext_source == ".pdf":
            doc = fitz.open(chemin)
            return "\n".join(page.get_text() for page in doc)
        elif self.ext_source == ".docx":
            doc = docx.Document(chemin)
            return "\n".join(p.text for p in doc.paragraphs)
        elif self.ext_source == ".epub":
            livre = epub.read_epub(chemin)
            morceaux = []
            for item in livre.get_items_of_type(9):  # DOCUMENT
                soup = BeautifulSoup(item.get_content(), "html.parser")
                morceaux.append(soup.get_text())
            return "\n".join(morceaux)
        else:
            with open(chemin, "r", encoding="utf-8", errors="ignore") as f:
                contenu = f.read()
            if self.ext_source == ".html":
                return BeautifulSoup(contenu, "html.parser").get_text()
            return contenu

    def _generer_pdf_simple(self, texte: str, chemin_sortie: str):
        c = canvas.Canvas(chemin_sortie, pagesize=A4)
        largeur, hauteur = A4
        y = hauteur - 50
        for ligne in texte.splitlines():
            if y < 50:
                c.showPage()
                y = hauteur - 50
            c.drawString(40, y, ligne[:95])
            y -= 15
        c.save()

    def _generer_epub(self, texte: str, titre: str, chemin_sortie: str):
        livre = epub.EpubBook()
        livre.set_title(titre)
        livre.set_language("fr")
        chapitre = epub.EpubHtml(title="Contenu", file_name="chap_01.xhtml", lang="fr")
        chapitre.content = f"<h1>{titre}</h1><p>{texte.replace(chr(10), '<br/>')}</p>"
        livre.add_item(chapitre)
        livre.toc = (epub.Link("chap_01.xhtml", "Contenu", "chap1"),)
        livre.add_item(epub.EpubNcx())
        livre.add_item(epub.EpubNav())
        livre.spine = ["nav", chapitre]
        epub.write_epub(chemin_sortie, livre)
