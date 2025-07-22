# 🚀 Bulk Generator

**Générateur puissant pour créer des PDF et CSV en masse**

Un outil polyvalent qui permet de générer :
- **PDF de versets bibliques** : Jusqu'à 1000+ petits papiers avec versets inspirants
- **Fichiers CSV en masse** : Jusqu'à 1M+ de lignes avec données réalistes ou séquentielles

## ✨ Fonctionnalités

### 📄 Générateur PDF
- ✅ Génération de milliers de petits papiers avec versets bibliques
- ✅ Numérotation automatique (#1 à #1000)
- ✅ Optimisé pour impression et découpe (format A4)
- ✅ Bordures et embellissements pour impression noir & blanc
- ✅ Configuration flexible de la mise en page

### 📊 Générateur CSV  
- ✅ Génération de centaines de milliers de lignes
- ✅ Données réalistes avec Faker (noms, emails, téléphones français)
- ✅ Données séquentielles (Nom001, Nom002, etc.)
- ✅ Colonnes personnalisables
- ✅ Export UTF-8 compatible Excel

### 🌐 Interface Web
- ✅ Interface moderne et intuitive
- ✅ Configuration en temps réel
- ✅ Aperçu des données avant génération
- ✅ Gestion des fichiers générés
- ✅ Téléchargement direct des fichiers

## 🚀 Démarrage rapide

### Installation
```bash
git clone [votre-repo]
cd bulk-generator
pip install -r requirements.txt
```

### Utilisation

#### Interface Web (Recommandé)
```bash
python lancer_web.py
```
Puis ouvrez http://localhost:5000 dans votre navigateur.

#### Ligne de commande
```bash
# Générer un PDF de 1000 versets
python generateur_versets.py

# Tests avec moins de versets
python demo_simple.py    # 6 versets
python test_final.py     # 20 versets  
python apercu.py         # 100 versets
```
   → Génère `APERCU_numerotation.pdf` (6 versets) pour voir le rendu final

2. **Test de démonstration** (OBLIGATOIRE) :
   ```bash
   python demo_simple.py
   ```
   → Génère `DEMO_20_versets.pdf` (1 page) pour tester l'impression et la découpe

3. **Validation finale** (recommandé) :
   ```bash
   python test_final.py
   ```
   → Génère `TEST_100_versets_final.pdf` (~5 pages) pour validation

4. **Production finale** :
   ```bash
   python generateur_versets.py
   ```
   → Génère le PDF complet avec 1000 versets numérotés (~48 pages)

### 📊 Informations du projet :
```bash
python info.py
```

## 📋 Installation

1. **Cloner le projet** (ou télécharger)
2. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```
3. **Lancer la démonstration** pour tester
4. **Générer les 1000 versets** quand vous êtes satisfait du format

## 🔧 Configuration

Modifiez `config.py` pour ajuster :
- **Taille des papiers** (`PAPIER_LARGEUR`, `PAPIER_HAUTEUR`)
- **Police et taille** (`POLICE_NOM`, `POLICE_TAILLE`)
- **Marges et espacements**
- **Affichage des bordures**

## ✨ Nouvelles Fonctionnalités

### � Numérotation des Versets
- **Chaque verset est numéroté** de #1 à #1000
- **Position** : Coin supérieur droit de chaque papier
- **Style** : Discret en gris, taille 5pt
- **Avantage** : Permet de savoir quel verset quelqu'un a choisi !

### 🎨 Design Embelli (Impression N&B)
- **Bordures de découpe** avec marques aux coins
- **Petit point décoratif** en bas à gauche
- **Références en gris** pour un look élégant
- **Optimisé noir et blanc** : Pas de couleurs, juste du style !

### 📐 Mise en Page Optimisée
- **21 papiers par page** (3×7) au lieu de 18
- **Économie de papier** : 8 pages en moins !
- **Police adaptée** : 8pt pour le texte, 6pt pour les références

## 📝 Contenu

Le projet inclut plus de 100 versets de base couvrant :
- 💙 L'amour et la compassion
- ☮️ La paix et l'espoir
- 😊 La joie et les bénédictions
- 💪 La force et le courage
- 🧠 La sagesse et la foi
- 🛡️ La protection divine

Le générateur répète intelligemment les versets pour atteindre 1000, en évitant les répétitions consécutives.

## 📁 Structure du Projet

```
versets/
├── generateur_versets.py    # 🎯 Script principal (1000 versets)
├── demo_simple.py          # 🧪 Démonstration rapide (20 versets)
├── config.py               # ⚙️ Configuration
├── versets/
│   └── base_versets.py     # 📖 Base de données des versets
├── output/                 # 📄 PDFs générés
├── requirements.txt        # 📦 Dépendances
└── .vscode/tasks.json      # ⚡ Tâches VS Code
```

## 🎨 Tâches VS Code

Depuis VS Code, utilisez `Ctrl+Shift+P` → "Tasks: Run Task" :
- **Générer PDF Demo (20 versets)** - Test rapide
- **Générer PDF Complet (1000 versets)** - Production finale
- **Installer les dépendances** - Configuration

## 📐 Spécifications Techniques

- **Format de page** : A4 (595 × 842 points)
- **Papiers par page** : 21 (3×7) - OPTIMISÉ !
- **Dimensions d'un papier** : 5.1cm × 3.0cm
- **Police** : Helvetica 8pt (texte), 6pt (référence)
- **Nombre de pages total** : ~48 pages pour 1000 versets

## 🍩 Instructions d'Utilisation

1. **Imprimez** le PDF sur papier A4 standard
2. **Découpez** le long des lignes grises
3. **Distribuez** avec vos beignets ou lors de moments de partage
4. **Partagez** la joie et l'espoir ! 🙏

## 💡 Idées d'Usage

- 🍩 Accompagner des beignets ou pâtisseries
- ☕ Messages dans les tasses de café
- 🎁 Petites attentions dans les cadeaux
- 📚 Marque-pages inspirants
- 🤝 Moments de partage communautaire
- 🙏 Encouragements quotidiens

---

*Que ces versets apportent joie, réconfort et espoir à tous ceux qui les liront !* �️✨
