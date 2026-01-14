# 🏃‍♂️ Sports Performance Pro - Plateforme de Suivi des Performances Sportives

## 📋 Description du Projet

**Sports Performance Pro** est une application web complète développée avec Streamlit pour le suivi, l'analyse et l'optimisation des performances sportives. Cette plateforme permet aux athlètes et sportifs de tous niveaux d'enregistrer leurs entraînements, d'analyser leurs données avec des métriques avancées, de visualiser leurs progrès de manière interactive et de générer des rapports détaillés en PDF.

### 🎯 Thèmes du Projet

- **Calcul formel** : Calculs scientifiques de métriques sportives (TRIMP, VO2max, zones cardiaques, etc.)
- **Tableaux de bord** : Visualisations interactives et métriques en temps réel
- **Exportation des données** : Génération de rapports PDF et export CSV
- **Visualisation des données** : Graphiques interactifs avec Plotly

---

## ✨ Fonctionnalités Principales

### 1. 📊 Tableau de Bord
- **Vue d'ensemble des performances** : Métriques clés (entraînements, distance, durée, calories)
- **Filtres avancés** : Par sport, date de début/fin
- **Visualisations interactives** :
  - Évolution de la distance et durée
  - Analyse de la fréquence cardiaque
  - Répartition par sport et type d'entraînement
- **Widget hebdomadaire** : Statistiques de la semaine et de l'année avec indicateurs visuels

### 2. ➕ Enregistrement de Performances
- Formulaire complet pour enregistrer :
  - Informations générales (date, sport, type d'entraînement, durée, distance, calories)
  - Métriques cardiaques (FC moyenne, FC max)
  - Vitesse moyenne et élévation
  - Notes personnelles
- Validation et sauvegarde automatique dans la session

### 3. 📈 Analyse Avancée
- **Statistiques générales** :
  - Nombre d'entraînements
  - Distance/durée moyenne par séance
  - Fréquence d'entraînement
  - Vitesse et calories moyennes
- **Analyse de progression** : Calcul du pourcentage d'amélioration sur la distance et la vitesse
- **Zones de fréquence cardiaque** :
  - Calcul automatique des 5 zones cardiaques
  - Visualisation graphique avec votre FC moyenne
  - Zones : Récupération, Endurance, Tempo, Seuil, VO2 Max
- **Corrélations** :
  - Distance vs Calories
  - Vitesse vs Fréquence cardiaque
  - Analyse par sport et type d'entraînement
- **Intensité hebdomadaire** : Graphique de charge d'entraînement par semaine

### 4. 🎯 Objectifs & Records
- **Suivi des objectifs** :
  - Objectifs hebdomadaires (distance, séances, durée, calories)
  - Objectifs mensuels (distance)
  - Barres de progression visuelles
  - Graphique radar de progression
- **Records personnels** :
  - Plus longue distance par sport
  - Plus longue durée
  - Meilleure vitesse
  - Plus de calories brûlées
- **Profil utilisateur** :
  - Âge, poids, taille, sexe
  - FC au repos et FC max
  - Calcul automatique de l'IMC
  - FC max théorique (formule de Tanaka)
  - VO2max estimé (formule d'Uth)

### 5. 🧮 Calculateurs Sportifs
- **Calculateur d'allure** :
  - Calcul de l'allure (min/km) à partir de distance et temps
  - Calcul de la vitesse moyenne
- **Prédiction de temps de course** :
  - Basé sur la formule de Riegel
  - Prédiction pour différentes distances (5km, 10km, semi-marathon, marathon)
- **Calculateur de calories** :
  - Estimation basée sur le MET (Metabolic Equivalent of Task)
  - Support de multiples activités sportives
- **Calculateur TRIMP** :
  - Training Impulse : mesure de la charge d'entraînement
  - Basé sur la durée, FC moyenne, FC repos, FC max et sexe
  - Indicateur visuel avec jauge d'intensité

### 6. 📥 Import/Export
- **Export PDF** :
  - Rapport professionnel avec métriques clés
  - Tableau détaillé des entraînements
  - Personnalisable par période et sport
- **Export CSV** :
  - Export complet des données
  - Compatible avec Excel et autres outils
- **Import CSV** :
  - Import de données existantes
  - Mode ajout ou remplacement
  - Validation et aperçu avant import
  - Modèle CSV téléchargeable

---

## 🛠️ Technologies Utilisées

### Frameworks et Bibliothèques
- **Streamlit** : Framework web pour l'interface utilisateur
- **Pandas** : Manipulation et analyse de données
- **NumPy** : Calculs numériques
- **Plotly** : Visualisations interactives (express et graph_objects)
- **ReportLab** : Génération de rapports PDF

### Fonctionnalités Techniques
- **Session State** : Persistance des données pendant la session
- **CSS personnalisé** : Design moderne avec support light/dark mode
- **Responsive Design** : Interface adaptative
- **Animations CSS** : Transitions fluides

---

## 📦 Installation

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes d'Installation

1. **Cloner le dépôt** (ou télécharger les fichiers)
   ```bash
   git clone <url-du-repo>
   cd "S1CNIPY Projet Fin Module"
   ```

2. **Créer un environnement virtuel** (recommandé)
   ```bash
   python -m venv venv
   
   # Sur Windows
   venv\Scripts\activate
   
   # Sur Linux/Mac
   source venv/bin/activate
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Lancer l'application**
   ```bash
   streamlit run mainapp.py
   ```

5. **Accéder à l'application**
   - L'application s'ouvrira automatiquement dans votre navigateur
   - URL par défaut : `http://localhost:8501`

---

## 📚 Guide d'Utilisation

### Première Utilisation

1. **Configurer votre profil** :
   - Allez dans "🎯 Objectifs & Records" → "👤 Mon Profil"
   - Remplissez vos informations (âge, poids, taille, FC repos, FC max)
   - Cliquez sur "💾 Sauvegarder le Profil"

2. **Définir vos objectifs** :
   - Dans "🎯 Objectifs & Records" → "📊 Suivi des Objectifs"
   - Définissez vos objectifs hebdomadaires et mensuels
   - Sauvegardez vos objectifs

3. **Enregistrer votre première performance** :
   - Allez dans "➕ Ajouter Performance"
   - Remplissez le formulaire avec les données de votre entraînement
   - Cliquez sur "💾 Enregistrer la Performance"

### Utilisation Quotidienne

1. **Enregistrer un entraînement** : Utilisez le formulaire dans "➕ Ajouter Performance"
2. **Consulter vos statistiques** : Visualisez vos progrès dans "📊 Tableau de bord"
3. **Analyser vos performances** : Utilisez "📈 Analyse Avancée" pour des insights détaillés
4. **Suivre vos objectifs** : Vérifiez votre progression dans "🎯 Objectifs & Records"

### Export de Données

1. **Générer un rapport PDF** :
   - Allez dans "📥 Import/Export" → "📤 Exporter"
   - Sélectionnez la période et les sports
   - Cliquez sur "📄 Générer le Rapport PDF"
   - Téléchargez le fichier

2. **Exporter en CSV** :
   - Dans la même section, cliquez sur "📥 Télécharger le CSV"
   - Ouvrez le fichier dans Excel ou un autre tableur

---

## 🔬 Formules Scientifiques Implémentées

### 1. Zones de Fréquence Cardiaque
Les 5 zones sont calculées selon la méthode de Karvonen :
```
Zone = FC_repos + (pourcentage × (FC_max - FC_repos))
```
- Zone 1 (Récupération) : 50-60% de la réserve cardiaque
- Zone 2 (Endurance) : 60-70%
- Zone 3 (Tempo) : 70-80%
- Zone 4 (Seuil) : 80-90%
- Zone 5 (VO2 Max) : 90-100%

### 2. TRIMP (Training Impulse)
Formule de Banister pour mesurer la charge d'entraînement :
```
TRIMP = durée × ΔFC × facteur_d'intensité
```
où :
- `ΔFC = (FC_moy - FC_repos) / (FC_max - FC_repos)`
- Facteur d'intensité : `y = 0.64 × e^(1.92 × ΔFC)` (Homme) ou `y = 0.86 × e^(1.67 × ΔFC)` (Femme)

### 3. Prédiction de Temps (Formule de Riegel)
```
T2 = T1 × (D2/D1)^1.06
```
où T1 et T2 sont les temps, D1 et D2 sont les distances.

### 4. FC Max Théorique (Formule de Tanaka)
```
FC_max = 208 - 0.7 × âge
```

### 5. VO2max Estimé (Formule d'Uth)
```
VO2max = 15.3 × (FC_max / FC_repos)
```

### 6. IMC (Indice de Masse Corporelle)
```
IMC = poids (kg) / (taille (m))²
```

### 7. Calories (Métabolisme Équivalent)
```
Calories = MET × poids (kg) × durée (heures)
```

---

## 📁 Structure du Projet

```
S1CNIPY Projet Fin Module/
│
├── mainapp.py              # Application principale Streamlit
├── draft.py                # Fichier de brouillon (optionnel)
├── requirements.txt        # Dépendances Python
├── .gitignore             # Fichiers ignorés par Git
└── README.md              # Documentation (ce fichier)
```

### Structure du Code

Le fichier `mainapp.py` est organisé en sections :

1. **Imports et Configuration** (lignes 1-22)
   - Import des bibliothèques
   - Configuration de la page Streamlit

2. **CSS et Styling** (lignes 24-330)
   - Styles personnalisés avec support light/dark mode
   - Animations et transitions

3. **Initialisation des Données** (lignes 332-359)
   - Initialisation des DataFrames
   - Configuration des objectifs et profil par défaut

4. **Fonctions de Calcul** (lignes 361-497)
   - `calculer_metriques_avancees()` : Calcul des statistiques
   - `calculer_zones_fc()` : Zones cardiaques
   - `calculer_trimp()` : Charge d'entraînement
   - `calculer_pace()` : Allure
   - `predire_temps_course()` : Prédiction de temps
   - `calculer_imc()` : IMC
   - `calculer_fc_max_theorique()` : FC max théorique
   - `calculer_vo2max_estime()` : VO2max
   - `obtenir_records_personnels()` : Records
   - `calculer_progression_objectifs()` : Progression

5. **Génération PDF** (lignes 499-584)
   - `generer_rapport_pdf()` : Création du rapport PDF

6. **Widget Hebdomadaire** (lignes 586-656)
   - `create_weekly_widget()` : Widget de statistiques

7. **Interface Utilisateur** (lignes 658-1688)
   - En-tête et navigation
   - Sections principales :
     - Tableau de bord
     - Ajouter Performance
     - Analyse Avancée
     - Objectifs & Records
     - Calculateurs
     - Import/Export

---

## 🎨 Caractéristiques de Design

### Thème Visuel
- **Couleurs principales** : Dégradé violet (#667eea → #764ba2)
- **Police** : Inter (Google Fonts)
- **Style** : Moderne avec glassmorphism
- **Support** : Light et Dark mode

### Animations
- Fade in/out pour les éléments
- Transitions fluides sur les hover
- Effets de profondeur avec les ombres

### Responsive
- Layout adaptatif avec colonnes
- Graphiques interactifs Plotly
- Interface optimisée pour tous les écrans

---

## 🔒 Gestion des Données

### Stockage
- Les données sont stockées dans `st.session_state` (mémoire)
- **Note** : Les données sont perdues à la fermeture de l'application
- Pour une persistance permanente, utilisez l'export CSV

### Format des Données
Les performances sont stockées dans un DataFrame avec les colonnes :
- `date` : Date de l'entraînement
- `sport` : Type de sport
- `type_entrainement` : Type d'entraînement
- `duree_min` : Durée en minutes
- `distance_km` : Distance en kilomètres
- `calories` : Calories brûlées
- `frequence_cardiaque_moy` : FC moyenne (bpm)
- `frequence_cardiaque_max` : FC max (bpm)
- `vitesse_moy` : Vitesse moyenne (km/h)
- `elevation_m` : Élévation en mètres
- `notes` : Notes personnelles

---

## 🚀 Améliorations Futures Possibles

- [ ] Persistance des données avec base de données (SQLite, PostgreSQL)
- [ ] Authentification utilisateur (multi-utilisateurs)
- [ ] Synchronisation avec appareils fitness (Garmin, Strava, etc.)
- [ ] Notifications et rappels d'entraînement
- [ ] Planification d'entraînements
- [ ] Comparaison avec d'autres athlètes (anonymisée)
- [ ] Export vers formats supplémentaires (JSON, Excel)
- [ ] Graphiques supplémentaires (heatmaps, calendriers)
- [ ] Mode hors ligne (PWA)
- [ ] Application mobile

---

## 🐛 Dépannage

### Problèmes Courants

1. **L'application ne démarre pas**
   - Vérifiez que toutes les dépendances sont installées : `pip install -r requirements.txt`
   - Vérifiez votre version de Python : `python --version` (doit être 3.8+)

2. **Les graphiques ne s'affichent pas**
   - Vérifiez votre connexion internet (pour les polices Google Fonts)
   - Assurez-vous que Plotly est correctement installé

3. **Erreur lors de la génération PDF**
   - Vérifiez que ReportLab est installé : `pip install reportlab`
   - Assurez-vous d'avoir des données à exporter

4. **Les données disparaissent après fermeture**
   - C'est normal : les données sont en mémoire
   - Utilisez l'export CSV pour sauvegarder vos données
   - Importez-les au prochain démarrage

---

## 📝 Licence

Ce projet est développé dans le cadre d'un projet de fin de module (S1CNIPY - ENSET GLSID).

---

## 👥 Auteurs

Développé dans le cadre du projet de fin de module S1CNIPY.

---

## 🙏 Remerciements

- **Streamlit** pour le framework web
- **Plotly** pour les visualisations interactives
- **ReportLab** pour la génération PDF
- La communauté open-source Python

---

## 📞 Support

Pour toute question ou problème, veuillez créer une issue dans le dépôt du projet.

---

**Version** : 1.0.0  
**Dernière mise à jour** : 2024

---

*Bon entraînement ! 💪🏃‍♂️*
