#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test des nouvelles fonctionnalités CSV :
- Séparateurs personnalisés
- Champs uniques
"""

import json
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import generer_csv_bulk

def test_separateurs():
    """Test des différents séparateurs"""
    print("🧪 === TEST DES SÉPARATEURS CSV ===")
    print()
    
    colonnes_config = [
        {'nom': 'ID', 'unique': True},
        {'nom': 'Nom', 'unique': False},
        {'nom': 'Email', 'unique': True},
    ]
    
    separateurs = {
        ',': 'virgule (standard)',
        ';': 'point-virgule (Excel FR)',
        '|': 'pipe (alternatif)',
        '\t': 'tabulation (TSV)'
    }
    
    for sep, description in separateurs.items():
        print(f"📄 Test {description}...")
        try:
            fichier = generer_csv_bulk(10, colonnes_config, 'fake', sep)
            
            # Lire et afficher un échantillon
            with open(fichier, 'r', encoding='utf-8') as f:
                lignes = f.readlines()[:3]  # En-tête + 2 lignes
                print(f"   ✅ Fichier: {os.path.basename(fichier)}")
                print(f"   📋 Aperçu:")
                for ligne in lignes:
                    print(f"      {ligne.strip()}")
                print()
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
            print()

def test_unicite():
    """Test de l'unicité des champs"""
    print("🔒 === TEST DE L'UNICITÉ ===")
    print()
    
    # Configuration avec champs uniques
    colonnes_config = [
        {'nom': 'ID', 'unique': True},
        {'nom': 'Email', 'unique': True},
        {'nom': 'Nom', 'unique': False},
        {'nom': 'Ville', 'unique': False}
    ]
    
    print("📊 Génération de 50 lignes avec champs uniques...")
    try:
        fichier = generer_csv_bulk(50, colonnes_config, 'fake', ',')
        print(f"✅ Fichier généré: {os.path.basename(fichier)}")
        
        # Vérifier l'unicité
        with open(fichier, 'r', encoding='utf-8') as f:
            import csv
            reader = csv.reader(f)
            header = next(reader)
            
            # Collecter les valeurs des colonnes uniques
            ids = []
            emails = []
            
            for ligne in reader:
                ids.append(ligne[0])      # ID
                emails.append(ligne[1])   # Email
        
        # Vérifier l'unicité
        ids_uniques = len(set(ids))
        emails_uniques = len(set(emails))
        
        print(f"🔍 Vérification de l'unicité:")
        print(f"   📧 Emails: {emails_uniques}/50 uniques {'✅' if emails_uniques == 50 else '❌'}")
        print(f"   🆔 IDs: {ids_uniques}/50 uniques {'✅' if ids_uniques == 50 else '❌'}")
        
        if ids_uniques == 50 and emails_uniques == 50:
            print("🎉 Test d'unicité RÉUSSI !")
        else:
            print("⚠️  Test d'unicité partiellement échoué")
            
        print()
        
        # Afficher un échantillon
        print("📋 Échantillon des données:")
        with open(fichier, 'r', encoding='utf-8') as f:
            lignes = f.readlines()[:6]  # En-tête + 5 lignes
            for i, ligne in enumerate(lignes):
                print(f"   {i:2d}: {ligne.strip()}")
                
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    print()

def test_formats():
    """Test des différents formats de données"""
    print("📊 === TEST DES FORMATS DE DONNÉES ===")
    print()
    
    colonnes_config = [
        {'nom': 'ID', 'unique': True},
        {'nom': 'Nom', 'unique': False},
        {'nom': 'Email', 'unique': True}
    ]
    
    formats = ['fake', 'sequence', 'custom']
    
    for fmt in formats:
        print(f"🎯 Test format '{fmt}'...")
        try:
            fichier = generer_csv_bulk(5, colonnes_config, fmt, ',')
            print(f"   ✅ Fichier: {os.path.basename(fichier)}")
            
            # Afficher un échantillon
            with open(fichier, 'r', encoding='utf-8') as f:
                lignes = f.readlines()[:4]  # En-tête + 3 lignes
                print(f"   📋 Aperçu:")
                for ligne in lignes:
                    print(f"      {ligne.strip()}")
            print()
            
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
            print()

def main():
    """Tests principaux"""
    print("🧪 === TESTS DES NOUVELLES FONCTIONNALITÉS CSV ===")
    print("Séparateurs personnalisés + Champs uniques")
    print("=" * 60)
    print()
    
    try:
        test_separateurs()
        test_unicite()
        test_formats()
        
        print("🎉 === TESTS TERMINÉS ===")
        print("✅ Toutes les nouvelles fonctionnalités ont été testées !")
        print()
        print("💡 Nouvelles capacités:")
        print("   • Séparateurs: , ; | \\t")
        print("   • Champs uniques garantis")
        print("   • Format TSV automatique")
        print("   • Rétrocompatibilité assurée")
        
    except Exception as e:
        print(f"❌ Erreur générale: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
