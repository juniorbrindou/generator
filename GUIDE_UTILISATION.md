# 🙏 Guide d'Utilisation - Générateur de Versets

## 📋 Étapes Recommandées

### 1. 🧪 Test de Démonstration (OBLIGATOIRE)
```bash
python demo_simple.py
```
- Génère 20 versets sur 2 pages
- Vérifiez la taille et la lisibilité
- Testez l'impression et la découpe

### 2. 🔬 Test Intermédiaire (RECOMMANDÉ)
```bash
python test_final.py
```
- Génère 100 versets sur ~6 pages
- Validation finale du format
- Test de performance

### 3. 🎯 Génération Complète (1000 versets)
```bash
python generateur_versets.py
```
- Génère les 1000 versets complets
- ~56 pages A4
- Prêt pour l'impression finale !

## 📄 Fichiers Générés

- `output/DEMO_20_versets.pdf` - Démonstration
- `output/TEST_100_versets_final.pdf` - Test intermédiaire  
- `output/versets_1000_papiers_YYYYMMDD_HHMMSS.pdf` - Version finale

## 🖨️ Instructions d'Impression

1. **Paramètres d'impression recommandés** :
   - Format : A4
   - Qualité : Normale ou Élevée
   - Marges : Respecter les marges du PDF
   - Recto uniquement

2. **Découpe** :
   - Utilisez les lignes grises comme guide
   - Chaque papier fait ~5cm × 3.8cm
   - Un cutter ou des ciseaux feront l'affaire

3. **Vérification** :
   - Testez d'abord avec la version démo
   - Vérifiez la lisibilité du texte
   - Ajustez si nécessaire dans `config.py`

## ⚙️ Personnalisation

### Modifier la Taille des Papiers
Dans `config.py`, ajustez :
```python
PAPIER_LARGEUR = 144  # ~5cm (en points)
PAPIER_HAUTEUR = 85   # ~3cm (en points) - Format optimisé 6×4
```

### Changer la Police
```python
POLICE_TAILLE = 8         # Taille du texte principal (optimisée)
POLICE_REFERENCE_TAILLE = 6  # Taille des références (optimisée)
```

### Ajouter Vos Versets
Dans `versets/base_versets.py`, ajoutez à la liste :
```python
("Votre verset personnalisé", "Référence"),
```

## 🎯 Utilisation Pratique

### Pour 1000 Personnes
- Imprimez les ~48 pages (optimisé !)
- Découpez ~1000 papiers
- Distribuez avec vos beignets/pâtisseries

### Calculs Pratiques
- **Temps d'impression** : ~12-15 minutes (moins de pages !)
- **Temps de découpe** : ~2-3 heures (selon la méthode)
- **Coût papier** : ~1€ pour 48 pages A4

## 🚨 Conseils Importants

1. **TOUJOURS tester d'abord** avec `demo_simple.py`
2. **Vérifier l'impression** sur une page test
3. **Prévoir du temps** pour la découpe (ou recruter des bénévoles !)
4. **Garder quelques papiers** en réserve

## 🤝 Partage et Distribution

### Idées Créatives
- 🍩 Dans des sacs de beignets
- ☕ Avec des boissons chaudes  
- 🎁 Dans des petits cadeaux
- 📚 Comme marque-pages
- 💌 Messages personnels

### Moment de Distribution
- Sourire et bienveillance
- Pas de pression, juste du partage
- Laisser les gens libres de lire ou non

---

**🙏 Que ces versets apportent joie et espoir à tous ceux qui les recevront !**
