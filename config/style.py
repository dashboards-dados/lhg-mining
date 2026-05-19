import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        /* Importação de Fontes Premium */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Reset & Base Tipografia */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            color: #1E293B; /* Slate 800 - Alta legibilidade */
            background-color: #F8FAFC; /* Slate 50 - Fundo ultra-light */
        }
        
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Outfit', sans-serif !important;
            font-weight: 700 !important;
            color: #0F172A !important; /* Slate 900 */
            letter-spacing: -0.025em;
        }
        
        /* Sidebar - Suave e Limpa */
        [data-testid="stSidebar"] {
            background-color: #FFFFFF !important;
            border-right: 1px solid #F1F5F9; /* Slate 100 */
            box-shadow: 4px 0 24px rgba(0, 0, 0, 0.02);
        }
        
        /* Esconder elementos padrão */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header { visibility: hidden; }
        .stDeployButton { display: none !important; }
        
        /* Customização das Abas (Tabs) - Modern Pills com Sombra Suave */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background: transparent;
            padding: 4px;
            border: none;
            margin-bottom: 24px;
        }
        .stTabs [data-baseweb="tab"] {
            height: 40px;
            background-color: transparent;
            padding: 0 20px;
            font-family: 'Inter', sans-serif;
            font-weight: 500;
            font-size: 0.9rem;
            color: #64748B; /* Slate 500 */
            border-radius: 8px;
            transition: all 0.2s ease-in-out;
            border: 1px solid transparent !important;
        }
        .stTabs [aria-selected="true"] {
            background-color: #FFFFFF !important;
            color: #FF6600 !important;
            border: 1px solid #F1F5F9 !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05), 0 1px 2px rgba(0,0,0,0.03) !important; /* Tailwind shadow-sm */
            font-weight: 600;
        }
        .stTabs [data-baseweb="tab"]:hover:not([aria-selected="true"]) {
            color: #334155;
            background-color: #F1F5F9;
        }
        
        /* Container para KPIs - Grid Fluido e Layered Shadows */
        .kpi-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 24px; /* Escala de 8px (3x8) */
            margin-bottom: 32px;
        }
        
        .kpi-card {
            background: #FFFFFF;
            padding: 24px;
            border-radius: 12px;
            border: 1px solid #F1F5F9; /* Slate 100 */
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03), 0 2px 4px -1px rgba(0, 0, 0, 0.02); /* Tailwind shadow-md super suave */
            transition: all 0.2s ease-in-out;
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }
        
        .kpi-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.04), 0 4px 6px -2px rgba(0, 0, 0, 0.02); /* Tailwind shadow-lg sutil */
        }
        
        .kpi-title {
            font-family: 'Inter', sans-serif;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-weight: 600;
            color: #64748B; /* Slate 500 */
            margin-bottom: 12px;
        }
        
        .kpi-value {
            font-family: 'Outfit', sans-serif;
            font-size: 2.25rem; /* 36px */
            font-weight: 700;
            color: #0F172A; /* Slate 900 */
            line-height: 1.2;
            margin-bottom: 8px;
        }
        
        .kpi-delta {
            font-family: 'Inter', sans-serif;
            font-size: 0.8rem;
            font-weight: 500;
            display: inline-flex;
            align-items: center;
            gap: 4px;
            padding: 4px 10px;
            border-radius: 6px;
            align-self: flex-start;
        }
        .delta-up { background-color: #F0FDF4; color: #16A34A; border: 1px solid #DCFCE7; } /* Green 50/600/100 */
        .delta-down { background-color: #FEF2F2; color: #DC2626; border: 1px solid #FEE2E2; } /* Red 50/600/100 */
        .delta-neutral { background-color: #F8FAFC; color: #64748B; border: 1px solid #F1F5F9; } /* Slate 50/500/100 */
        
        /* Feed de Notícias - Fluid Grid */
        .news-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 24px;
            margin-top: 24px;
        }
        
        .news-card-premium {
            background: #FFFFFF;
            border-radius: 8px; /* Cantos suavemente arredondados */
            padding: 24px 24px 20px 32px; /* Maior espaçamento interno na esquerda */
            display: flex;
            flex-direction: column;
            border: 1px solid #E2E8F0;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04); /* Sombra ultra-leve e difusa */
            transition: all 0.2s ease-in-out;
            position: relative;
            overflow: hidden;
        }
        
        .news-card-premium:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.06);
        }
        
        /* Barra lateral de sentimento arredondada acompanhando a curvatura do card */
        .news-card-sentiment-bar {
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 5px;
            border-top-left-radius: 8px;
            border-bottom-left-radius: 8px;
        }
        .news-card-sentiment-bar.pos { background-color: #00A86B; }
        .news-card-sentiment-bar.neg { background-color: #E04F5F; }
        .news-card-sentiment-bar.neu { background-color: #8E9BB0; }
        
        .news-header-badge {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.7rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            text-align: center;
            margin-bottom: 12px;
        }
        .badge-pos { background-color: #E6F4EA; color: #137333; border: 1px solid #CEEAD6; }
        .badge-neg { background-color: #FCE8E6; color: #C5221F; border: 1px solid #FAD2CF; }
        .badge-neu { background-color: #F1F3F4; color: #5F6368; border: 1px solid #E8EAED; }
        
        .news-card-title {
            font-family: 'Inter', sans-serif;
            font-size: 1.05rem;
            font-weight: 500; /* Peso médio (Medium) */
            color: #2D3748; /* Grafite fosco escuro */
            line-height: 1.45;
            margin-bottom: 16px;
        }
        
        .news-card-footer {
            margin-top: auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-top: 14px;
            border-top: 1px dashed #E2E8F0;
        }
        .news-date { font-family: 'Inter', sans-serif; font-size: 0.78rem; color: #718096; font-weight: 400; }
        .news-portal {
            font-family: 'Inter', sans-serif;
            font-size: 0.75rem;
            color: #4A5568;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em; /* Espaçamento editorial moderno */
            margin-bottom: 2px;
        }
        
        .news-action {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 6px 14px;
            background-color: #EDF2F7; /* Cinza bem claro discreto */
            color: #4A5568; /* Texto em cinza escuro */
            border-radius: 4px; /* Cantos arredondados */
            text-decoration: none;
            font-weight: 600;
            font-size: 0.75rem;
            transition: all 0.15s ease-in-out;
            cursor: pointer;
            border: none !important;
            margin-top: 14px;
        }
        .news-action:hover {
            background-color: #E2E8F0;
            color: #1A202C;
        }
        
        /* Estilo para Gráficos - Container Premium sem bordas fortes */
        [data-testid="stPlotlyChart"] {
            background: #FFFFFF !important;
            border-radius: 12px !important;
            padding: 16px !important;
            border: 1px solid #F1F5F9 !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03), 0 2px 4px -1px rgba(0, 0, 0, 0.02) !important;
            transition: all 0.2s ease-in-out !important;
            overflow: hidden !important;
        }
        [data-testid="stPlotlyChart"] iframe {
            overflow: hidden !important;
        }
        [data-testid="stPlotlyChart"]:hover {
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.04), 0 4px 6px -2px rgba(0, 0, 0, 0.02) !important;
            transform: translateY(-2px);
        }
        
        /* Global scrollbar styling to avoid ugly default scrollbars */
        ::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        ::-webkit-scrollbar-thumb {
            background: #CBD5E1;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-track {
            background: transparent;
        }
        
        /* Custom Tooltip Styling via CSS injection if Plotly allows or at least preparing the class */
        .hoverlayer .hovertext {
            border-radius: 8px !important;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05) !important;
            backdrop-filter: blur(4px) !important;
        }

        /* Botão de Download - Elegante e Moderno */
        [data-testid="stDownloadButton"] > button {
            background-color: #FFFFFF !important;
            color: #0F172A !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 8px !important;
            font-family: 'Inter', sans-serif !important;
            font-weight: 600 !important;
            font-size: 0.9rem !important;
            padding: 10px 20px !important;
            transition: all 0.2s ease-in-out !important;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05) !important;
        }
        [data-testid="stDownloadButton"] > button:hover {
            background-color: #F8FAFC !important;
            border-color: #CBD5E1 !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
            transform: translateY(-1px);
        }
        
        /* Ajustes Gerais */
        .stMarkdown p { color: #475569; }
        .stExpander { border: 1px solid #F1F5F9 !important; background: #FFFFFF !important; border-radius: 8px !important; box-shadow: 0 1px 3px rgba(0,0,0,0.03) !important;}
        
        /* Esqueleto de Loading (Skeleton Screens Setup via CSS Animation) */
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: .5; }
        }
        .skeleton {
            animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
            background-color: #E2E8F0;
            border-radius: 6px;
        }
        </style>
    """, unsafe_allow_html=True)
