import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import base64

# Configuration de la page avec thème moderne
st.set_page_config(
    page_title="Sports Performance Pro",
    page_icon="🏃‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé adaptatif pour light/dark mode
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    /* Variables CSS pour le thème */
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --primary-color: #667eea;
        --secondary-color: #764ba2;
        --success-color: #48bb78;
    }
    
    /* ========== LIGHT MODE (défaut) ========== */
    [data-testid="stAppViewContainer"] {
        --bg-primary: rgba(255, 255, 255, 0.95);
        --bg-secondary: #f7fafc;
        --bg-tertiary: #edf2f7;
        --text-primary: #2d3748;
        --text-secondary: #4a5568;
        --text-muted: #718096;
        --border-color: #e2e8f0;
        --shadow-color: rgba(0, 0, 0, 0.1);
        --card-bg: linear-gradient(135deg, #ffffff 0%, #f7fafc 100%);
    }
    
    /* ========== DARK MODE ========== */
    [data-testid="stAppViewContainer"][data-theme="dark"],
    .stApp[data-theme="dark"] [data-testid="stAppViewContainer"],
    @media (prefers-color-scheme: dark) {
        [data-testid="stAppViewContainer"] {
            --bg-primary: rgba(26, 32, 44, 0.95);
            --bg-secondary: #2d3748;
            --bg-tertiary: #4a5568;
            --text-primary: #f7fafc;
            --text-secondary: #e2e8f0;
            --text-muted: #a0aec0;
            --border-color: #4a5568;
            --shadow-color: rgba(0, 0, 0, 0.3);
            --card-bg: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
        }
    }
    
    /* Force dark mode styles when Streamlit is in dark mode */
    .stApp[data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Conteneur principal avec glassmorphism adaptatif */
    .block-container {
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
    }
    
    /* Titres avec gradient (fonctionne en light et dark) */
    h1 {
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
        font-size: 3rem;
        margin-bottom: 1.5rem;
        text-align: center;
        animation: fadeInDown 0.8s ease-in-out;
    }
    
    h2 {
        font-weight: 600;
        font-size: 1.8rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 3px solid var(--primary-color);
        padding-bottom: 0.5rem;
        animation: fadeInLeft 0.8s ease-in-out;
    }
    
    h3 {
        font-weight: 600;
        font-size: 1.3rem;
    }
    
    /* Cartes de métriques améliorées */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.9rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    div[data-testid="metric-container"] {
        border-radius: 15px;
        padding: 1.5rem;
        border-left: 5px solid var(--primary-color);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        animation: fadeInUp 0.6s ease-in-out;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(102, 126, 234, 0.3);
    }
    
    /* Boutons stylisés */
    .stButton > button {
        background: var(--primary-gradient) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Inputs améliorés */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select,
    .stTextArea > div > div > textarea {
        border-radius: 10px;
        padding: 0.75rem;
        transition: all 0.3s ease;
        font-size: 1rem;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary-color) !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2) !important;
    }
    
    /* Tabs personnalisés */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        border: 2px solid transparent;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--primary-gradient) !important;
        color: white !important;
        border-color: var(--primary-color);
    }
    
    /* DataFrames stylisés */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
    }
    
    /* Messages info/success/warning */
    .stAlert {
        border-radius: 12px;
        border-left: 5px solid;
        animation: slideInRight 0.5s ease-in-out;
    }
    
    /* Animations */
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes fadeInLeft {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(100px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    /* Badge de statistiques */
    .stat-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        color: white;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
        margin: 0.25rem;
        box-shadow: 0 2px 5px rgba(72, 187, 120, 0.3);
    }
    
    /* Graphiques Plotly */
    .js-plotly-plot {
        border-radius: 15px;
        overflow: hidden;
    }
    
    /* Progress bars personnalisés */
    .stProgress > div > div > div {
        background: var(--primary-gradient) !important;
    }
    
    /* Selectbox et autres widgets */
    [data-baseweb="select"] {
        border-radius: 10px !important;
    }
    
    /* Radio buttons */
    .stRadio > div {
        gap: 1rem;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        border-radius: 10px;
        font-weight: 600;
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        border-radius: 10px;
    }
    
    /* Download button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%) !important;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a202c 0%, #2d3748 100%);
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #e2e8f0;
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4 {
        color: #f7fafc !important;
        -webkit-text-fill-color: #f7fafc !important;
        background: none !important;
    }
    
    /* Multiselect tags */
    [data-baseweb="tag"] {
        background: var(--primary-gradient) !important;
        border-radius: 8px !important;
    }
    
    /* Info, warning, success, error boxes */
    .stAlert > div {
        border-radius: 10px;
    }
    
    /* Number input spinner buttons */
    .stNumberInput button {
        border-radius: 8px !important;
    }
    
    /* Slider */
    .stSlider > div > div > div {
        background: var(--primary-gradient) !important;
    }
    
    /* Column gaps */
    [data-testid="column"] {
        padding: 0 0.5rem;
    }
    
    /* Plotly charts dark mode compatibility */
    .js-plotly-plot .plotly .modebar {
        background: transparent !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialisation des données dans session_state
if 'performances' not in st.session_state:
    st.session_state.performances = pd.DataFrame(columns=[
        'date', 'sport', 'type_entrainement', 'duree_min', 'distance_km', 
        'calories', 'frequence_cardiaque_moy', 'frequence_cardiaque_max',
        'vitesse_moy', 'elevation_m', 'notes'
    ])

# Initialisation des objectifs
if 'objectifs' not in st.session_state:
    st.session_state.objectifs = {
        'distance_hebdo': 50.0,
        'distance_mensuel': 200.0,
        'seances_hebdo': 4,
        'calories_hebdo': 2000,
        'duree_hebdo': 300  # minutes
    }

# Initialisation du profil utilisateur
if 'profil' not in st.session_state:
    st.session_state.profil = {
        'age': 30,
        'poids': 70.0,
        'taille': 175,
        'fc_repos': 60,
        'fc_max': 190,
        'sexe': 'Homme'
    }

# Fonctions de calcul des métriques
def calculer_metriques_avancees(df):
    if df.empty:
        return {}
    
    metriques = {
        'total_entrainements': len(df),
        'duree_totale': df['duree_min'].sum(),
        'distance_totale': df['distance_km'].sum(),
        'calories_totales': df['calories'].sum(),
        'vitesse_moyenne': df['vitesse_moy'].mean(),
        'fc_moyenne': df['frequence_cardiaque_moy'].mean(),
        'elevation_totale': df['elevation_m'].sum()
    }
    
    if len(df) > 1:
        df_sorted = df.sort_values('date')
        metriques['progression_distance'] = (
            (df_sorted['distance_km'].iloc[-1] - df_sorted['distance_km'].iloc[0]) / 
            df_sorted['distance_km'].iloc[0] * 100 if df_sorted['distance_km'].iloc[0] > 0 else 0
        )
        metriques['progression_vitesse'] = (
            (df_sorted['vitesse_moy'].iloc[-1] - df_sorted['vitesse_moy'].iloc[0]) / 
            df_sorted['vitesse_moy'].iloc[0] * 100 if df_sorted['vitesse_moy'].iloc[0] > 0 else 0
        )
    
    return metriques

def calculer_zones_fc(fc_max, fc_repos=60):
    zones = {
        'Zone 1 (Récupération)': (fc_repos + 0.5 * (fc_max - fc_repos), fc_repos + 0.6 * (fc_max - fc_repos)),
        'Zone 2 (Endurance)': (fc_repos + 0.6 * (fc_max - fc_repos), fc_repos + 0.7 * (fc_max - fc_repos)),
        'Zone 3 (Tempo)': (fc_repos + 0.7 * (fc_max - fc_repos), fc_repos + 0.8 * (fc_max - fc_repos)),
        'Zone 4 (Seuil)': (fc_repos + 0.8 * (fc_max - fc_repos), fc_repos + 0.9 * (fc_max - fc_repos)),
        'Zone 5 (VO2 Max)': (fc_repos + 0.9 * (fc_max - fc_repos), fc_max)
    }
    return zones

def calculer_trimp(duree_min, fc_moy, fc_repos, fc_max, sexe='Homme'):
    """
    Calcul du TRIMP (Training Impulse) - Mesure de la charge d'entraînement
    Formule de Banister: TRIMP = durée × ΔFC × facteur d'intensité
    """
    if fc_max <= fc_repos:
        return 0
    
    delta_fc = (fc_moy - fc_repos) / (fc_max - fc_repos)
    delta_fc = max(0, min(1, delta_fc))  # Limiter entre 0 et 1
    
    # Facteur selon le sexe (coefficient exponentiel)
    if sexe == 'Homme':
        y = 0.64 * np.exp(1.92 * delta_fc)
    else:
        y = 0.86 * np.exp(1.67 * delta_fc)
    
    trimp = duree_min * delta_fc * y
    return round(trimp, 1)

def calculer_pace(distance_km, duree_min):
    """Calcule l'allure en min/km"""
    if distance_km <= 0:
        return 0, 0
    pace_total = duree_min / distance_km
    pace_min = int(pace_total)
    pace_sec = int((pace_total - pace_min) * 60)
    return pace_min, pace_sec

def predire_temps_course(distance_ref, temps_ref_min, distance_cible):
    """
    Prédit le temps pour une distance cible basé sur une performance de référence
    Utilise la formule de Riegel: T2 = T1 × (D2/D1)^1.06
    """
    if distance_ref <= 0 or temps_ref_min <= 0:
        return 0
    temps_predit = temps_ref_min * (distance_cible / distance_ref) ** 1.06
    return temps_predit

def calculer_imc(poids, taille_cm):
    """Calcule l'IMC (Indice de Masse Corporelle)"""
    taille_m = taille_cm / 100
    if taille_m <= 0:
        return 0
    return round(poids / (taille_m ** 2), 1)

def calculer_fc_max_theorique(age):
    """Calcule la FC max théorique selon la formule de Tanaka"""
    return round(208 - 0.7 * age)

def calculer_vo2max_estime(fc_repos, fc_max):
    """Estime le VO2max basé sur la fréquence cardiaque (formule d'Uth)"""
    if fc_repos <= 0:
        return 0
    return round(15.3 * (fc_max / fc_repos), 1)

def obtenir_records_personnels(df):
    """Identifie les records personnels par sport"""
    if df.empty:
        return {}
    
    records = {}
    for sport in df['sport'].unique():
        df_sport = df[df['sport'] == sport]
        records[sport] = {
            'distance_max': df_sport['distance_km'].max(),
            'duree_max': df_sport['duree_min'].max(),
            'vitesse_max': df_sport['vitesse_moy'].max(),
            'calories_max': df_sport['calories'].max(),
            'meilleur_pace': df_sport['distance_km'].max() / df_sport[df_sport['distance_km'] == df_sport['distance_km'].max()]['duree_min'].values[0] * 60 if df_sport['distance_km'].max() > 0 else 0
        }
    return records

def calculer_progression_objectifs(df, objectifs):
    """Calcule la progression vers les objectifs"""
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())
    start_of_month = today.replace(day=1)
    
    if df.empty:
        return {
            'distance_hebdo': 0,
            'distance_mensuel': 0,
            'seances_hebdo': 0,
            'calories_hebdo': 0,
            'duree_hebdo': 0
        }
    
    df['date'] = pd.to_datetime(df['date'])
    df_week = df[df['date'] >= start_of_week]
    df_month = df[df['date'] >= start_of_month]
    
    return {
        'distance_hebdo': df_week['distance_km'].sum(),
        'distance_mensuel': df_month['distance_km'].sum(),
        'seances_hebdo': len(df_week),
        'calories_hebdo': df_week['calories'].sum(),
        'duree_hebdo': df_week['duree_min'].sum()
    }

def generer_rapport_pdf(df, metriques, graphiques_base64):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
    
    elements = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    elements.append(Paragraph("Rapport de Performance Sportive", title_style))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}", styles['Normal']))
    elements.append(Spacer(1, 20))
    
    elements.append(Paragraph("Résumé des Performances", styles['Heading2']))
    elements.append(Spacer(1, 12))
    
    metriques_data = [
        ['Métrique', 'Valeur'],
        ['Total d\'entraînements', f"{metriques['total_entrainements']}"],
        ['Durée totale', f"{metriques['duree_totale']:.0f} min"],
        ['Distance totale', f"{metriques['distance_totale']:.2f} km"],
        ['Calories brûlées', f"{metriques['calories_totales']:.0f} kcal"],
        ['Vitesse moyenne', f"{metriques['vitesse_moyenne']:.2f} km/h"],
        ['FC moyenne', f"{metriques['fc_moyenne']:.0f} bpm"],
        ['Élévation totale', f"{metriques['elevation_totale']:.0f} m"]
    ]
    
    t = Table(metriques_data, colWidths=[3*inch, 2*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(t)
    elements.append(Spacer(1, 20))
    
    if not df.empty:
        elements.append(PageBreak())
        elements.append(Paragraph("Détail des Entraînements", styles['Heading2']))
        elements.append(Spacer(1, 12))
        
        df_display = df.tail(10).copy()
        df_display['date'] = pd.to_datetime(df_display['date']).dt.strftime('%d/%m/%Y')
        
        table_data = [['Date', 'Sport', 'Type', 'Durée', 'Distance', 'Vitesse']]
        for _, row in df_display.iterrows():
            table_data.append([
                row['date'],
                row['sport'],
                row['type_entrainement'],
                f"{row['duree_min']:.0f} min",
                f"{row['distance_km']:.2f} km",
                f"{row['vitesse_moy']:.2f} km/h"
            ])
        
        t2 = Table(table_data, colWidths=[1.2*inch, 1*inch, 1.2*inch, 1*inch, 1.2*inch, 1.2*inch])
        t2.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(t2)
    
    doc.build(elements)
    buffer.seek(0)
    return buffer

def create_weekly_widget():
    """Widget style Nike pour les statistiques hebdomadaires - Version 100% Streamlit natif"""
    df = st.session_state.performances.copy()
    
    # Header avec emojis
    st.markdown("#### 🏃 🚴 🏊")
    
    if df.empty:
        st.info("📊 Ajoutez votre première performance pour voir vos statistiques !")
        return
    
    df['date'] = pd.to_datetime(df['date'])
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())
    
    # Données de la semaine
    df_week = df[df['date'] >= start_of_week]
    distance_semaine = df_week['distance_km'].sum()
    duree_semaine = df_week['duree_min'].sum()
    
    # Données de l'année
    start_of_year = datetime(today.year, 1, 1)
    df_year = df[df['date'] >= start_of_year]
    distance_annee = df_year['distance_km'].sum()
    
    # Progression par rapport à l'objectif
    objectif_semaine = 50
    progression = min((distance_semaine / objectif_semaine) * 100, 100) if objectif_semaine > 0 else 0
    
    # Message de motivation
    st.success("**Continuez comme ça ! 💪**")
    
    # Stats de la semaine avec metrics natifs
    st.markdown("##### 📅 Cette Semaine")
    st.metric(label="Distance", value=f"{distance_semaine:.1f} km")
    
    # Jours actifs
    jours = ['L', 'M', 'M', 'J', 'V', 'S', 'D']
    jours_actifs = df_week['date'].dt.dayofweek.unique().tolist()
    jours_display = " ".join([f"**{j}**" if i in jours_actifs else j for i, j in enumerate(jours)])
    st.markdown(f"Jours actifs: {jours_display}")
    
    # Stats temps et séances
    c1, c2 = st.columns(2)
    with c1:
        heures = int(duree_semaine // 60)
        minutes = int(duree_semaine % 60)
        st.metric("Temps", f"{heures}h{minutes:02d}")
    with c2:
        st.metric("Séances", len(df_week))
    
    # Barre de progression
    st.markdown(f"**Objectif:** {objectif_semaine} km")
    st.progress(progression / 100)
    st.caption(f"{progression:.0f}% atteint")
    
    st.markdown("---")
    
    # Stats annuelles
    st.markdown("##### 📆 Cette Année")
    st.metric(label="Total", value=f"{distance_annee:.1f} km")
    progression_annee = min((distance_annee / 500) * 100, 100)
    st.progress(progression_annee / 100)

# En-tête avec animation
st.markdown("""
    <div style='text-align: center; padding: 2rem 0;'>
        <h1 style='font-size: 3.5rem; margin-bottom: 0;'>
            🏃‍♂️ Sports Performance Pro
        </h1>
        <p style='font-size: 1.2rem; opacity: 0.7; margin-top: 0.5rem;'>
            Suivez, analysez et optimisez vos performances sportives
        </p>
    </div>
""", unsafe_allow_html=True)

# Layout principal avec sidebar gauche
col_left, col_right = st.columns([1, 3])

with col_left:
    st.markdown("### 🎯 Navigation")
    menu = st.selectbox(
        "Choisir une section",
        ["📊 Tableau de bord", "➕ Ajouter Performance", "📈 Analyse Avancée", 
         "🎯 Objectifs & Records", "🧮 Calculateurs", "📥 Import/Export"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Widget hebdomadaire style Nike
    create_weekly_widget()

with col_right:
    # Section 1: Tableau de bord
    if menu == "📊 Tableau de bord":
        st.markdown("## 📊 Tableau de Bord des Performances")
        
        if st.session_state.performances.empty:
            st.markdown("""
                <div style='text-align: center; padding: 3rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            border-radius: 15px; color: white;'>
                    <h2>🚀 Commencez votre parcours</h2>
                    <p style='font-size: 1.1rem;'>Aucune donnée disponible. Ajoutez votre première performance pour débuter !</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            df = st.session_state.performances.copy()
            df['date'] = pd.to_datetime(df['date'])
            
            # Filtres avec design amélioré
            st.markdown("### 🔍 Filtres")
            col1, col2, col3 = st.columns(3)
            with col1:
                sports = ['Tous'] + list(df['sport'].unique())
                sport_filtre = st.selectbox("🏅 Sport", sports)
            with col2:
                date_debut = st.date_input("📅 Date début", df['date'].min())
            with col3:
                date_fin = st.date_input("📅 Date fin", df['date'].max())
            
            # Application des filtres
            df_filtre = df.copy()
            if sport_filtre != 'Tous':
                df_filtre = df_filtre[df_filtre['sport'] == sport_filtre]
            df_filtre = df_filtre[(df_filtre['date'] >= pd.to_datetime(date_debut)) & 
                                   (df_filtre['date'] <= pd.to_datetime(date_fin))]
            
            # Métriques principales avec design amélioré
            st.markdown("### 📈 Métriques Clés")
            metriques = calculer_metriques_avancees(df_filtre)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("🎯 Entraînements", metriques['total_entrainements'])
            with col2:
                st.metric("⏱️ Durée Totale", f"{metriques['duree_totale']:.0f} min")
            with col3:
                st.metric("🏃 Distance", f"{metriques['distance_totale']:.2f} km")
            with col4:
                st.metric("🔥 Calories", f"{metriques['calories_totales']:.0f} kcal")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("⚡ Vitesse Moy", f"{metriques['vitesse_moyenne']:.2f} km/h")
            with col2:
                st.metric("💓 FC Moyenne", f"{metriques['fc_moyenne']:.0f} bpm")
            with col3:
                st.metric("⛰️ Élévation", f"{metriques['elevation_totale']:.0f} m")
            
            # Graphiques avec thème amélioré
            st.markdown("### 📊 Visualisations")
            
            tab1, tab2, tab3 = st.tabs(["📏 Distance & Durée", "💓 Fréquence Cardiaque", "📊 Répartition"])
            
            with tab1:
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=df_filtre['date'], y=df_filtre['distance_km'],
                    mode='lines+markers', name='Distance (km)',
                    line=dict(color='#667eea', width=3),
                    marker=dict(size=8, color='#764ba2')
                ))
                fig.update_layout(
                    title='Évolution de la Distance',
                    xaxis_title='Date',
                    yaxis_title='Distance (km)',
                    height=400,
                    template=None,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    hovermode='x unified'
                )
                st.plotly_chart(fig, use_container_width=True)
                
                fig2 = go.Figure()
                fig2.add_trace(go.Bar(
                    x=df_filtre['date'], y=df_filtre['duree_min'],
                    name='Durée',
                    marker=dict(
                        color=df_filtre['duree_min'],
                        colorscale='Viridis',
                        showscale=True
                    )
                ))
                fig2.update_layout(
                    title='Durée des Entraînements',
                    xaxis_title='Date',
                    yaxis_title='Durée (min)',
                    height=400,
                    template=None,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig2, use_container_width=True)
            
            with tab2:
                fig3 = go.Figure()
                fig3.add_trace(go.Scatter(
                    x=df_filtre['date'], y=df_filtre['frequence_cardiaque_moy'],
                    mode='lines+markers', name='FC Moyenne',
                    line=dict(color='#e74c3c', width=3),
                    marker=dict(size=8)
                ))
                fig3.add_trace(go.Scatter(
                    x=df_filtre['date'], y=df_filtre['frequence_cardiaque_max'],
                    mode='lines+markers', name='FC Max',
                    line=dict(color='#f39c12', width=3, dash='dash'),
                    marker=dict(size=8)
                ))
                fig3.update_layout(
                    title='Évolution de la Fréquence Cardiaque',
                    xaxis_title='Date',
                    yaxis_title='BPM',
                    height=400,
                    template=None,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    hovermode='x unified'
                )
                st.plotly_chart(fig3, use_container_width=True)
            
            with tab3:
                col1, col2 = st.columns(2)
                with col1:
                    sport_counts = df_filtre['sport'].value_counts()
                    fig4 = px.pie(
                        values=sport_counts.values,
                        names=sport_counts.index,
                        title='Répartition par Sport',
                        color_discrete_sequence=px.colors.sequential.RdBu
                    )
                    fig4.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig4, use_container_width=True)
                
                with col2:
                    type_counts = df_filtre['type_entrainement'].value_counts()
                    fig5 = px.pie(
                        values=type_counts.values,
                        names=type_counts.index,
                        title='Répartition par Type',
                        color_discrete_sequence=px.colors.sequential.Purples
                    )
                    fig5.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig5, use_container_width=True)
            
            # Tableau des dernières performances
            st.markdown("### 📋 Dernières Performances")
            df_display = df_filtre.tail(10).copy()
            df_display['date'] = df_display['date'].dt.strftime('%d/%m/%Y')
            st.dataframe(
                df_display[['date', 'sport', 'type_entrainement', 'duree_min', 'distance_km', 'vitesse_moy', 'calories']],
                use_container_width=True,
                hide_index=True
            )

    # Section 2: Ajouter une performance
    elif menu == "➕ Ajouter Performance":
        st.markdown("## ➕ Enregistrer une Nouvelle Performance")
        
        with st.form("form_performance", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 📅 Informations Générales")
                date = st.date_input("Date", datetime.now())
                sport = st.selectbox("🏅 Sport", ["Course à pied", "Cyclisme", "Natation", "Marche", "Randonnée", "Fitness", "Autre"])
                type_entrainement = st.selectbox(
                    "🎯 Type d'entraînement",
                    ["Endurance", "Interval", "Tempo", "Récupération", "Compétition", "Force"]
                )
                duree = st.number_input("⏱️ Durée (minutes)", min_value=1, value=30)
                distance = st.number_input("📏 Distance (km)", min_value=0.0, value=5.0, step=0.1)
                calories = st.number_input("🔥 Calories brûlées", min_value=0, value=300)
            
            with col2:
                st.markdown("#### 💓 Métriques Cardio")
                fc_moy = st.number_input("💓 FC Moyenne (bpm)", min_value=40, max_value=220, value=140)
                fc_max = st.number_input("💓 FC Max (bpm)", min_value=40, max_value=220, value=170)
                vitesse_moy = st.number_input("⚡ Vitesse moyenne (km/h)", min_value=0.0, value=10.0, step=0.1)
                elevation = st.number_input("⛰️ Élévation (m)", min_value=0, value=0)
                notes = st.text_area("📝 Notes", placeholder="Commentaires sur l'entraînement...")
            
            submitted = st.form_submit_button("💾 Enregistrer la Performance", use_container_width=True)
            
            if submitted:
                nouvelle_perf = {
                    'date': date,
                    'sport': sport,
                    'type_entrainement': type_entrainement,
                    'duree_min': float(duree),
                    'distance_km': float(distance),
                    'calories': float(calories),
                    'frequence_cardiaque_moy': float(fc_moy),
                    'frequence_cardiaque_max': float(fc_max),
                    'vitesse_moy': float(vitesse_moy),
                    'elevation_m': float(elevation),
                    'notes': notes
                }
                
                new_df = pd.DataFrame([nouvelle_perf])
                st.session_state.performances = pd.concat([
                    st.session_state.performances,
                    new_df
                ], ignore_index=True)
                
                # Assurer les types numériques corrects
                numeric_cols = ['duree_min', 'distance_km', 'calories', 'frequence_cardiaque_moy', 
                               'frequence_cardiaque_max', 'vitesse_moy', 'elevation_m']
                for col in numeric_cols:
                    st.session_state.performances[col] = pd.to_numeric(st.session_state.performances[col], errors='coerce')
                
                st.success("✅ Performance enregistrée avec succès!")
                st.balloons()

    # Section 3: Analyse avancée
    elif menu == "📈 Analyse Avancée":
        st.markdown("## 📈 Analyse Détaillée des Performances")
        
        if st.session_state.performances.empty:
            st.info("🔍 Aucune donnée disponible pour l'analyse.")
        else:
            df = st.session_state.performances.copy()
            df['date'] = pd.to_datetime(df['date'])
            
            # Sélection de période
            st.markdown("### ⏰ Période d'Analyse")
            periode = st.selectbox(
                "Choisir une période",
                ["7 derniers jours", "30 derniers jours", "3 derniers mois", "6 derniers mois", "Tout"]
            )
            
            if periode == "7 derniers jours":
                df_analyse = df[df['date'] >= (datetime.now() - timedelta(days=7))]
            elif periode == "30 derniers jours":
                df_analyse = df[df['date'] >= (datetime.now() - timedelta(days=30))]
            elif periode == "3 derniers mois":
                df_analyse = df[df['date'] >= (datetime.now() - timedelta(days=90))]
            elif periode == "6 derniers mois":
                df_analyse = df[df['date'] >= (datetime.now() - timedelta(days=180))]
            else:
                df_analyse = df
            
            if not df_analyse.empty:
                # Statistiques générales
                st.markdown("### 📊 Statistiques Générales")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("📅 Nombre d'entraînements", len(df_analyse))
                    st.metric("📏 Distance moyenne/séance", f"{df_analyse['distance_km'].mean():.2f} km")
                
                with col2:
                    st.metric("⏱️ Durée moyenne/séance", f"{df_analyse['duree_min'].mean():.0f} min")
                    # Calcul de la fréquence avec protection contre division par zéro
                    if len(df_analyse) > 1:
                        date_range_days = (df_analyse['date'].max() - df_analyse['date'].min()).days
                        if date_range_days > 0:
                            frequence = len(df_analyse) / (date_range_days / 7)
                        else:
                            # Si toutes les dates sont le même jour, on estime sur 1 semaine
                            frequence = len(df_analyse)
                    else:
                        frequence = 0
                    st.metric("🔄 Fréquence d'entraînement", f"{frequence:.1f} séances/semaine")
                
                with col3:
                    st.metric("⚡ Vitesse moyenne", f"{df_analyse['vitesse_moy'].mean():.2f} km/h")
                    st.metric("🔥 Calories moyennes", f"{df_analyse['calories'].mean():.0f} kcal")
                
                # Progression
                if len(df_analyse) > 1:
                    st.markdown("### 📈 Analyse de Progression")
                    df_sorted = df_analyse.sort_values('date')
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        prog_distance = ((df_sorted['distance_km'].iloc[-1] - df_sorted['distance_km'].iloc[0]) / 
                                       df_sorted['distance_km'].iloc[0] * 100) if df_sorted['distance_km'].iloc[0] > 0 else 0
                        st.metric("📏 Progression Distance", f"{prog_distance:+.1f}%", 
                                 delta=f"{prog_distance:.1f}%")
                    
                    with col2:
                        prog_vitesse = ((df_sorted['vitesse_moy'].iloc[-1] - df_sorted['vitesse_moy'].iloc[0]) / 
                                      df_sorted['vitesse_moy'].iloc[0] * 100) if df_sorted['vitesse_moy'].iloc[0] > 0 else 0
                        st.metric("⚡ Progression Vitesse", f"{prog_vitesse:+.1f}%",
                                 delta=f"{prog_vitesse:.1f}%")
                
                # Zones de fréquence cardiaque
                st.markdown("### 💓 Analyse de la Fréquence Cardiaque")
                fc_max_utilisateur = df_analyse['frequence_cardiaque_max'].max()
                fc_repos = st.slider("FC de repos (bpm)", 40, 80, 60)
                zones = calculer_zones_fc(fc_max_utilisateur, fc_repos)
                
                # Affichage des zones
                col1, col2 = st.columns([2, 1])
                with col1:
                    # Graphique des zones FC
                    fig_zones = go.Figure()
                    colors_zones = ['#48bb78', '#4299e1', '#ed8936', '#f56565', '#9f7aea']
                    for i, (zone, (min_fc, max_fc)) in enumerate(zones.items()):
                        fig_zones.add_trace(go.Bar(
                            name=zone,
                            x=[zone],
                            y=[(max_fc + min_fc) / 2],
                            error_y=dict(type='data', array=[(max_fc - min_fc) / 2]),
                            marker_color=colors_zones[i]
                        ))
                    
                    # Ligne de FC moyenne
                    fig_zones.add_trace(go.Scatter(
                        x=list(zones.keys()),
                        y=[df_analyse['frequence_cardiaque_moy'].mean()] * len(zones),
                        mode='lines+markers',
                        name='Votre FC moyenne',
                        line=dict(color='red', width=3, dash='dash'),
                        marker=dict(size=10)
                    ))
                    
                    fig_zones.update_layout(
                        title='Zones de Fréquence Cardiaque',
                        yaxis_title='BPM',
                        height=400,
                        showlegend=True,
                        template=None,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)'
                    )
                    st.plotly_chart(fig_zones, use_container_width=True)
                
                with col2:
                    st.markdown("#### 🎯 Vos Zones")
                    for zone, (min_fc, max_fc) in zones.items():
                        st.markdown(f"""
                            <div style='padding: 0.5rem; margin: 0.5rem 0; background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%); 
                                        border-radius: 10px; border-left: 4px solid #667eea;'>
                                <strong>{zone}</strong><br/>
                                {min_fc:.0f} - {max_fc:.0f} bpm
                            </div>
                        """, unsafe_allow_html=True)
                
                # Corrélations entre métriques
                st.markdown("### 🔗 Corrélations entre Métriques")
                col1, col2 = st.columns(2)
                
                # Convertir les colonnes numériques pour éviter les erreurs de type
                df_corr = df_analyse.copy()
                numeric_cols = ['distance_km', 'calories', 'duree_min', 'vitesse_moy', 'frequence_cardiaque_moy']
                for col in numeric_cols:
                    if col in df_corr.columns:
                        df_corr[col] = pd.to_numeric(df_corr[col], errors='coerce').fillna(0)
                
                # Vérifier si statsmodels est disponible pour les trendlines
                try:
                    import statsmodels
                    trendline_option = 'ols'
                except ImportError:
                    trendline_option = None
                
                with col1:
                    try:
                        fig_corr1 = px.scatter(
                            df_corr, x='distance_km', y='calories',
                            trendline=trendline_option,
                            title='Distance vs Calories',
                            labels={'distance_km': 'Distance (km)', 'calories': 'Calories (kcal)'},
                            color='sport',
                            size='duree_min'
                        )
                        fig_corr1.update_layout(height=400)
                        st.plotly_chart(fig_corr1, use_container_width=True)
                    except Exception as e:
                        # Fallback sans size si erreur
                        fig_corr1 = px.scatter(
                            df_corr, x='distance_km', y='calories',
                            title='Distance vs Calories',
                            labels={'distance_km': 'Distance (km)', 'calories': 'Calories (kcal)'},
                            color='sport'
                        )
                        fig_corr1.update_layout(height=400)
                        st.plotly_chart(fig_corr1, use_container_width=True)
                
                with col2:
                    try:
                        fig_corr2 = px.scatter(
                            df_corr, x='vitesse_moy', y='frequence_cardiaque_moy',
                            trendline=trendline_option,
                            title='Vitesse vs Fréquence Cardiaque',
                            labels={'vitesse_moy': 'Vitesse (km/h)', 'frequence_cardiaque_moy': 'FC Moyenne (bpm)'},
                            color='type_entrainement',
                            size='distance_km'
                        )
                        fig_corr2.update_layout(height=400)
                        st.plotly_chart(fig_corr2, use_container_width=True)
                    except Exception as e:
                        # Fallback sans size si erreur
                        fig_corr2 = px.scatter(
                            df_corr, x='vitesse_moy', y='frequence_cardiaque_moy',
                            title='Vitesse vs Fréquence Cardiaque',
                            labels={'vitesse_moy': 'Vitesse (km/h)', 'frequence_cardiaque_moy': 'FC Moyenne (bpm)'},
                            color='type_entrainement'
                        )
                        fig_corr2.update_layout(height=400)
                        st.plotly_chart(fig_corr2, use_container_width=True)
                
                # Analyse par sport
                st.markdown("### 🏅 Analyse par Sport")
                sport_stats = df_analyse.groupby('sport').agg({
                    'distance_km': ['sum', 'mean', 'count'],
                    'duree_min': ['sum', 'mean'],
                    'calories': ['sum', 'mean'],
                    'vitesse_moy': 'mean'
                }).round(2)
                
                sport_stats.columns = ['Distance Totale (km)', 'Distance Moy (km)', 'Nombre', 
                                      'Durée Totale (min)', 'Durée Moy (min)', 
                                      'Calories Totales', 'Calories Moy', 'Vitesse Moy (km/h)']
                
                st.dataframe(sport_stats, use_container_width=True)
                
                # Graphique d'intensité par semaine
                st.markdown("### 📅 Intensité Hebdomadaire")
                df_analyse['semaine'] = df_analyse['date'].dt.to_period('W').astype(str)
                intensite_hebdo = df_analyse.groupby('semaine').agg({
                    'distance_km': 'sum',
                    'duree_min': 'sum',
                    'calories': 'sum'
                }).reset_index()
                
                fig_hebdo = go.Figure()
                fig_hebdo.add_trace(go.Bar(
                    x=intensite_hebdo['semaine'],
                    y=intensite_hebdo['distance_km'],
                    name='Distance (km)',
                    marker_color='#667eea'
                ))
                fig_hebdo.add_trace(go.Scatter(
                    x=intensite_hebdo['semaine'],
                    y=intensite_hebdo['duree_min'],
                    name='Durée (min)',
                    yaxis='y2',
                    line=dict(color='#f56565', width=3)
                ))
                
                fig_hebdo.update_layout(
                    title='Charge d\'entraînement hebdomadaire',
                    xaxis_title='Semaine',
                    yaxis_title='Distance (km)',
                    yaxis2=dict(title='Durée (min)', overlaying='y', side='right'),
                    height=400,
                    template=None,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig_hebdo, use_container_width=True)
            else:
                st.warning("⚠️ Aucune donnée disponible pour cette période.")

    # Section 4: Objectifs & Records
    elif menu == "🎯 Objectifs & Records":
        st.markdown("## 🎯 Objectifs & Records Personnels")
        
        tab1, tab2, tab3 = st.tabs(["📊 Suivi des Objectifs", "🏆 Records Personnels", "👤 Mon Profil"])
        
        with tab1:
            st.markdown("### 📊 Définir vos Objectifs")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### 📅 Objectifs Hebdomadaires")
                new_dist_hebdo = st.number_input(
                    "🏃 Distance (km)", 
                    min_value=0.0, 
                    value=float(st.session_state.objectifs['distance_hebdo']),
                    step=5.0,
                    key="obj_dist_hebdo"
                )
                new_seances_hebdo = st.number_input(
                    "📆 Nombre de séances", 
                    min_value=0, 
                    value=int(st.session_state.objectifs['seances_hebdo']),
                    key="obj_seances"
                )
                new_duree_hebdo = st.number_input(
                    "⏱️ Durée totale (min)", 
                    min_value=0, 
                    value=int(st.session_state.objectifs['duree_hebdo']),
                    step=30,
                    key="obj_duree"
                )
            
            with col2:
                st.markdown("#### 📅 Objectifs Mensuels")
                new_dist_mensuel = st.number_input(
                    "🏃 Distance (km)", 
                    min_value=0.0, 
                    value=float(st.session_state.objectifs['distance_mensuel']),
                    step=10.0,
                    key="obj_dist_mensuel"
                )
                new_calories_hebdo = st.number_input(
                    "🔥 Calories hebdo", 
                    min_value=0, 
                    value=int(st.session_state.objectifs['calories_hebdo']),
                    step=100,
                    key="obj_calories"
                )
            
            if st.button("💾 Sauvegarder les Objectifs", type="primary"):
                st.session_state.objectifs = {
                    'distance_hebdo': new_dist_hebdo,
                    'distance_mensuel': new_dist_mensuel,
                    'seances_hebdo': new_seances_hebdo,
                    'calories_hebdo': new_calories_hebdo,
                    'duree_hebdo': new_duree_hebdo
                }
                st.success("✅ Objectifs mis à jour!")
            
            st.markdown("---")
            st.markdown("### 📈 Progression vers vos Objectifs")
            
            progression = calculer_progression_objectifs(
                st.session_state.performances, 
                st.session_state.objectifs
            )
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                pct_dist = min(100, (progression['distance_hebdo'] / st.session_state.objectifs['distance_hebdo'] * 100)) if st.session_state.objectifs['distance_hebdo'] > 0 else 0
                st.metric("🏃 Distance Hebdo", f"{progression['distance_hebdo']:.1f} / {st.session_state.objectifs['distance_hebdo']} km")
                st.progress(pct_dist / 100)
            
            with col2:
                pct_seances = min(100, (progression['seances_hebdo'] / st.session_state.objectifs['seances_hebdo'] * 100)) if st.session_state.objectifs['seances_hebdo'] > 0 else 0
                st.metric("📆 Séances Hebdo", f"{progression['seances_hebdo']} / {st.session_state.objectifs['seances_hebdo']}")
                st.progress(pct_seances / 100)
            
            with col3:
                pct_calories = min(100, (progression['calories_hebdo'] / st.session_state.objectifs['calories_hebdo'] * 100)) if st.session_state.objectifs['calories_hebdo'] > 0 else 0
                st.metric("🔥 Calories Hebdo", f"{progression['calories_hebdo']:.0f} / {st.session_state.objectifs['calories_hebdo']}")
                st.progress(pct_calories / 100)
            
            # Graphique radar des objectifs
            if not st.session_state.performances.empty:
                categories = ['Distance', 'Séances', 'Calories', 'Durée']
                objectifs_vals = [
                    st.session_state.objectifs['distance_hebdo'],
                    st.session_state.objectifs['seances_hebdo'],
                    st.session_state.objectifs['calories_hebdo'] / 100,
                    st.session_state.objectifs['duree_hebdo'] / 10
                ]
                progression_vals = [
                    progression['distance_hebdo'],
                    progression['seances_hebdo'],
                    progression['calories_hebdo'] / 100,
                    progression['duree_hebdo'] / 10
                ]
                
                fig_radar = go.Figure()
                fig_radar.add_trace(go.Scatterpolar(
                    r=objectifs_vals + [objectifs_vals[0]],
                    theta=categories + [categories[0]],
                    fill='toself',
                    name='Objectifs',
                    line_color='#667eea'
                ))
                fig_radar.add_trace(go.Scatterpolar(
                    r=progression_vals + [progression_vals[0]],
                    theta=categories + [categories[0]],
                    fill='toself',
                    name='Progression',
                    line_color='#48bb78'
                ))
                fig_radar.update_layout(
                    polar=dict(radialaxis=dict(visible=True)),
                    showlegend=True,
                    title="Radar de Progression"
                )
                st.plotly_chart(fig_radar, use_container_width=True)
        
        with tab2:
            st.markdown("### 🏆 Vos Records Personnels")
            
            if st.session_state.performances.empty:
                st.info("📊 Ajoutez des performances pour voir vos records!")
            else:
                df = st.session_state.performances.copy()
                records = obtenir_records_personnels(df)
                
                for sport, sport_records in records.items():
                    st.markdown(f"#### 🏅 {sport}")
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("📏 Plus longue distance", f"{sport_records['distance_max']:.2f} km")
                    with col2:
                        st.metric("⏱️ Plus longue durée", f"{sport_records['duree_max']:.0f} min")
                    with col3:
                        st.metric("⚡ Meilleure vitesse", f"{sport_records['vitesse_max']:.2f} km/h")
                    with col4:
                        st.metric("🔥 Plus de calories", f"{sport_records['calories_max']:.0f} kcal")
                    st.markdown("---")
        
        with tab3:
            st.markdown("### 👤 Mon Profil Sportif")
            
            col1, col2 = st.columns(2)
            with col1:
                new_age = st.number_input("🎂 Âge", min_value=10, max_value=100, value=st.session_state.profil['age'])
                new_poids = st.number_input("⚖️ Poids (kg)", min_value=30.0, max_value=200.0, value=float(st.session_state.profil['poids']), step=0.5)
                new_taille = st.number_input("📏 Taille (cm)", min_value=100, max_value=250, value=st.session_state.profil['taille'])
            
            with col2:
                new_sexe = st.selectbox("👤 Sexe", ["Homme", "Femme"], index=0 if st.session_state.profil['sexe'] == 'Homme' else 1)
                new_fc_repos = st.number_input("💓 FC au repos (bpm)", min_value=30, max_value=100, value=st.session_state.profil['fc_repos'])
                new_fc_max = st.number_input("💓 FC max (bpm)", min_value=120, max_value=220, value=st.session_state.profil['fc_max'])
            
            if st.button("💾 Sauvegarder le Profil", type="primary"):
                st.session_state.profil = {
                    'age': new_age,
                    'poids': new_poids,
                    'taille': new_taille,
                    'sexe': new_sexe,
                    'fc_repos': new_fc_repos,
                    'fc_max': new_fc_max
                }
                st.success("✅ Profil mis à jour!")
            
            st.markdown("---")
            st.markdown("### 📊 Vos Indicateurs de Santé")
            
            imc = calculer_imc(st.session_state.profil['poids'], st.session_state.profil['taille'])
            fc_max_theo = calculer_fc_max_theorique(st.session_state.profil['age'])
            vo2max = calculer_vo2max_estime(st.session_state.profil['fc_repos'], st.session_state.profil['fc_max'])
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📊 IMC", f"{imc}")
                if imc < 18.5:
                    st.caption("Insuffisance pondérale")
                elif imc < 25:
                    st.caption("✅ Poids normal")
                elif imc < 30:
                    st.caption("⚠️ Surpoids")
                else:
                    st.caption("⚠️ Obésité")
            
            with col2:
                st.metric("💓 FC Max Théorique", f"{fc_max_theo} bpm")
                st.caption("Formule de Tanaka")
            
            with col3:
                st.metric("🫁 VO2max Estimé", f"{vo2max} ml/kg/min")
                if vo2max < 30:
                    st.caption("Faible")
                elif vo2max < 40:
                    st.caption("Moyen")
                elif vo2max < 50:
                    st.caption("Bon")
                else:
                    st.caption("✅ Excellent")

    # Section 5: Calculateurs
    elif menu == "🧮 Calculateurs":
        st.markdown("## 🧮 Calculateurs Sportifs")
        
        tab1, tab2, tab3 = st.tabs(["⏱️ Allure & Temps", "🔥 Calories & Énergie", "💓 Charge d'Entraînement"])
        
        with tab1:
            st.markdown("### ⏱️ Calculateur d'Allure")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### Calculer votre allure")
                calc_distance = st.number_input("Distance parcourue (km)", min_value=0.1, value=10.0, step=0.5, key="calc_dist")
                calc_heures = st.number_input("Heures", min_value=0, value=0, key="calc_h")
                calc_minutes = st.number_input("Minutes", min_value=0, max_value=59, value=50, key="calc_min")
                calc_secondes = st.number_input("Secondes", min_value=0, max_value=59, value=0, key="calc_sec")
                
                if st.button("📊 Calculer l'allure", key="btn_pace"):
                    duree_totale = calc_heures * 60 + calc_minutes + calc_secondes / 60
                    pace_min, pace_sec = calculer_pace(calc_distance, duree_totale)
                    vitesse = calc_distance / (duree_totale / 60) if duree_totale > 0 else 0
                    
                    st.success(f"**Allure:** {pace_min}'{pace_sec:02d}\" /km")
                    st.info(f"**Vitesse:** {vitesse:.2f} km/h")
            
            with col2:
                st.markdown("#### Prédire un temps de course")
                st.caption("Basé sur la formule de Riegel")
                
                ref_distance = st.number_input("Distance de référence (km)", min_value=0.1, value=10.0, step=0.5, key="ref_dist")
                ref_temps = st.number_input("Temps de référence (min)", min_value=1.0, value=50.0, step=1.0, key="ref_temps")
                cible_distance = st.selectbox("Distance cible", [5, 10, 21.1, 42.195], format_func=lambda x: f"{x} km" if x < 21 else f"{x} km ({'Semi' if x == 21.1 else 'Marathon'})")
                
                if st.button("🎯 Prédire le temps", key="btn_predict"):
                    temps_predit = predire_temps_course(ref_distance, ref_temps, cible_distance)
                    heures = int(temps_predit // 60)
                    minutes = int(temps_predit % 60)
                    secondes = int((temps_predit % 1) * 60)
                    
                    if heures > 0:
                        st.success(f"**Temps prédit pour {cible_distance} km:** {heures}h {minutes}'{secondes:02d}\"")
                    else:
                        st.success(f"**Temps prédit pour {cible_distance} km:** {minutes}'{secondes:02d}\"")
        
        with tab2:
            st.markdown("### 🔥 Calculateur de Calories")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### Estimation des calories brûlées")
                cal_poids = st.number_input("Votre poids (kg)", min_value=30.0, value=float(st.session_state.profil['poids']), step=0.5, key="cal_poids")
                cal_activite = st.selectbox("Type d'activité", [
                    "Course à pied (10 km/h)",
                    "Course à pied (12 km/h)",
                    "Cyclisme (20 km/h)",
                    "Cyclisme (25 km/h)",
                    "Natation (loisir)",
                    "Natation (intensive)",
                    "Marche rapide",
                    "Randonnée"
                ])
                cal_duree = st.number_input("Durée (minutes)", min_value=1, value=60, key="cal_duree")
                
                # MET values pour chaque activité
                met_values = {
                    "Course à pied (10 km/h)": 10.0,
                    "Course à pied (12 km/h)": 12.5,
                    "Cyclisme (20 km/h)": 8.0,
                    "Cyclisme (25 km/h)": 10.0,
                    "Natation (loisir)": 6.0,
                    "Natation (intensive)": 10.0,
                    "Marche rapide": 5.0,
                    "Randonnée": 6.0
                }
                
                if st.button("📊 Calculer les calories", key="btn_cal"):
                    met = met_values[cal_activite]
                    calories = met * cal_poids * (cal_duree / 60)
                    st.success(f"**Calories brûlées:** {calories:.0f} kcal")
                    st.info(f"**MET utilisé:** {met} (Metabolic Equivalent of Task)")
            
            with col2:
                st.markdown("#### Zones de Fréquence Cardiaque")
                zones = calculer_zones_fc(st.session_state.profil['fc_max'], st.session_state.profil['fc_repos'])
                
                for zone_name, (fc_min, fc_max) in zones.items():
                    st.markdown(f"**{zone_name}**")
                    fc_range = st.session_state.profil['fc_max'] - st.session_state.profil['fc_repos']
                    if fc_range > 0:
                        progress_value = (fc_max - st.session_state.profil['fc_repos']) / fc_range
                        st.progress(progress_value)
                    else:
                        st.progress(0.5)  # Default progress if fc_max == fc_repos
                    st.caption(f"{fc_min:.0f} - {fc_max:.0f} bpm")
        
        with tab3:
            st.markdown("### 💓 Calculateur de Charge d'Entraînement (TRIMP)")
            st.caption("Le TRIMP (Training Impulse) mesure la charge d'entraînement basée sur la durée et l'intensité cardiaque")
            
            col1, col2 = st.columns(2)
            with col1:
                trimp_duree = st.number_input("Durée de l'entraînement (min)", min_value=1, value=60, key="trimp_duree")
                trimp_fc_moy = st.number_input("FC moyenne pendant l'effort (bpm)", min_value=60, max_value=220, value=150, key="trimp_fc")
            
            with col2:
                trimp_fc_repos = st.number_input("FC au repos (bpm)", min_value=30, max_value=100, value=st.session_state.profil['fc_repos'], key="trimp_repos")
                trimp_fc_max = st.number_input("FC maximale (bpm)", min_value=120, max_value=220, value=st.session_state.profil['fc_max'], key="trimp_max")
            
            trimp_sexe = st.radio("Sexe", ["Homme", "Femme"], horizontal=True, key="trimp_sexe")
            
            if st.button("📊 Calculer le TRIMP", type="primary", key="btn_trimp"):
                trimp = calculer_trimp(trimp_duree, trimp_fc_moy, trimp_fc_repos, trimp_fc_max, trimp_sexe)
                
                st.markdown("---")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("💓 Score TRIMP", f"{trimp}")
                with col2:
                    if trimp < 50:
                        niveau = "🟢 Léger"
                        desc = "Séance de récupération"
                    elif trimp < 100:
                        niveau = "🟡 Modéré"
                        desc = "Entraînement standard"
                    elif trimp < 150:
                        niveau = "🟠 Élevé"
                        desc = "Séance intense"
                    else:
                        niveau = "🔴 Très élevé"
                        desc = "Séance très exigeante"
                    
                    st.metric("📊 Intensité", niveau)
                    st.caption(desc)
                
                # Graphique d'intensité
                fig_trimp = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=trimp,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Score TRIMP"},
                    gauge={
                        'axis': {'range': [0, 200]},
                        'bar': {'color': "#667eea"},
                        'steps': [
                            {'range': [0, 50], 'color': "#48bb78"},
                            {'range': [50, 100], 'color': "#ecc94b"},
                            {'range': [100, 150], 'color': "#ed8936"},
                            {'range': [150, 200], 'color': "#f56565"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': trimp
                        }
                    }
                ))
                fig_trimp.update_layout(height=300)
                st.plotly_chart(fig_trimp, use_container_width=True)

    # Section 6: Import/Export
    elif menu == "📥 Import/Export":
        st.markdown("## 📥 Import & Export de Données")
        
        tab1, tab2 = st.tabs(["📤 Exporter", "📥 Importer"])
        
        with tab1:
            st.markdown("### 📤 Exporter vos Données")
            
            if st.session_state.performances.empty:
                st.info("🔍 Aucune donnée disponible pour l'export.")
            else:
                df = st.session_state.performances.copy()
                df['date'] = pd.to_datetime(df['date'])
                
                st.markdown("#### ⚙️ Configuration de l'Export")
                
                col1, col2 = st.columns(2)
                with col1:
                    date_debut = st.date_input("📅 Date de début", df['date'].min(), key="export_start")
                with col2:
                    date_fin = st.date_input("📅 Date de fin", df['date'].max(), key="export_end")
                
                sport_filtre = st.multiselect(
                    "🏅 Sports à inclure",
                    df['sport'].unique(),
                    default=list(df['sport'].unique())
                )
                
                df_export = df[(df['date'] >= pd.to_datetime(date_debut)) & 
                               (df['date'] <= pd.to_datetime(date_fin)) &
                               (df['sport'].isin(sport_filtre))]
                
                if not df_export.empty:
                    metriques = calculer_metriques_avancees(df_export)
                    
                    st.markdown("#### 👁️ Aperçu")
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("📊 Entraînements", metriques['total_entrainements'])
                    with col2:
                        st.metric("📏 Distance", f"{metriques['distance_totale']:.2f} km")
                    with col3:
                        st.metric("⏱️ Durée", f"{metriques['duree_totale']:.0f} min")
                    with col4:
                        st.metric("🔥 Calories", f"{metriques['calories_totales']:.0f} kcal")
                    
                    st.markdown("---")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        # Export PDF
                        st.markdown("#### 📄 Rapport PDF")
                        if st.button("📄 Générer le Rapport PDF", type="primary", use_container_width=True):
                            with st.spinner("⏳ Génération du rapport en cours..."):
                                graphiques_base64 = {}
                                pdf_buffer = generer_rapport_pdf(df_export, metriques, graphiques_base64)
                                
                                st.success("✅ Rapport généré avec succès!")
                                
                                st.download_button(
                                    label="📥 Télécharger le PDF",
                                    data=pdf_buffer,
                                    file_name=f"rapport_performances_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                                    mime="application/pdf",
                                    use_container_width=True
                                )
                    
                    with col2:
                        # Export CSV
                        st.markdown("#### 📊 Données CSV")
                        csv = df_export.to_csv(index=False, encoding='utf-8-sig')
                        st.download_button(
                            label="📥 Télécharger le CSV",
                            data=csv,
                            file_name=f"performances_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
                    
                    # Résumé détaillé
                    with st.expander("📑 Voir le résumé détaillé"):
                        st.markdown(f"""
                            **Période:** {date_debut.strftime('%d/%m/%Y')} - {date_fin.strftime('%d/%m/%Y')}
                            
                            **Sports inclus:** {', '.join(sport_filtre)}
                            
                            **Statistiques:**
                            - Total d'entraînements: {metriques['total_entrainements']}
                            - Distance totale: {metriques['distance_totale']:.2f} km
                            - Durée totale: {metriques['duree_totale']:.0f} minutes ({metriques['duree_totale']/60:.1f} heures)
                            - Calories brûlées: {metriques['calories_totales']:.0f} kcal
                            - Vitesse moyenne: {metriques['vitesse_moyenne']:.2f} km/h
                            - FC moyenne: {metriques['fc_moyenne']:.0f} bpm
                            - Élévation totale: {metriques['elevation_totale']:.0f} m
                        """)
                else:
                    st.warning("⚠️ Aucune donnée ne correspond aux critères sélectionnés.")
        
        with tab2:
            st.markdown("### 📥 Importer des Données")
            
            st.info("""
                **Format attendu du fichier CSV:**
                - `date` : Date (YYYY-MM-DD)
                - `sport` : Type de sport
                - `type_entrainement` : Type d'entraînement
                - `duree_min` : Durée en minutes
                - `distance_km` : Distance en km
                - `calories` : Calories brûlées
                - `frequence_cardiaque_moy` : FC moyenne
                - `frequence_cardiaque_max` : FC max
                - `vitesse_moy` : Vitesse moyenne
                - `elevation_m` : Élévation
                - `notes` : Notes (optionnel)
            """)
            
            uploaded_file = st.file_uploader("📂 Choisir un fichier CSV", type=['csv'])
            
            if uploaded_file is not None:
                try:
                    df_import = pd.read_csv(uploaded_file)
                    
                    st.markdown("#### 👁️ Aperçu des données importées")
                    st.dataframe(df_import.head(10), use_container_width=True)
                    st.caption(f"Total: {len(df_import)} enregistrements")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        mode_import = st.radio(
                            "Mode d'import",
                            ["Ajouter aux données existantes", "Remplacer les données existantes"],
                            key="import_mode"
                        )
                    
                    if st.button("✅ Confirmer l'import", type="primary"):
                        # Convertir les types
                        numeric_cols = ['duree_min', 'distance_km', 'calories', 'frequence_cardiaque_moy', 
                                       'frequence_cardiaque_max', 'vitesse_moy', 'elevation_m']
                        for col in numeric_cols:
                            if col in df_import.columns:
                                df_import[col] = pd.to_numeric(df_import[col], errors='coerce').fillna(0)
                        
                        if mode_import == "Remplacer les données existantes":
                            st.session_state.performances = df_import
                            st.success(f"✅ {len(df_import)} enregistrements importés (données remplacées)!")
                        else:
                            st.session_state.performances = pd.concat([
                                st.session_state.performances,
                                df_import
                            ], ignore_index=True)
                            st.success(f"✅ {len(df_import)} enregistrements ajoutés!")
                        
                        st.balloons()
                        
                except Exception as e:
                    st.error(f"❌ Erreur lors de l'import: {str(e)}")
            
            st.markdown("---")
            st.markdown("#### 📋 Télécharger un modèle CSV")
            
            template_df = pd.DataFrame({
                'date': ['2024-01-15', '2024-01-17'],
                'sport': ['Course à pied', 'Cyclisme'],
                'type_entrainement': ['Endurance', 'Interval'],
                'duree_min': [45, 60],
                'distance_km': [8.5, 25.0],
                'calories': [450, 600],
                'frequence_cardiaque_moy': [145, 135],
                'frequence_cardiaque_max': [175, 165],
                'vitesse_moy': [11.3, 25.0],
                'elevation_m': [120, 350],
                'notes': ['Bonne séance', 'Sortie vallonnée']
            })
            
            csv_template = template_df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="📥 Télécharger le modèle CSV",
                data=csv_template,
                file_name="modele_import_performances.csv",
                mime="text/csv"
            )