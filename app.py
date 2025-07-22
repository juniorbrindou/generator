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
    """Génère un fichier CSV avec des données en masse"""
    from faker import Faker
    fake = Faker('fr_FR')  # Données en français
    
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
        # Utiliser le séparateur personnalisé
        writer = csv.writer(csvfile, delimiter=separateur)
        
        # Écrire l'en-tête
        writer.writerow(colonnes_noms)
        
        # Générer les lignes de données
        for i in range(nombre_lignes):
            ligne = []
            
            for col_config in colonnes_config:
                if isinstance(col_config, dict):
                    colonne = col_config['nom']
                    est_unique = col_config.get('unique', False)
                else:
                    colonne = col_config
                    est_unique = False
                
                colonne_lower = colonne.lower()
                valeur = None
                
                # Générer la valeur selon le format
                if format_donnees == 'sequence':
                    valeur = generer_valeur_sequence(colonne, colonne_lower, i)
                elif format_donnees == 'fake':
                    valeur = generer_valeur_fake(fake, colonne, colonne_lower, i)
                else:
                    valeur = f'{colonne}_{i+1}'
                
                # Garantir l'unicité si nécessaire
                if est_unique:
                    tentatives = 0
                    while valeur in valeurs_uniques[colonne] and tentatives < 100:
                        if format_donnees == 'fake':
                            valeur = generer_valeur_fake(fake, colonne, colonne_lower, i + tentatives * 1000)
                        else:
                            valeur = f"{valeur}_{tentatives:03d}"
                        tentatives += 1
                    
                    valeurs_uniques[colonne].add(valeur)
                
                ligne.append(valeur)
            
            writer.writerow(ligne)
            
            # Afficher le progrès pour les gros fichiers
            if (i + 1) % 10000 == 0:
                print(f"📊 Génération CSV: {i+1}/{nombre_lignes} lignes...")
    
    print(f"✅ CSV généré: {csv_path}")
    return csv_path

def generer_valeur_sequence(colonne, colonne_lower, index):
    """Génère une valeur séquentielle"""
    if 'nom' in colonne_lower:
        return f'Nom{(index+1):06d}'
    elif 'email' in colonne_lower or 'mail' in colonne_lower:
        return f'user{(index+1):06d}@example.com'
    elif 'tel' in colonne_lower or 'phone' in colonne_lower:
        return f'06{(index+1):08d}'
    elif 'id' in colonne_lower:
        return index + 1
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
        return index + 1
    else:
        return fake.word()

if __name__ == '__main__':
    print("🌐 === BULK GENERATOR - INTERFACE WEB ===")
    print("Interface web pour génération de PDF et CSV en masse")
    print()
    print("🔗 Accès: http://localhost:5000")
    print("📁 Fichiers générés dans: ./output/")
    print()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
