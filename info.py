#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script d'information et de nettoyage pour le projet
"""

import os
from versets.base_versets import obtenir_tous_versets

def informations_projet():
    """Affiche les informations du projet"""
    print("📊 === INFORMATIONS DU PROJET ===")
    print()
    
    # Compter les versets disponibles
    versets = obtenir_tous_versets()
    print(f"📖 Versets disponibles : {len(versets)}")
    print()
    
    # Lister les fichiers dans output
    print("📁 Fichiers générés :")
    if os.path.exists("output"):
        fichiers = os.listdir("output")
        if fichiers:
            for fichier in sorted(fichiers):
                taille = os.path.getsize(f"output/{fichier}")
                print(f"   • {fichier} ({taille/1024:.1f} KB)")
        else:
            print("   Aucun fichier généré pour l'instant")
    else:
        print("   Dossier output non créé")
    
    print()
    print("🚀 === COMMANDES DISPONIBLES ===")
    print("   python demo_simple.py        # Test rapide (20 versets)")
    print("   python test_final.py         # Validation (100 versets)")  
    print("   python generateur_versets.py # Production finale (1000 versets)")
    print()
    print("📋 === ÉTAPES RECOMMANDÉES ===")
    print("   1. Lancer d'abord demo_simple.py")
    print("   2. Vérifier l'impression et la découpe")
    print("   3. Ajuster config.py si nécessaire")
    print("   4. Lancer test_final.py pour validation")
    print("   5. Générer les 1000 versets complets")
    print()
    print("🎯 Prêt pour distribuer 1000 messages d'espoir avec vos beignets ! 🙏")

def nettoyer_output():
    """Nettoie le dossier output"""
    print("🧹 === NETTOYAGE DU DOSSIER OUTPUT ===")
    
    if os.path.exists("output"):
        fichiers = os.listdir("output")
        if fichiers:
            print(f"Suppression de {len(fichiers)} fichier(s)...")
            for fichier in fichiers:
                os.remove(f"output/{fichier}")
                print(f"   • {fichier} supprimé")
            print("✅ Nettoyage terminé!")
        else:
            print("📁 Dossier output déjà vide")
    else:
        print("📁 Dossier output n'existe pas")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "clean":
        nettoyer_output()
    else:
        informations_projet()
        print()
        print("💡 Astuce: Utilisez 'python info.py clean' pour nettoyer le dossier output")
