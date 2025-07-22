#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test rapide pour générer un petit PDF de démonstration
"""

import os
from generateur_versets import GenerateurVersetsPDF
import config

def test_generation_demo():
    """Génère un PDF de démonstration avec seulement 20 versets"""
    print("🧪 === TEST DE GÉNÉRATION RAPIDE ===")
    print("Génération d'un PDF de démonstration avec 20 versets")
    
    try:
        # Sauvegarder la valeur originale
        original_nombre = config.NOMBRE_VERSETS
        
        # Modifier temporairement pour le test
        config.NOMBRE_VERSETS = 20
        
        generateur = GenerateurVersetsPDF()
        # Changer le nom du fichier pour le test
        generateur.pdf_filename = f"demo_versets_20_papiers.pdf"
        
        pdf_path = generateur.generer_pdf()
        
        print(f"✅ PDF de démonstration créé: {pdf_path}")
        print("� Vérifiez le résultat avant de générer les 1000 versets complets!")
        
        # Restaurer la valeur originale
        config.NOMBRE_VERSETS = original_nombre
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        # Restaurer en cas d'erreur aussi
        config.NOMBRE_VERSETS = 1000
        return False
    
    return True

if __name__ == "__main__":
    test_generation_demo()
