#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de démonstration avec 20 versets seulement
"""

import os
import random
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black, lightgrey, gray
from versets.base_versets import obtenir_tous_versets

# Configuration simplifiée pour la démonstration
PAPIER_LARGEUR = 144  # ~5cm
PAPIER_HAUTEUR = 85   # ~3cm (nouvelle disposition 6×4)
MARGE_PAGE = 36
ESPACEMENT_HORIZONTAL = 18
ESPACEMENT_VERTICAL = 15    # Réduit pour 6 lignes
POLICE_NOM = "Helvetica"
POLICE_TAILLE = 8          # Réduit pour s'adapter au format plus petit
POLICE_REFERENCE_TAILLE = 6
PAGE_LARGEUR = 595  # A4
PAGE_HAUTEUR = 842  # A4

# Calcul des papiers par page
PAPIERS_PAR_LIGNE = int((PAGE_LARGEUR - 2 * MARGE_PAGE + ESPACEMENT_HORIZONTAL) / (PAPIER_LARGEUR + ESPACEMENT_HORIZONTAL))
PAPIERS_PAR_COLONNE = int((PAGE_HAUTEUR - 2 * MARGE_PAGE + ESPACEMENT_VERTICAL) / (PAPIER_HAUTEUR + ESPACEMENT_VERTICAL))
PAPIERS_PAR_PAGE = PAPIERS_PAR_LIGNE * PAPIERS_PAR_COLONNE

def diviser_texte(canvas_obj, texte, largeur_max, taille_police):
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

def formater_texte(canvas_obj, texte, reference, x, y, largeur, hauteur, numero_verset):
    """Formate et dessine le texte dans le rectangle du papier"""
    from reportlab.lib.colors import black, gray
    
    marge_interne = 6
    
    zone_x = x + marge_interne
    zone_y = y + marge_interne
    zone_largeur = largeur - 2 * marge_interne
    zone_hauteur = hauteur - 2 * marge_interne
    
    # Ajouter le numéro en haut à droite
    canvas_obj.setFont(POLICE_NOM, 5)  # Taille 5 pour le numéro
    canvas_obj.setFillColor(gray)
    numero_text = f"#{numero_verset}"
    numero_largeur = canvas_obj.stringWidth(numero_text, POLICE_NOM, 5)
    canvas_obj.drawString(x + largeur - numero_largeur - 4, y + hauteur - 8, numero_text)
    
    # Petit point décoratif en bas à gauche
    canvas_obj.circle(x + 6, y + 6, 1, fill=1)
    canvas_obj.setFillColor(black)
    
    lignes_texte = diviser_texte(canvas_obj, texte, zone_largeur, POLICE_TAILLE)
    lignes_reference = diviser_texte(canvas_obj, reference, zone_largeur, POLICE_REFERENCE_TAILLE)
    
    hauteur_ligne = POLICE_TAILLE + 1.5
    hauteur_reference = POLICE_REFERENCE_TAILLE + 1.5
    hauteur_totale = len(lignes_texte) * hauteur_ligne + len(lignes_reference) * hauteur_reference + 3
    
    start_y = zone_y + zone_hauteur - 8 - (zone_hauteur - 8 - hauteur_totale) / 2
    
    # Texte principal
    canvas_obj.setFont(POLICE_NOM, POLICE_TAILLE)
    canvas_obj.setFillColor(black)
    for i, ligne in enumerate(lignes_texte):
        canvas_obj.drawString(zone_x, start_y - i * hauteur_ligne, ligne)
    
    # Référence en gris
    try:
        canvas_obj.setFont(POLICE_NOM + "-Oblique", POLICE_REFERENCE_TAILLE)
    except:
        canvas_obj.setFont(POLICE_NOM, POLICE_REFERENCE_TAILLE)
    
    canvas_obj.setFillColor(gray)
    ref_y = start_y - len(lignes_texte) * hauteur_ligne - 3
    for i, ligne in enumerate(lignes_reference):
        canvas_obj.drawString(zone_x, ref_y - i * hauteur_reference, ligne)
    
    canvas_obj.setFillColor(black)

def dessiner_bordures(canvas_obj, x, y, largeur, hauteur):
    """Dessine les bordures du papier"""
    canvas_obj.setStrokeColor(gray)
    canvas_obj.setLineWidth(0.5)
    # Bordure principale
    canvas_obj.rect(x, y, largeur, hauteur)
    
    # Petites marques de découpe aux coins
    canvas_obj.setLineWidth(0.8)
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

def main():
    print("🧪 === DÉMONSTRATION 20 VERSETS ===")
    print("Génération d'un PDF de test avec 20 versets seulement")
    
    # Préparer les versets
    tous_versets = obtenir_tous_versets()
    versets_demo = random.sample(tous_versets, min(20, len(tous_versets)))
    
    # Créer le dossier output s'il n'existe pas
    if not os.path.exists("output"):
        os.makedirs("output")
    
    # Créer le PDF
    pdf_filename = "output/DEMO_20_versets.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=A4)
    
    c.setTitle("DÉMO - 20 Versets Bibliques")
    c.setAuthor("Générateur de Versets - Version Démo")
    
    print(f"📄 Format: {PAPIERS_PAR_LIGNE} × {PAPIERS_PAR_COLONNE} = {PAPIERS_PAR_PAGE} papiers par page")
    
    verset_index = 0
    page_numero = 1
    
    while verset_index < len(versets_demo):
        print(f"📖 Génération de la page {page_numero}...")
        
        for row in range(PAPIERS_PAR_COLONNE):
            for col in range(PAPIERS_PAR_LIGNE):
                if verset_index >= len(versets_demo):
                    break
                
                # Position du papier
                x = MARGE_PAGE + col * (PAPIER_LARGEUR + ESPACEMENT_HORIZONTAL)
                y = PAGE_HAUTEUR - MARGE_PAGE - (row + 1) * (PAPIER_HAUTEUR + ESPACEMENT_VERTICAL)
                
                # Dessiner bordures
                dessiner_bordures(c, x, y, PAPIER_LARGEUR, PAPIER_HAUTEUR)
                
                # Récupérer et dessiner le verset
                texte, reference = versets_demo[verset_index]
                formater_texte(c, texte, reference, x, y, PAPIER_LARGEUR, PAPIER_HAUTEUR, verset_index + 1)
                
                verset_index += 1
            
            if verset_index >= len(versets_demo):
                break
        
        # Numéro de page
        c.setFont(POLICE_NOM, 8)
        c.setFillColor(lightgrey)
        texte_page = f"DÉMO - Page {page_numero} - Versets {max(1, verset_index - min(PAPIERS_PAR_PAGE, len(versets_demo)) + 1)} à {min(verset_index, 20)}"
        largeur_texte = c.stringWidth(texte_page, POLICE_NOM, 8)
        c.drawString((PAGE_LARGEUR - largeur_texte) / 2, 20, texte_page)
        c.setFillColor(black)
        
        if verset_index < len(versets_demo):
            c.showPage()
            page_numero += 1
    
    c.save()
    
    print(f"✅ PDF de démonstration créé: {pdf_filename}")
    print(f"📊 {len(versets_demo)} versets sur {page_numero} page(s)")
    print(f"📐 Format des papiers: {PAPIER_LARGEUR/72*2.54:.1f}cm × {PAPIER_HAUTEUR/72*2.54:.1f}cm")
    print("🔍 Vérifiez ce fichier avant de générer les 1000 versets complets!")

if __name__ == "__main__":
    main()
