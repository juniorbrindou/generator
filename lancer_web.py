#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de lancement pour l'interface web du Bulk Generator
"""

import os
import sys
import webbrowser
import time
import threading

def ouvrir_navigateur():
    """Ouvre le navigateur après un délai"""
    time.sleep(2)  # Attendre que le serveur démarre
    webbrowser.open('http://localhost:5000')

def main():
    print("🌐 === BULK GENERATOR - INTERFACE WEB ===")
    print()
    print("🚀 Démarrage de l'interface web...")
    print("🔗 L'interface sera accessible sur: http://localhost:5000")
    print()
    print("📋 Fonctionnalités disponibles:")
    print("   • Générateur PDF (versets bibliques)")
    print("   • Générateur CSV (données en masse)")
    print("   • Gestion des fichiers générés")
    print()
    print("💡 Appuyez sur Ctrl+C pour arrêter le serveur")
    print("-" * 50)
    print()
    
    # Ouvrir le navigateur dans un thread séparé
    threading.Thread(target=ouvrir_navigateur, daemon=True).start()
    
    # Démarrer l'application Flask
    try:
        from app import app
        app.run(debug=False, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n🛑 Arrêt du serveur...")
        print("👋 Au revoir !")
    except ImportError as e:
        print(f"❌ Erreur d'importation: {e}")
        print("💡 Assurez-vous que Flask est installé: pip install flask")
        return 1
    except Exception as e:
        print(f"❌ Erreur lors du démarrage: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
