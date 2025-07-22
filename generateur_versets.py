#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur de PDF pour 1000 petits papiers avec versets bibliques
Optimisé pour l'impression et la découpe
"""

import os
import random
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.colors import black, lightgrey
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Import des configurations et versets locaux
from config import *
from versets.base_versets import obtenir_tous_versets


class GenerateurVersetsPDF:
    def __init__(self, nombre_versets=None):
        self.versets = obtenir_tous_versets()
        self.output_dir = "output"
        self.pdf_filename = f"versets_1000_papiers_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        self.nombre_versets = nombre_versets if nombre_versets is not None else NOMBRE_VERSETS
        
        # S'assurer que le dossier output existe
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def etendre_versets(self, nombre_souhaite):
        """Étend la liste des versets pour atteindre le nombre souhaité"""
        versets_etendus = []
        versets_base = self.versets.copy()
        
        while len(versets_etendus) < nombre_souhaite:
            if not versets_base:
                versets_base = self.versets.copy()
            
            # Prendre un verset aléatoire
            verset = versets_base.pop(random.randint(0, len(versets_base) - 1))
            versets_etendus.append(verset)
        
        return versets_etendus[:nombre_souhaite]
    
    def formater_texte(self, canvas_obj, texte, reference, x, y, largeur, hauteur, numero_verset):
        """Formate et dessine le texte dans le rectangle du papier"""
        # Marges intérieures du papier
        marge_interne = 6  # Réduit pour faire de la place au numéro
        
        # Zone de texte disponible
        zone_x = x + marge_interne
        zone_y = y + marge_interne
        zone_largeur = largeur - 2 * marge_interne
        zone_hauteur = hauteur - 2 * marge_interne
        
        # Ajouter le numéro en haut à droite si activé
        if AFFICHER_NUMEROS:
            canvas_obj.setFont(POLICE_NOM, POLICE_NUMERO_TAILLE)
            canvas_obj.setFillColor(COULEUR_NUMERO)
            numero_text = f"#{numero_verset}"
            numero_largeur = canvas_obj.stringWidth(numero_text, POLICE_NOM, POLICE_NUMERO_TAILLE)
            canvas_obj.drawString(x + largeur - numero_largeur - 4, y + hauteur - 8, numero_text)
            canvas_obj.setFillColor(black)
        
        # Ajouter une petite décoration si activé (pour impression N&B)
        if STYLE_DECORATIF:
            # Petit point décoratif en bas à gauche
            canvas_obj.setFillColor(COULEUR_NUMERO)
            canvas_obj.circle(x + 6, y + 6, 1, fill=1)
            canvas_obj.setFillColor(black)
        
        # Diviser le texte en lignes
        lignes_texte = self.diviser_texte(canvas_obj, texte, zone_largeur, POLICE_TAILLE)
        lignes_reference = self.diviser_texte(canvas_obj, reference, zone_largeur, POLICE_REFERENCE_TAILLE)
        
        # Calculer la hauteur totale nécessaire
        hauteur_ligne = POLICE_TAILLE + 1.5
        hauteur_reference = POLICE_REFERENCE_TAILLE + 1.5
        espace_numero = 8 if AFFICHER_NUMEROS else 0
        hauteur_totale = len(lignes_texte) * hauteur_ligne + len(lignes_reference) * hauteur_reference + 3
        
        # Position de départ (centré verticalement, avec espace pour le numéro)
        start_y = zone_y + zone_hauteur - espace_numero - (zone_hauteur - espace_numero - hauteur_totale) / 2
        
        # Dessiner le texte principal
        canvas_obj.setFont(POLICE_NOM, POLICE_TAILLE)
        canvas_obj.setFillColor(black)
        for i, ligne in enumerate(lignes_texte):
            canvas_obj.drawString(zone_x, start_y - i * hauteur_ligne, ligne)
        
        # Dessiner la référence (en plus petit et en italique si possible)
        try:
            canvas_obj.setFont(POLICE_NOM + "-Oblique", POLICE_REFERENCE_TAILLE)
        except:
            canvas_obj.setFont(POLICE_NOM, POLICE_REFERENCE_TAILLE)
        
        canvas_obj.setFillColor(COULEUR_NUMERO)  # Référence en gris pour style
        ref_y = start_y - len(lignes_texte) * hauteur_ligne - 3
        for i, ligne in enumerate(lignes_reference):
            canvas_obj.drawString(zone_x, ref_y - i * hauteur_reference, ligne)
        
        canvas_obj.setFillColor(black)
    
    def diviser_texte(self, canvas_obj, texte, largeur_max, taille_police):
        """Divise le texte en lignes qui rentrent dans la largeur donnée"""
        canvas_obj.setFont(POLICE_NOM, taille_police)
        
        mots = texte.split()
        lignes = []
        ligne_courante = ""
        
        for mot in mots:
            test_ligne = ligne_courante + (" " if ligne_courante else "") + mot
            largeur_test = canvas_obj.stringWidth(test_ligne, POLICE_NOM, taille_police)
            
            if largeur_test <= largeur_max:
                ligne_courante = test_ligne
            else:
                if ligne_courante:
                    lignes.append(ligne_courante)
                ligne_courante = mot
        
        if ligne_courante:
            lignes.append(ligne_courante)
        
        return lignes
    
    def dessiner_bordures(self, canvas_obj, x, y, largeur, hauteur):
        """Dessine les bordures du papier pour faciliter la découpe"""
        if AFFICHER_BORDURES:
            from reportlab.lib.colors import gray
            canvas_obj.setStrokeColor(gray)
            canvas_obj.setLineWidth(EPAISSEUR_BORDURES)
            
            # Bordure principale
            canvas_obj.rect(x, y, largeur, hauteur)
            
            # Ajouter des petites marques de découpe aux coins si style décoratif
            if STYLE_DECORATIF:
                canvas_obj.setLineWidth(0.8)
                # Petites marques aux coins extérieurs
                extension = 3
                # Coin haut-gauche
                canvas_obj.line(x - extension, y + hauteur, x, y + hauteur)
                canvas_obj.line(x, y + hauteur, x, y + hauteur + extension)
                # Coin haut-droite  
                canvas_obj.line(x + largeur, y + hauteur + extension, x + largeur, y + hauteur)
                canvas_obj.line(x + largeur, y + hauteur, x + largeur + extension, y + hauteur)
                # Coin bas-droite
                canvas_obj.line(x + largeur + extension, y, x + largeur, y)
                canvas_obj.line(x + largeur, y, x + largeur, y - extension)
                # Coin bas-gauche
                canvas_obj.line(x, y - extension, x, y)
                canvas_obj.line(x, y, x - extension, y)
    
    def generer_pdf(self):
        """Génère le PDF complet avec tous les versets"""
        print(f"🙏 Génération du PDF avec {self.nombre_versets} versets...")
        print(f"📄 Format: {PAPIERS_PAR_LIGNE} × {PAPIERS_PAR_COLONNE} = {PAPIERS_PAR_PAGE} papiers par page")
        
        # Étendre les versets pour atteindre le nombre souhaité
        versets_complets = self.etendre_versets(self.nombre_versets)
        random.shuffle(versets_complets)  # Mélanger pour éviter les répétitions consécutives
        
        # Créer le PDF
        pdf_path = os.path.join(self.output_dir, self.pdf_filename)
        c = canvas.Canvas(pdf_path, pagesize=A4)
        
        # Ajouter des métadonnées
        c.setTitle("Versets Bibliques - 1000 Petits Papiers")
        c.setAuthor("Générateur de Versets")
        c.setSubject("Collection de versets bibliques pour partage")
        
        verset_index = 0
        page_numero = 1
        
        while verset_index < len(versets_complets):
            print(f"📖 Génération de la page {page_numero}...")
            
            # Dessiner tous les papiers de cette page
            for row in range(PAPIERS_PAR_COLONNE):
                for col in range(PAPIERS_PAR_LIGNE):
                    if verset_index >= len(versets_complets):
                        break
                    
                    # Calculer la position du papier
                    x = MARGE_PAGE + col * (PAPIER_LARGEUR + ESPACEMENT_HORIZONTAL)
                    y = PAGE_HAUTEUR - MARGE_PAGE - (row + 1) * (PAPIER_HAUTEUR + ESPACEMENT_VERTICAL)
                    
                    # Dessiner les bordures
                    self.dessiner_bordures(c, x, y, PAPIER_LARGEUR, PAPIER_HAUTEUR)
                    
                    # Récupérer le verset
                    texte, reference = versets_complets[verset_index]
                    
                    # Formater et dessiner le texte avec numéro
                    self.formater_texte(c, texte, reference, x, y, PAPIER_LARGEUR, PAPIER_HAUTEUR, verset_index + 1)
                    
                    verset_index += 1
                
                if verset_index >= len(versets_complets):
                    break
            
            # Ajouter numéro de page en bas
            c.setFont(POLICE_NOM, 8)
            c.setFillColor(lightgrey)
            texte_page = f"Page {page_numero} - Versets {max(1, verset_index - PAPIERS_PAR_PAGE + 1)} à {min(verset_index, self.nombre_versets)}"
            largeur_texte = c.stringWidth(texte_page, POLICE_NOM, 8)
            c.drawString((PAGE_LARGEUR - largeur_texte) / 2, 20, texte_page)
            c.setFillColor(black)
            
            # Nouvelle page si nécessaire
            if verset_index < len(versets_complets):
                c.showPage()
                page_numero += 1
        
        # Sauvegarder le PDF
        c.save()
        
        # Statistiques finales
        nombre_pages = page_numero
        print(f"✅ PDF généré avec succès!")
        print(f"📁 Fichier: {pdf_path}")
        print(f"📊 Statistiques:")
        print(f"   • {len(versets_complets)} versets générés")
        print(f"   • {nombre_pages} pages")
        print(f"   • {PAPIERS_PAR_PAGE} papiers par page")
        print(f"   • Format des papiers: {PAPIER_LARGEUR/72*2.54:.1f}cm × {PAPIER_HAUTEUR/72*2.54:.1f}cm")
        
        return pdf_path


def main():
    """Fonction principale"""
    print("🙏 === GÉNÉRATEUR DE VERSETS BIBLIQUES ===")
    print("Création de 1000 petits papiers pour partager la Parole de Dieu")
    print()
    
    try:
        generateur = GenerateurVersetsPDF()
        pdf_path = generateur.generer_pdf()
        
        print()
        print(f"🎉 PDF créé avec succès: {pdf_path}")
        print()
        print("📋 Instructions d'impression:")
        print("   1. Imprimez sur du papier A4 standard")
        print("   2. Utilisez les lignes de guidage pour découper")
        print(f"   3. Chaque petit papier fait environ {PAPIER_LARGEUR/72*2.54:.1f}×{PAPIER_HAUTEUR/72*2.54:.1f}cm")
        print()
        print("🍩 Parfait pour accompagner vos beignets!")
        print("Que ces versets apportent joie et réconfort à tous ceux qui les liront. 🙏")
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
