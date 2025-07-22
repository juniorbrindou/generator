#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test final - Génère 100 versets pour vérifier le bon fonctionnement
avant la génération complète de 1000
"""

from generateur_versets import GenerateurVersetsPDF

def test_100_versets():
    """Test avec 100 versets pour validation finale"""
    print("🔬 === TEST FINAL - 100 VERSETS ===")
    print("Validation avant génération des 1000 versets complets")
    
    try:
        # Créer le générateur avec 100 versets spécifiquement
        generateur = GenerateurVersetsPDF(nombre_versets=100)
        generateur.pdf_filename = "TEST_100_versets_final.pdf"
        
        pdf_path = generateur.generer_pdf()
        
        print(f"✅ Test final réussi: {pdf_path}")
        print("🎯 Vous êtes prêt pour générer les 1000 versets complets!")
        print("   Utilisez: python generateur_versets.py")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    test_100_versets()
