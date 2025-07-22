#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aperçu rapide - 6 versets pour voir le rendu avec numérotation
"""

from generateur_versets import GenerateurVersetsPDF

def apercu_numerotation():
    """Génère un aperçu de 6 versets pour voir la numérotation"""
    print("👀 === APERÇU NUMÉROTATION ===")
    print("Génération de 6 versets pour voir le rendu final")
    
    try:
        generateur = GenerateurVersetsPDF(nombre_versets=6)
        generateur.pdf_filename = "APERCU_numerotation.pdf"
        
        pdf_path = generateur.generer_pdf()
        
        print(f"✅ Aperçu créé: {pdf_path}")
        print("🔍 Vérifiez la numérotation et les embellissements!")
        print("   Chaque verset a son numéro (#1, #2, etc.)")
        print("   + Petit point décoratif en bas à gauche")
        print("   + Marques de découpe aux coins")
        print("   + Référence en gris pour l'élégance")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    apercu_numerotation()
