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
        colonnes = data.get('colonnes', ['Nom', 'Email', 'Telephone'])
        format_donnees = data.get('format', 'fake')  # fake, sequence, custom
        
        # Générer le CSV
        csv_path = generer_csv_bulk(nombre_lignes, colonnes, format_donnees)
        
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

def generer_csv_bulk(nombre_lignes, colonnes, format_donnees):
    """Génère un fichier CSV avec des données en masse"""
    from faker import Faker
    fake = Faker('fr_FR')  # Données en français
    
    # Créer le nom du fichier
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'bulk_data_{nombre_lignes}_lignes_{timestamp}.csv'
    csv_path = os.path.join('output', filename)
    
    # S'assurer que le dossier output existe
    if not os.path.exists('output'):
        os.makedirs('output')
    
    # Générer les données
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Écrire l'en-tête
        writer.writerow(colonnes)
        
        # Générer les lignes de données
        for i in range(nombre_lignes):
            ligne = []
            for colonne in colonnes:
                colonne_lower = colonne.lower()
                
                if format_donnees == 'sequence':
                    # Données séquentielles
                    if 'nom' in colonne_lower:
                        ligne.append(f'Nom{i+1:06d}')
                    elif 'email' in colonne_lower or 'mail' in colonne_lower:
                        ligne.append(f'user{i+1:06d}@example.com')
                    elif 'tel' in colonne_lower or 'phone' in colonne_lower:
                        ligne.append(f'06{i+1:08d}')
                    elif 'id' in colonne_lower:
                        ligne.append(i+1)
                    else:
                        ligne.append(f'{colonne}{i+1:06d}')
                        
                elif format_donnees == 'fake':
                    # Données réalistes avec Faker
                    if 'nom' in colonne_lower or 'name' in colonne_lower:
                        ligne.append(fake.name())
                    elif 'prenom' in colonne_lower or 'firstname' in colonne_lower:
                        ligne.append(fake.first_name())
                    elif 'email' in colonne_lower or 'mail' in colonne_lower:
                        ligne.append(fake.email())
                    elif 'tel' in colonne_lower or 'phone' in colonne_lower:
                        ligne.append(fake.phone_number())
                    elif 'adresse' in colonne_lower or 'address' in colonne_lower:
                        ligne.append(fake.address().replace('\n', ', '))
                    elif 'ville' in colonne_lower or 'city' in colonne_lower:
                        ligne.append(fake.city())
                    elif 'code' in colonne_lower and 'postal' in colonne_lower:
                        ligne.append(fake.postcode())
                    elif 'entreprise' in colonne_lower or 'company' in colonne_lower:
                        ligne.append(fake.company())
                    elif 'date' in colonne_lower:
                        ligne.append(fake.date())
                    elif 'id' in colonne_lower:
                        ligne.append(i+1)
                    else:
                        ligne.append(fake.word())
                else:
                    # Format personnalisé ou par défaut
                    ligne.append(f'{colonne}_{i+1}')
            
            writer.writerow(ligne)
            
            # Afficher le progrès pour les gros fichiers
            if (i + 1) % 10000 == 0:
                print(f"📊 Génération CSV: {i+1}/{nombre_lignes} lignes...")
    
    print(f"✅ CSV généré: {csv_path}")
    return csv_path

if __name__ == '__main__':
    print("🌐 === BULK GENERATOR - INTERFACE WEB ===")
    print("Interface web pour génération de PDF et CSV en masse")
    print()
    print("🔗 Accès: http://localhost:5000")
    print("📁 Fichiers générés dans: ./output/")
    print()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
