# Configuration pour le générateur de versets

# Dimensions des petits papiers (en points - 1 point = 1/72 pouce)
PAPIER_LARGEUR = 144  # ~5cm
PAPIER_HAUTEUR = 85   # ~3cm (réduit pour 6 lignes)

# Marges et espacement
MARGE_PAGE = 36  # 1.27cm
ESPACEMENT_HORIZONTAL = 18  # 0.63cm
ESPACEMENT_VERTICAL = 15    # 0.53cm (réduit pour plus de lignes)

# Police et texte
POLICE_NOM = "Helvetica"
POLICE_TAILLE = 8          # Réduit pour le nouveau format
POLICE_REFERENCE_TAILLE = 6 # Réduit pour le nouveau format
POLICE_NUMERO_TAILLE = 5    # Taille pour le numéro du verset
COULEUR_TEXTE = "black"
COULEUR_NUMERO = "gray"     # Gris pour le numéro (impression N&B)

# Format de page (A4 par défaut)
PAGE_LARGEUR = 595  # A4 largeur en points
PAGE_HAUTEUR = 842  # A4 hauteur en points

# Calcul automatique du nombre de papiers par page
PAPIERS_PAR_LIGNE = int((PAGE_LARGEUR - 2 * MARGE_PAGE + ESPACEMENT_HORIZONTAL) / (PAPIER_LARGEUR + ESPACEMENT_HORIZONTAL))
PAPIERS_PAR_COLONNE = int((PAGE_HAUTEUR - 2 * MARGE_PAGE + ESPACEMENT_VERTICAL) / (PAPIER_HAUTEUR + ESPACEMENT_VERTICAL))
PAPIERS_PAR_PAGE = PAPIERS_PAR_LIGNE * PAPIERS_PAR_COLONNE

# Nombre total de versets souhaité
NOMBRE_VERSETS = 1000

# Bordures et style
AFFICHER_BORDURES = True
COULEUR_BORDURES = "gray"
EPAISSEUR_BORDURES = 0.5
AFFICHER_NUMEROS = True     # Afficher le numéro sur chaque verset
STYLE_DECORATIF = True      # Ajouter des éléments décoratifs (impression N&B)
