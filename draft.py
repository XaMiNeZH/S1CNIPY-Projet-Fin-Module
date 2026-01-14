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

# CSS personnalisé pour un design moderne et attrayant
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    /* Arrière-plan général avec gradient */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Conteneur principal avec glassmorphism */
    .block-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    
    /* Sidebar avec style moderne */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2d3748 0%, #1a202c 100%);
    }
    
    [data-testid="stSidebar"] .css-1d391kg {
        color: white;
    }
    
    /* Titres avec gradient */
    h1 {
        background: linear-gradient(120deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 3rem;
        margin-bottom: 1.5rem;
        text-align: center;
        animation: fadeInDown 0.8s ease-in-out;
    }
    
    h2 {
        color: #2d3748;
        font-weight: 600;
        font-size: 1.8rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 3px solid #667eea;
        padding-bottom: 0.5rem;
        animation: fadeInLeft 0.8s ease-in-out;
    }
    
    h3 {
        color: #4a5568;
        font-weight: 600;
        font-size: 1.3rem;
    }
    
    /* Cartes de métriques améliorées */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(120deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.9rem;
        font-weight: 600;
        color: #4a5568;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #ffffff 0%, #f7fafc 100%);
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #667eea;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        animation: fadeInUp 0.6s ease-in-out;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(102, 126, 234, 0.3);
    }
    
    /* Boutons stylisés */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
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
        border: 2px solid #e2e8f0;
        padding: 0.75rem;
        transition: all 0.3s ease;
        font-size: 1rem;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Tabs personnalisés */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        border: 2px solid transparent;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-color: #667eea;
    }
    
    /* DataFrames stylisés */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Messages info/success/warning */
    .stAlert {
        border-radius: 12px;
        border-left: 5px solid;
        animation: slideInRight 0.5s ease-in-out;
    }
    
    /* Animations */
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInLeft {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(100px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Sidebar personnalisé */
    [data-testid="stSidebar"] .stSelectbox label {
        color: white;
        font-weight: 600;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #e2e8f0;
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
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Date inputs */
    .stDateInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e2e8f0;
    }
    
    /* Expander personnalisé */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
        border-radius: 10px;
        font-weight: 600;
    }
    
    /* Widget personnalisé - Style Nike */
    .weekly-widget {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
    }
    
    .weekly-header {
        text-align: center;
        margin-bottom: 1.5rem;
    }
    
    .weekly-title {
        font-size: 0.85rem;
        font-weight: 600;
        color: #718096;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }
    
    .weekly-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2d3748;
        margin: 0;
    }
    
    .weekly-days {
        display: flex;
        justify-content: space-around;
        margin: 1.5rem 0;
        padding: 0.5rem 0;
    }
    
    .day-item {
        text-align: center;
        position: relative;
    }
    
    .day-label {
        font-size: 0.75rem;
        font-weight: 600;
        color: #a0aec0;
        margin-bottom: 0.5rem;
    }
    
    .day-indicator {
        width: 8px;
        height: 8px;
        background: #e2e8f0;
        border-radius: 50%;
        margin: 0 auto;
    }
    
    .day-indicator.active {
        background: #667eea;
        box-shadow: 0 0 10px rgba(102, 126, 234, 0.5);
    }
    
    .weekly-stats {
        display: flex;
        justify-content: space-around;
        margin-top: 1.5rem;
        padding-top: 1.5rem;
        border-top: 1px solid #e2e8f0;
    }
    
    .stat-item {
        text-align: center;
    }
    
    .stat-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #2d3748;
    }
    
    .stat-label {
        font-size: 0.75rem;
        color: #718096;
        margin-top: 0.25rem;
    }
    
    .progress-bar-container {
        background: #e2e8f0;
        height: 8px;
        border-radius: 10px;
        overflow: hidden;
        margin: 1rem 0;
    }
    
    .progress-bar {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        height: 100%;
        border-radius: 10px;
        transition: width 0.5s ease;
    }
    
    .year-section {
        margin-top: 2rem;
        padding-top: 1.5rem;
        border-top: 2px solid #e2e8f0;
    }
    
    .section-title {
        font-size: 0.85rem;
        font-weight: 600;
        color: #718096;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 1rem;
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
    """Widget style Nike pour les statistiques hebdomadaires"""
    df = st.session_state.performances.copy()
    
    if df.empty:
        st.markdown("""
            <div class="weekly-widget">
                <div style="text-align: center; padding: 2rem;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">🏃</div>
                    <div style="color: #718096; font-size: 0.9rem;">
                        Ajoutez votre première performance !
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        return
    
    try:
        df['date'] = pd.to_datetime(df['date'])
        today = datetime.now()
        start_of_week = today - timedelta(days=today.weekday())
        
        df_week = df[df['date'] >= start_of_week]
        distance_semaine = float(df_week['distance_km'].sum())
        duree_semaine = float(df_week['duree_min'].sum())
        
        start_of_year = datetime(today.year, 1, 1)
        df_year = df[df['date'] >= start_of_year]
        distance_annee = float(df_year['distance_km'].sum())
        
        jours = ['L', 'M', 'M', 'J', 'V', 'S', 'D']
        jours_actifs = set(df_week['date'].dt.dayofweek.tolist())
        
        objectif_semaine = 50
        progression = min((distance_semaine / objectif_semaine) * 100, 100) if objectif_semaine > 0 else 0
        
        heures = int(duree_semaine // 60)
        minutes = int(duree_semaine % 60)
        nb_seances = len(df_week)
        
        progress_annee = min((distance_annee / 500) * 100, 100)
        
        # Construction HTML propre
        html_parts = []
        html_parts.append('<div class="weekly-widget">')
        
        # Icônes
        html_parts.append('<div style="display: flex; justify-content: center; gap: 2rem; margin-bottom: 1.5rem;">')
        html_parts.append('<span style="font-size: 2rem;">🏃</span>')
        html_parts.append('<span style="font-size: 2rem;">🚴</span>')
        html_parts.append('<span style="font-size: 2rem;">🏊</span>')
        html_parts.append('</div>')
        
        # Message
        html_parts.append('<div style="background: #f7fafc; padding: 1rem; border-radius: 10px; margin-bottom: 1.5rem; text-align: center;">')
        html_parts.append('<p style="margin: 0; color: #4a5568; font-size: 0.9rem; line-height: 1.5;">')
        html_parts.append('<strong>Continuez comme ça ! 💪</strong><br/>')
        html_parts.append('Vous progressez bien !')
        html_parts.append('</p></div>')
        
        # Cette semaine
        html_parts.append('<div class="weekly-header">')
        html_parts.append('<div class="weekly-title">CETTE SEMAINE</div>')
        html_parts.append(f'<div class="weekly-value">{distance_semaine:.1f} km</div>')
        html_parts.append('</div>')
        
        # Jours
        html_parts.append('<div class="weekly-days">')
        for i, jour in enumerate(jours):
            active = "active" if i in jours_actifs else ""
            html_parts.append('<div class="day-item">')
            html_parts.append(f'<div class="day-label">{jour}</div>')
            html_parts.append(f'<div class="day-indicator {active}"></div>')
            html_parts.append('</div>')
        html_parts.append('</div>')
        
        # Stats
        html_parts.append('<div class="weekly-stats">')
        html_parts.append('<div class="stat-item">')
        html_parts.append(f'<div class="stat-value">{heures}h{minutes:02d}</div>')
        html_parts.append('<div class="stat-label">Temps</div>')
        html_parts.append('</div>')
        html_parts.append('<div class="stat-item">')
        html_parts.append(f'<div class="stat-value">{nb_seances}</div>')
        html_parts.append('<div class="stat-label">Séances</div>')
        html_parts.append('</div>')
        html_parts.append('</div>')
        
        # Progress bar
        html_parts.append('<div style="margin-top: 1.5rem;">')
        html_parts.append('<div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">')
        html_parts.append(f'<span style="font-size: 0.75rem; color: #718096;">Objectif: {objectif_semaine} km</span>')
        html_parts.append(f'<span style="font-size: 0.75rem; color: #667eea; font-weight: 600;">{progression:.0f}%</span>')
        html_parts.append('</div>')
        html_parts.append('<div class="progress-bar-container">')
        html_parts.append(f'<div class="progress-bar" style="width: {progression}%;"></div>')
        html_parts.append('</div>')
        html_parts.append('</div>')
        
        # Cette année
        html_parts.append('<div class="year-section">')
        html_parts.append('<div class="section-title">CETTE ANNÉE</div>')
        html_parts.append('<div style="display: flex; align-items: center; gap: 1rem;">')
        html_parts.append('<div style="flex: 1;">')
        html_parts.append('<div class="progress-bar-container" style="height: 4px;">')
        html_parts.append(f'<div class="progress-bar" style="width: {progress_annee}%;"></div>')
        html_parts.append('</div>')
        html_parts.append('</div>')
        html_parts.append('<div style="text-align: right;">')
        html_parts.append(f'<div style="font-size: 1.2rem; font-weight: 700; color: #2d3748;">{distance_annee:.1f} km</div>')
        html_parts.append('<div style="font-size: 0.7rem; color: #718096;">TOTAL</div>')
        html_parts.append('</div>')
        html_parts.append('</div>')
        html_parts.append('</div>')
        
        # Bouton
        html_parts.append('<div style="margin-top: 1.5rem; text-align: center;">')
        html_parts.append('<div style="color: #667eea; font-weight: 600; font-size: 0.9rem; cursor: pointer;">')
        html_parts.append('Gérer vos objectifs →')
        html_parts.append('</div>')
        html_parts.append('</div>')
        
        html_parts.append('</div>')
        
        st.markdown(''.join(html_parts), unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Erreur dans le widget: {str(e)}")

# En-tête avec animation
st.markdown("""
    <div style='text-align: center; padding: 2rem 0;'>
        <h1 style='font-size: 3.5rem; margin-bottom: 0;'>
            🏃‍♂️ Sports Performance Pro
        </h1>
        <p style='font-size: 1.2rem; color: #718096; margin-top: 0.5rem;'>
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
        ["📊 Tableau de bord", "➕ Ajouter Performance", "📈 Analyse Avancée", "📄 Rapports & Export"],
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
                    template='plotly_white',
                    hovermode='x unified',
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
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
                    template='plotly_white',
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
                    template='plotly_white',
                    hovermode='x unified',
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
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
                    'duree_min': duree,
                    'distance_km': distance,
                    'calories': calories,
                    'frequence_cardiaque_moy': fc_moy,
                    'frequence_cardiaque_max': fc_max,
                    'vitesse_moy': vitesse_moy,
                    'elevation_m': elevation,
                    'notes': notes
                }
                
                st.session_state.performances = pd.concat([
                    st.session_state.performances,
                    pd.DataFrame([nouvelle_perf])
                ], ignore_index=True)
                
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
                    frequence = len(df_analyse) / ((df_analyse['date'].max() - df_analyse['date'].min()).days / 7) if len(df_analyse) > 1 else 0
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
                        template='plotly_white'
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
                
                with col1:
                    fig_corr1 = px.scatter(
                        df_analyse, x='distance_km', y='calories',
                        trendline='ols',
                        title='Distance vs Calories',
                        labels={'distance_km': 'Distance (km)', 'calories': 'Calories (kcal)'},
                        color='sport',
                        size='duree_min'
                    )
                    fig_corr1.update_layout(height=400)
                    st.plotly_chart(fig_corr1, use_container_width=True)
                
                with col2:
                    fig_corr2 = px.scatter(
                        df_analyse, x='vitesse_moy', y='frequence_cardiaque_moy',
                        trendline='ols',
                        title='Vitesse vs Fréquence Cardiaque',
                        labels={'vitesse_moy': 'Vitesse (km/h)', 'frequence_cardiaque_moy': 'FC Moyenne (bpm)'},
                        color='type_entrainement',
                        size='distance_km'
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
                    template='plotly_white'
                )
                st.plotly_chart(fig_hebdo, use_container_width=True)
            else:
                st.warning("⚠️ Aucune donnée disponible pour cette période.")

    # Section 4: Rapports & Export
    elif menu == "📄 Rapports & Export":
        st.markdown("## 📄 Générer et Exporter des Rapports")
        
        if st.session_state.performances.empty:
            st.info("🔍 Aucune donnée disponible pour générer un rapport.")
        else:
            df = st.session_state.performances.copy()
            df['date'] = pd.to_datetime(df['date'])
            
            st.markdown("### ⚙️ Configuration du Rapport")
            
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
            
            # Aperçu des données
            st.markdown("### 👁️ Aperçu des Données")
            df_rapport = df[(df['date'] >= pd.to_datetime(date_debut)) & 
                           (df['date'] <= pd.to_datetime(date_fin)) &
                           (df['sport'].isin(sport_filtre))]
            
            if not df_rapport.empty:
                metriques = calculer_metriques_avancees(df_rapport)
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("📊 Entraînements", metriques['total_entrainements'])
                with col2:
                    st.metric("📏 Distance", f"{metriques['distance_totale']:.2f} km")
                with col3:
                    st.metric("⏱️ Durée", f"{metriques['duree_totale']:.0f} min")
                with col4:
                    st.metric("🔥 Calories", f"{metriques['calories_totales']:.0f} kcal")
                
                # Export PDF
                st.markdown("### 📥 Export PDF")
                if st.button("📄 Générer le Rapport PDF", type="primary", use_container_width=True):
                    with st.spinner("⏳ Génération du rapport en cours..."):
                        graphiques_base64 = {}
                        pdf_buffer = generer_rapport_pdf(df_rapport, metriques, graphiques_base64)
                        
                        st.success("✅ Rapport généré avec succès!")
                        
                        st.download_button(
                            label="📥 Télécharger le Rapport PDF",
                            data=pdf_buffer,
                            file_name=f"rapport_performances_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                
                # Export CSV
                st.markdown("### 📊 Export CSV")
                csv = df_rapport.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="📥 Télécharger les Données CSV",
                    data=csv,
                    file_name=f"performances_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                
                # Résumé du rapport
                st.markdown("### 📑 Résumé du Rapport")
                with st.expander("Voir le résumé détaillé"):
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