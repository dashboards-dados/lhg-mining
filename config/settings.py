# config/settings.py
import os

# Base path of 'producao/' folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Paths & IDs (without JSON_CREDENTIALS for production secrets workflow)
PATH_KPI = os.path.join(BASE_DIR, 'dados-exemplo', 'Cópia de LHG MINING _ Monitoramento - Dados.xlsx')
GOOGLE_SHEET_ID = '1SOOtsF-YnNyohJaAqUaMT53kjjIBBjP-LzkyqKiWUb4'
GOOGLE_SHEET_ID_SAUDE = '10EjGlvgJCRWfhZRRsKjF5W6DdDzn7cYdxhrCoo8pGBo'

# Colors & Theming
COLOR_MAP = {'Positivo': '#00A86B', 'Negativo': '#E04F5F', 'Neutro': '#8E9BB0'} 
CHART_COLORS = ['#FF6600', '#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6']
PLOTLY_TEMPLATE = 'plotly_white'

plotly_layout_defaults = dict(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#475569", size=13),
    title_font=dict(family="Outfit, sans-serif", size=18, color="#0F172A", weight="bold"),
    height=450,
    xaxis=dict(
        showgrid=False, 
        zeroline=False, 
        linecolor="#E2E8F0", 
        tickfont=dict(color="#64748B", size=12, family="Inter"),
        title_font=dict(color="#64748B", size=13, family="Inter", weight="bold")
    ),
    yaxis=dict(
        showgrid=True, 
        gridcolor="#EDF2F7", # Soft grid
        gridwidth=1,
        griddash="dot", # Dotted pattern for grid
        zeroline=False, 
        linecolor="rgba(0,0,0,0)", 
        tickfont=dict(color="#64748B", size=12, family="Inter"),
        title_font=dict(color="#64748B", size=13, family="Inter", weight="bold")
    ),
    margin=dict(l=20, r=20, t=80, b=60),
    legend=dict(
        bgcolor="rgba(255,255,255,0.7)", 
        bordercolor="#E2E8F0", 
        borderwidth=1, 
        font=dict(size=13, color="#334155", family="Inter", weight=500),
        orientation="h",
        yanchor="bottom",
        y=-0.25,
        xanchor="center",
        x=0.5
    ),
    hoverlabel=dict(
        bgcolor="rgba(255, 255, 255, 0.9)",
        font_size=14,
        font_family="Inter",
        bordercolor="#CBD5E1",
        align="left"
    ),
    hovermode="closest"
)
