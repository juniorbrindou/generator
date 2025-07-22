#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interface Web pour le Bulk Generator
Génération de PDF (versets) et CSV en masse
"""

from flask import Flask, render_template, request, send_file, jsonify, flash, redirect, url_for
import os
import json
from datetime import datetime
from werkzeug.utils import secure_filename
import io
import csv
from generateur_versets import GenerateurVersetsPDF
from config import *

app = Flask(__name__)
app.secret_key = 'bulk-generator-secret-key-2025'

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv', 'json', 'txt'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Page d'accueil avec sélection du type de génération"""
    return render_template('index.html')

@app.route('/pdf-generator')
def pdf_generator():
    """Interface pour générer des PDF de versets"""
    return render_template('pdf_generator.html', config={
        'nombre_versets': NOMBRE_VERSETS,
        'papiers_par_ligne': PAPIERS_PAR_LIGNE,
        'papiers_par_colonne': PAPIERS_PAR_COLONNE,
        'afficher_numeros': AFFICHER_NUMEROS,
        'style_decoratif': STYLE_DECORATIF,
        'afficher_bordures': AFFICHER_BORDURES
    })

@app.route('/csv-generator')
def csv_generator():
    """Interface pour générer des fichiers CSV"""
    return render_template('csv_generator.html')

@app.route('/api/generate-pdf', methods=['POST'])
def api_generate_pdf():
    """API pour générer un PDF de versets"""
    try:
        data = request.get_json()
        nombre_versets = int(data.get('nombre_versets', NOMBRE_VERSETS))
        
        # Créer le générateur avec les paramètres personnalisés
        generateur = GenerateurVersetsPDF(nombre_versets=nombre_versets)
        
        # Générer le PDF
        pdf_path = generateur.generer_pdf()
        
        # Retourner les informations du fichier généré
        file_size = os.path.getsize(pdf_path)
        
        return jsonify({
            'success': True,
            'filename': os.path.basename(pdf_path),
            'filepath': pdf_path,
            'size': file_size,
            'versets': nombre_versets,
            'message': f'PDF généré avec {nombre_versets} versets'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/generate-csv', methods=['POST'])
def api_generate_csv():
    """API pour générer un fichier CSV"""
    try:
        data = request.get_json()
        
        # Paramètres de génération CSV
        nombre_lignes = int(data.get('nombre_lignes', 1000))
        colonnes_config = data.get('colonnes', [{'nom': 'Nom', 'unique': False}, {'nom': 'Email', 'unique': True}, {'nom': 'Telephone', 'unique': False}])
        format_donnees = data.get('format', 'fake')  # fake, sequence, custom
        separateur = data.get('separateur', ',')
        
        # Gérer le format des colonnes (rétrocompatibilité)
        if colonnes_config and isinstance(colonnes_config[0], str):
            # Ancien format (liste de strings)
            colonnes_config = [{'nom': col, 'unique': False} for col in colonnes_config]
        
        # Générer le CSV
        csv_path = generer_csv_bulk(nombre_lignes, colonnes_config, format_donnees, separateur)
        
        file_size = os.path.getsize(csv_path)
        
        return jsonify({
            'success': True,
            'filename': os.path.basename(csv_path),
            'filepath': csv_path,
            'size': file_size,
            'lignes': nombre_lignes,
            'message': f'CSV généré avec {nombre_lignes} lignes'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/download/<path:filename>')
def download_file(filename):
    """Télécharger un fichier généré"""
    try:
        # Chercher dans le dossier output d'abord
        output_path = os.path.join('output', filename)
        if os.path.exists(output_path):
            return send_file(output_path, as_attachment=True)
        
        # Sinon chercher dans le dossier racine
        if os.path.exists(filename):
            return send_file(filename, as_attachment=True)
            
        return jsonify({'error': 'Fichier non trouvé'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/files')
def api_list_files():
    """Lister les fichiers générés"""
    try:
        files = []
        
        # Lister les fichiers dans le dossier output
        output_dir = 'output'
        if os.path.exists(output_dir):
            for filename in os.listdir(output_dir):
                filepath = os.path.join(output_dir, filename)
                if os.path.isfile(filepath):
                    stat = os.stat(filepath)
                    files.append({
                        'name': filename,
                        'size': stat.st_size,
                        'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        'type': 'PDF' if filename.endswith('.pdf') else 'CSV' if filename.endswith('.csv') else 'Autre'
                    })
        
        # Trier par date de modification (plus récent en premier)
        files.sort(key=lambda x: x['modified'], reverse=True)
        
        return jsonify({'files': files})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generer_csv_bulk(nombre_lignes, colonnes_config, format_donnees, separateur=','):
    """Génère un fichier CSV avec des données en masse - Optimisé pour gros volumes"""
    from faker import Faker
    import gc
    import time
    
    fake = Faker('fr_FR')  # Données en français
    
    # Vérifications préalables pour gros volumes
    if nombre_lignes > 10000000:  # 10M+
        return generer_csv_tres_gros_volume(nombre_lignes, colonnes_config, format_donnees, separateur)
    elif nombre_lignes > 1000000:  # 1M+
        return generer_csv_gros_volume(nombre_lignes, colonnes_config, format_donnees, separateur)
    
    # Version standard pour < 1M lignes
    return generer_csv_standard(nombre_lignes, colonnes_config, format_donnees, separateur)

def generer_csv_standard(nombre_lignes, colonnes_config, format_donnees, separateur=','):
    """Version standard pour moins d'1 million de lignes"""
    from faker import Faker
    fake = Faker('fr_FR')
    
    # Extraire les noms des colonnes
    colonnes_noms = [col['nom'] if isinstance(col, dict) else col for col in colonnes_config]
    
    # Créer le nom du fichier
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    extension = 'tsv' if separateur == '\t' else 'csv'
    filename = f'bulk_data_{nombre_lignes}_lignes_{timestamp}.{extension}'
    csv_path = os.path.join('output', filename)
    
    # S'assurer que le dossier output existe
    if not os.path.exists('output'):
        os.makedirs('output')
    
    # Dictionnaires pour garantir l'unicité
    valeurs_uniques = {}
    for col_config in colonnes_config:
        if isinstance(col_config, dict) and col_config.get('unique', False):
            valeurs_uniques[col_config['nom']] = set()
    
    # Générer les données
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=separateur)
        writer.writerow(colonnes_noms)
        
        # Générer les lignes de données
        for i in range(nombre_lignes):
            ligne = []
            
            for col_config in colonnes_config:
                if isinstance(col_config, dict):
                    colonne = col_config['nom']
                    est_unique = col_config.get('unique', False)
                    min_length = col_config.get('minLength', 0)
                else:
                    colonne = col_config
                    est_unique = False
                    min_length = 0
                
                colonne_lower = colonne.lower()
                valeur = None
                
                # Générer la valeur selon le format
                if format_donnees == 'sequence':
                    valeur = generer_valeur_sequence(colonne, colonne_lower, i)
                elif format_donnees == 'fake':
                    valeur = generer_valeur_fake(fake, colonne, colonne_lower, i)
                else:
                    valeur = f'{colonne}_{i+1}'
                
                # Assurer la longueur minimum
                valeur = assurer_longueur_minimum(str(valeur), min_length, colonne_lower, fake)
                
                # Garantir l'unicité si nécessaire
                if est_unique:
                    tentatives = 0
                    while valeur in valeurs_uniques[colonne] and tentatives < 100:
                        if format_donnees == 'fake':
                            base_valeur = generer_valeur_fake(fake, colonne, colonne_lower, i + tentatives * 1000)
                            valeur = assurer_longueur_minimum(str(base_valeur), min_length, colonne_lower, fake)
                        else:
                            valeur = f"{valeur}_{tentatives:03d}"
                            valeur = assurer_longueur_minimum(valeur, min_length, colonne_lower, fake)
                        tentatives += 1
                    
                    valeurs_uniques[colonne].add(valeur)
                
                ligne.append(valeur)
            
            writer.writerow(ligne)
            
            # Afficher le progrès pour les gros fichiers
            if (i + 1) % 10000 == 0:
                print(f"📊 Génération CSV: {i+1}/{nombre_lignes} lignes...")
    
    print(f"✅ CSV généré: {csv_path}")
    return csv_path

def assurer_longueur_minimum(valeur, min_length, type_colonne, faker_instance):
    """Assure qu'une valeur respecte la longueur minimum"""
    if min_length <= 0 or len(valeur) >= min_length:
        return valeur
    
    # Stratégies différentes selon le type de colonne
    if 'email' in type_colonne or 'mail' in type_colonne:
        # Pour les emails, ajouter des caractères avant le @
        if '@' in valeur:
            partie_avant, partie_apres = valeur.split('@', 1)
            while len(valeur) < min_length:
                partie_avant += faker_instance.random_letter().lower()
                valeur = partie_avant + '@' + partie_apres
        else:
            valeur += '@example.com'
            
    elif 'tel' in type_colonne or 'phone' in type_colonne:
        # Pour les téléphones, ajouter des chiffres
        while len(valeur) < min_length:
            valeur += str(faker_instance.random_digit())
            
    elif 'nom' in type_colonne or 'name' in type_colonne or 'prenom' in type_colonne:
        # Pour les noms, ajouter des lettres
        while len(valeur) < min_length:
            valeur += faker_instance.random_letter().lower()
            
    elif 'adresse' in type_colonne or 'address' in type_colonne:
        # Pour les adresses, ajouter des mots
        while len(valeur) < min_length:
            valeur += ' ' + faker_instance.word()
            
    elif 'ville' in type_colonne or 'city' in type_colonne:
        # Pour les villes, ajouter des suffixes
        suffixes = ['ville', 'sur-Seine', 'les-Bains', 'en-Provence']
        while len(valeur) < min_length and suffixes:
            valeur += '-' + suffixes.pop(0)
            
    else:
        # Stratégie générale : répéter ou ajouter des caractères
        if valeur.isdigit():
            # Pour les nombres, ajouter des chiffres
            while len(valeur) < min_length:
                valeur += str(faker_instance.random_digit())
        else:
            # Pour le texte, ajouter des caractères alphanumériques
            while len(valeur) < min_length:
                valeur += faker_instance.random_letter().lower()
    
    return valeur

def generer_valeur_sequence(colonne, colonne_lower, index):
    """Génère une valeur séquentielle"""
    if 'nom' in colonne_lower:
        return f'Nom{(index+1):06d}'
    elif 'email' in colonne_lower or 'mail' in colonne_lower:
        return f'user{(index+1):06d}@example.com'
    elif 'tel' in colonne_lower or 'phone' in colonne_lower:
        return f'06{(index+1):08d}'
    elif 'id' in colonne_lower:
        return str(index + 1)
    else:
        return f'{colonne}{(index+1):06d}'

def generer_valeur_fake(fake, colonne, colonne_lower, index):
    """Génère une valeur réaliste avec Faker"""
    if 'nom' in colonne_lower or 'name' in colonne_lower:
        return fake.name()
    elif 'prenom' in colonne_lower or 'firstname' in colonne_lower:
        return fake.first_name()
    elif 'email' in colonne_lower or 'mail' in colonne_lower:
        return fake.email()
    elif 'tel' in colonne_lower or 'phone' in colonne_lower:
        return fake.phone_number()
    elif 'adresse' in colonne_lower or 'address' in colonne_lower:
        return fake.address().replace('\n', ', ')
    elif 'ville' in colonne_lower or 'city' in colonne_lower:
        return fake.city()
    elif 'code' in colonne_lower and 'postal' in colonne_lower:
        return fake.postcode()
    elif 'entreprise' in colonne_lower or 'company' in colonne_lower:
        return fake.company()
    elif 'date' in colonne_lower:
        return fake.date()
    elif 'id' in colonne_lower:
        return str(index + 1)
    else:
        return fake.word()

def generer_csv_gros_volume(nombre_lignes, colonnes_config, format_donnees, separateur=','):
    """Version optimisée pour 1-10 millions de lignes"""
    from faker import Faker
    import gc
    import time
    
    print(f"🚀 Mode GROS VOLUME activé pour {nombre_lignes:,} lignes")
    print("⚡ Optimisations: Garbage collection + Écriture par chunks")
    
    fake = Faker('fr_FR')
    colonnes_noms = [col['nom'] if isinstance(col, dict) else col for col in colonnes_config]
    
    # Créer le nom du fichier
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    extension = 'tsv' if separateur == '\t' else 'csv'
    filename = f'bulk_data_GROS_{nombre_lignes}_lignes_{timestamp}.{extension}'
    csv_path = os.path.join('output', filename)
    
    if not os.path.exists('output'):
        os.makedirs('output')
    
    # Pour les gros volumes, on utilise des compteurs au lieu de sets
    compteurs_uniques = {}
    for col_config in colonnes_config:
        if isinstance(col_config, dict) and col_config.get('unique', False):
            compteurs_uniques[col_config['nom']] = 0
    
    chunk_size = 50000  # Traiter par chunks de 50k lignes
    chunks_total = (nombre_lignes + chunk_size - 1) // chunk_size
    
    print(f"📊 Génération en {chunks_total} chunks de {chunk_size:,} lignes")
    
    debut = time.time()
    
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=separateur)
        writer.writerow(colonnes_noms)
        
        for chunk_num in range(chunks_total):
            debut_chunk = chunk_num * chunk_size
            fin_chunk = min(debut_chunk + chunk_size, nombre_lignes)
            
            print(f"🔄 Chunk {chunk_num+1}/{chunks_total}: lignes {debut_chunk+1:,}-{fin_chunk:,}")
            
            # Générer le chunk en mémoire
            chunk_data = []
            for i in range(debut_chunk, fin_chunk):
                ligne = []
                for col_config in colonnes_config:
                    valeur = generer_valeur_optimisee_gros_volume(
                        col_config, format_donnees, fake, i, compteurs_uniques
                    )
                    ligne.append(valeur)
                chunk_data.append(ligne)
            
            # Écrire le chunk
            writer.writerows(chunk_data)
            
            # Libérer la mémoire
            del chunk_data
            gc.collect()
            
            # Progression
            progression = ((chunk_num + 1) / chunks_total) * 100
            temps_ecoule = time.time() - debut
            print(f"   ✅ {progression:.1f}% - {temps_ecoule:.1f}s écoulées")
    
    temps_total = time.time() - debut
    vitesse = nombre_lignes / temps_total
    print(f"🎉 Génération terminée en {temps_total:.1f}s")
    print(f"⚡ Vitesse: {vitesse:,.0f} lignes/seconde")
    print(f"📁 Fichier: {csv_path}")
    
    return csv_path

def generer_csv_tres_gros_volume(nombre_lignes, colonnes_config, format_donnees, separateur=','):
    """Version ultra-optimisée pour 10+ millions de lignes"""
    from faker import Faker
    import gc
    import time
    import os
    
    print(f"🚀 Mode TRÈS GROS VOLUME activé pour {nombre_lignes:,} lignes")
    print("⚡ Optimisations: Pas d'unicité + Générateurs pré-calculés")
    
    # Vérifier l'espace disque disponible
    taille_estimee = nombre_lignes * len(colonnes_config) * 20  # ~20 bytes/cellule
    taille_estimee_gb = taille_estimee / (1024**3)
    print(f"💾 Taille estimée: {taille_estimee_gb:.2f} GB")
    
    if taille_estimee_gb > 10:
        print("⚠️  ATTENTION: Fichier très volumineux (>10GB)")
        print("💡 Conseil: Utilisez un SSD et vérifiez l'espace libre")
    
    fake = Faker('fr_FR')
    colonnes_noms = [col['nom'] if isinstance(col, dict) else col for col in colonnes_config]
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    extension = 'tsv' if separateur == '\t' else 'csv'
    filename = f'bulk_data_MEGA_{nombre_lignes}_lignes_{timestamp}.{extension}'
    csv_path = os.path.join('output', filename)
    
    if not os.path.exists('output'):
        os.makedirs('output')
    
    # Mode ultra-rapide: pas d'unicité garantie pour éviter la surcharge mémoire
    print("🔥 Mode ultra-rapide: unicité non garantie (performance prioritaire)")
    
    chunk_size = 100000  # Chunks plus gros pour très gros volumes
    chunks_total = (nombre_lignes + chunk_size - 1) // chunk_size
    
    print(f"📊 Génération en {chunks_total} chunks de {chunk_size:,} lignes")
    
    debut = time.time()
    
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=separateur)
        writer.writerow(colonnes_noms)
        
        for chunk_num in range(chunks_total):
            debut_chunk = chunk_num * chunk_size
            fin_chunk = min(debut_chunk + chunk_size, nombre_lignes)
            
            if chunk_num % 10 == 0:  # Affichage moins fréquent
                print(f"🔄 Chunk {chunk_num+1}/{chunks_total}: {debut_chunk+1:,}-{fin_chunk:,}")
            
            # Générer et écrire directement (sans stocker en mémoire)
            for i in range(debut_chunk, fin_chunk):
                ligne = []
                for col_config in colonnes_config:
                    valeur = generer_valeur_ultra_rapide(col_config, format_donnees, i)
                    ligne.append(valeur)
                writer.writerow(ligne)
            
            # Garbage collection moins fréquent
            if chunk_num % 10 == 0:
                gc.collect()
                
            # Progression moins fréquente
            if chunk_num % 50 == 0:
                progression = ((chunk_num + 1) / chunks_total) * 100
                temps_ecoule = time.time() - debut
                vitesse_actuelle = (chunk_num + 1) * chunk_size / temps_ecoule
                temps_reste = (chunks_total - chunk_num - 1) * chunk_size / vitesse_actuelle
                print(f"   ⚡ {progression:.1f}% - {vitesse_actuelle:,.0f} lignes/s - ETA: {temps_reste:.1f}s")
    
    temps_total = time.time() - debut
    vitesse = nombre_lignes / temps_total
    taille_fichier = os.path.getsize(csv_path) / (1024**2)  # MB
    
    print(f"🎉 TRÈS GROS VOLUME généré en {temps_total:.1f}s")
    print(f"⚡ Vitesse finale: {vitesse:,.0f} lignes/seconde")
    print(f"📁 Taille finale: {taille_fichier:.1f} MB")
    print(f"💾 Fichier: {csv_path}")
    
    return csv_path

def generer_valeur_optimisee_gros_volume(col_config, format_donnees, fake, index, compteurs_uniques):
    """Génération optimisée pour gros volumes avec unicité limitée"""
    if isinstance(col_config, dict):
        colonne = col_config['nom']
        est_unique = col_config.get('unique', False)
        min_length = col_config.get('minLength', 0)
    else:
        colonne = col_config
        est_unique = False
        min_length = 0
    
    colonne_lower = colonne.lower()
    
    # Pour les champs uniques en gros volume, on utilise l'index + compteur
    if est_unique and colonne in compteurs_uniques:
        base_index = compteurs_uniques[colonne]
        compteurs_uniques[colonne] += 1
        
        if format_donnees == 'sequence':
            if 'email' in colonne_lower:
                valeur = f'user{base_index:08d}@example.com'
            elif 'id' in colonne_lower:
                valeur = str(base_index + 1)
            else:
                valeur = f'{colonne}{base_index:08d}'
        else:
            # Mode fake avec garantie d'unicité via index
            if 'email' in colonne_lower:
                valeur = f'user{base_index:08d}@{fake.domain_name()}'
            elif 'nom' in colonne_lower:
                valeur = f'{fake.last_name()}{base_index:04d}'
            else:
                valeur = f'{fake.word()}{base_index:06d}'
    else:
        # Génération normale
        if format_donnees == 'sequence':
            valeur = generer_valeur_sequence(colonne, colonne_lower, index)
        elif format_donnees == 'fake':
            valeur = generer_valeur_fake(fake, colonne, colonne_lower, index)
        else:
            valeur = f'{colonne}_{index+1}'
    
    # Assurer la longueur minimum
    return assurer_longueur_minimum(str(valeur), min_length, colonne_lower, fake)

def generer_valeur_ultra_rapide(col_config, format_donnees, index):
    """Génération ultra-rapide sans Faker pour très gros volumes"""
    if isinstance(col_config, dict):
        colonne = col_config['nom']
        min_length = col_config.get('minLength', 0)
    else:
        colonne = col_config
        min_length = 0
    
    colonne_lower = colonne.lower()
    
    # Génération ultra-simple et rapide
    if format_donnees == 'sequence':
        if 'email' in colonne_lower:
            valeur = f'user{index+1:08d}@example.com'
        elif 'tel' in colonne_lower or 'phone' in colonne_lower:
            valeur = f'06{index+1:08d}'
        elif 'nom' in colonne_lower:
            valeur = f'Nom{index+1:08d}'
        elif 'id' in colonne_lower:
            valeur = str(index + 1)
        else:
            valeur = f'{colonne}{index+1:08d}'
    else:
        # Mode "fake" simplifié (sans vraie génération)
        if 'email' in colonne_lower:
            domaines = ['gmail.com', 'yahoo.fr', 'hotmail.com', 'outlook.fr']
            domaine = domaines[index % len(domaines)]
            valeur = f'user{index+1:08d}@{domaine}'
        elif 'nom' in colonne_lower:
            noms = ['Dupont', 'Martin', 'Bernard', 'Dubois', 'Thomas', 'Robert', 'Petit']
            nom = noms[index % len(noms)]
            valeur = f'{nom}{index+1:04d}'
        elif 'ville' in colonne_lower:
            villes = ['Paris', 'Lyon', 'Marseille', 'Toulouse', 'Nice', 'Nantes', 'Strasbourg']
            valeur = villes[index % len(villes)]
        else:
            valeur = f'{colonne}_{index+1:08d}'
    
    # Assurer longueur minimum de façon ultra-simple
    while len(valeur) < min_length:
        valeur += str((index % 10))
    
    return valeur

if __name__ == '__main__':
    print("🌐 === BULK GENERATOR - INTERFACE WEB ===")
    print("Interface web pour génération de PDF et CSV en masse")
    print()
    print("🔗 Accès: http://localhost:5000")
    print("📁 Fichiers générés dans: ./output/")
    print()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
