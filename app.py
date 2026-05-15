import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import html
import io
import base64
try:
    from fpdf import FPDF
    HAS_FPDF = True
except ImportError:
    HAS_FPDF = False

try:
    import gspread
    HAS_GSPREAD = True
except ImportError:
    HAS_GSPREAD = False

# --- Configuração da Página ---
st.set_page_config(
    page_title="LHG Mining",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Estética Moderna Premium (Gradients, Glassmorphism, Shadows) ---
st.markdown("""
    <style>
    /* Importação de Fontes Premium */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #1A1A1A;
        background-color: #F8F9FE;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 800 !important;
        color: #1A1A1A !important;
        letter-spacing: -0.5px;
    }
    
    /* Sidebar - Sleek Light */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FFFFFF 0%, #F4F6F9 100%) !important;
        border-right: none;
        box-shadow: 2px 0 20px rgba(0,0,0,0.03);
    }
    
    /* Esconder elementos padrão */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header { visibility: hidden; }
    .stDeployButton { display: none !important; }
    
    /* Customização das Abas (Tabs) - Modern Pills */
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
        background: #FFFFFF;
        padding: 8px;
        border-radius: 14px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.04);
        border: none;
        margin-bottom: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        background-color: transparent;
        padding: 0 25px;
        font-family: 'Outfit', sans-serif;
        font-weight: 600;
        font-size: 0.95rem;
        color: #6C757D;
        border-radius: 10px;
        transition: all 0.3s ease;
        border: none !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #FF6600, #FF8C33) !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 15px rgba(255, 102, 0, 0.3);
    }
    
    /* Container para KPIs - Glassmorphism & Hover FX */
    .kpi-container {
        display: flex;
        gap: 20px;
        margin-bottom: 30px;
        flex-wrap: wrap;
    }
    .kpi-card {
        flex: 1;
        min-width: 220px;
        background: #FFFFFF;
        padding: 25px;
        border-radius: 20px;
        position: relative;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 10px 30px rgba(0,0,0,0.04);
        border: 1px solid rgba(0, 0, 0, 0.02);
        overflow: hidden;
        z-index: 1;
    }
    .kpi-card::after {
        content: '';
        position: absolute;
        top: 0; right: 0;
        width: 150px; height: 150px;
        background: radial-gradient(circle, rgba(255,102,0,0.05) 0%, rgba(255,255,255,0) 70%);
        z-index: -1;
        border-radius: 50%;
        transform: translate(30%, -30%);
        transition: all 0.4s ease;
    }
    .kpi-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 15px 35px rgba(255, 102, 0, 0.1);
        border-color: rgba(255, 102, 0, 0.1);
    }
    .kpi-card:hover::after {
        background: radial-gradient(circle, rgba(255,102,0,0.1) 0%, rgba(255,255,255,0) 70%);
        transform: translate(20%, -20%) scale(1.2);
    }
    
    .kpi-title {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 700;
        color: #888888;
        margin-bottom: 10px;
    }
    .kpi-value {
        font-family: 'Outfit', sans-serif;
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #1A1A1A, #4A4A4A);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.1;
        margin-bottom: 10px;
    }
    .kpi-delta {
        font-size: 0.85rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 6px;
        padding: 6px 12px;
        border-radius: 20px;
        display: inline-flex;
    }
    .delta-up { background: rgba(40, 167, 69, 0.1); color: #28A745; }
    .delta-down { background: rgba(220, 53, 69, 0.1); color: #DC3545; }
    .delta-neutral { background: rgba(136, 136, 136, 0.1); color: #888888; }
    
    /* Feed de Notícias - Modern Cards */
    .news-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
        gap: 25px;
        margin-top: 20px;
    }
    .news-card-premium {
        background: #FFFFFF;
        border-radius: 20px;
        padding: 25px;
        display: flex;
        flex-direction: column;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 10px 30px rgba(0,0,0,0.03);
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(0,0,0,0.02);
    }
    .news-card-premium::before {
        content: '';
        position: absolute;
        top: 0; left: 0; width: 100%; height: 4px;
        transition: all 0.3s ease;
    }
    .news-card-premium.pos::before { background: linear-gradient(90deg, #52BE80, #2ECC71); }
    .news-card-premium.neg::before { background: linear-gradient(90deg, #E74C3C, #FF7675); }
    .news-card-premium.neu::before { background: linear-gradient(90deg, #95A5A6, #BDC3C7); }
    
    .news-card-premium:hover {
        box-shadow: 0 20px 40px rgba(0,0,0,0.08);
        transform: translateY(-6px);
    }
    .news-header-badge {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 15px;
    }
    .badge-pos { background: rgba(82, 190, 128, 0.1); color: #52BE80; }
    .badge-neg { background: rgba(231, 76, 60, 0.1); color: #E74C3C; }
    .badge-neu { background: rgba(149, 165, 166, 0.1); color: #7F8C8D; }
    
    .news-card-title {
        font-family: 'Outfit', sans-serif;
        font-size: 1.15rem;
        font-weight: 700;
        color: #1A1A1A;
        line-height: 1.4;
        margin-bottom: 25px;
    }
    
    .news-card-footer {
        margin-top: auto;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-top: 1px solid #F1F3F5;
        padding-top: 15px;
    }
    .news-date { font-size: 0.85rem; color: #888888; font-weight: 500; }
    .news-portal { font-size: 0.9rem; color: #4A4A4A; font-weight: 700; text-transform: uppercase; }
    
    .news-action {
        display: inline-block;
        padding: 8px 16px;
        background: rgba(243, 112, 33, 0.1);
        color: #FF6600;
        border-radius: 8px;
        text-decoration: none;
        font-weight: 700;
        font-size: 0.85rem;
        transition: all 0.3s ease;
    }
    .news-action:hover {
        background: #FF6600;
        color: #FFFFFF;
        box-shadow: 0 4px 10px rgba(255, 102, 0, 0.3);
    }
    
    /* Estilo para Gráficos - Container Premium */
    [data-testid="stPlotlyChart"] {
        background: #FFFFFF !important;
        border-radius: 24px !important;
        padding: 20px !important;
        border: 1px solid rgba(0,0,0,0.02) !important;
        box-shadow: 0 10px 40px rgba(0,0,0,0.04) !important;
        transition: transform 0.4s ease, box-shadow 0.4s ease !important;
        overflow: hidden !important;
    }
    [data-testid="stPlotlyChart"]:hover {
        box-shadow: 0 15px 50px rgba(0,0,0,0.08) !important;
        transform: translateY(-4px);
    }
    
    /* Botão de Download - Laranja Vibrante Premium */
    [data-testid="stDownloadButton"] > button {
        background: linear-gradient(135deg, #FF6600, #FF8C33) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 12px !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        padding: 14px 28px !important;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        box-shadow: 0 8px 20px rgba(255, 102, 0, 0.3) !important;
    }
    [data-testid="stDownloadButton"] > button:hover {
        box-shadow: 0 12px 25px rgba(255, 102, 0, 0.5) !important;
        transform: scale(1.03) translateY(-2px);
        color: #FFFFFF !important;
    }
    
    /* Ajustes Gerais */
    .stMarkdown p { color: #4A4A4A; }
    .stExpander { border: 1px solid #E9ECEF !important; background: #FFFFFF !important; border-radius: 12px !important; }
    </style>
""", unsafe_allow_html=True)


# Paleta Premium LHG Mining
COLOR_MAP = {'Positivo': '#52BE80', 'Negativo': '#E74C3C', 'Neutro': '#95A5A6'}
CHART_COLORS = ['#FF6600', '#3498DB', '#2ECC71', '#F1C40F', '#E74C3C', '#9B59B6']
PLOTLY_TEMPLATE = 'plotly_white'

plotly_layout_defaults = dict(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Outfit, Inter, sans-serif", color="#4A4A4A", size=12),
    title_font=dict(family="Outfit, sans-serif", size=18, color="#1A1A1A", weight="bold"),
    height=450,
    xaxis=dict(
        showgrid=False, 
        zeroline=False, 
        linecolor="#F1F3F5", 
        tickfont=dict(color="#888888", size=11, family="Inter"),
        title_font=dict(color="#888888", size=12, family="Inter")
    ),
    yaxis=dict(
        showgrid=True, 
        gridcolor="#F8F9FA", 
        gridwidth=1,
        zeroline=False, 
        linecolor="rgba(0,0,0,0)", 
        tickfont=dict(color="#888888", size=11, family="Inter"),
        title_font=dict(color="#888888", size=12, family="Inter")
    ),
    margin=dict(l=20, r=20, t=80, b=60),
    legend=dict(
        bgcolor="rgba(255,255,255,0.8)", 
        bordercolor="#F1F3F5", 
        borderwidth=1, 
        font=dict(size=12, color="#4A4A4A", family="Inter"),
        orientation="h",
        yanchor="bottom",
        y=-0.25,
        xanchor="center",
        x=0.5
    ),
    hoverlabel=dict(
        bgcolor="#FFFFFF",
        font_size=13,
        font_family="Outfit",
        bordercolor="#E9ECEF"
    )
)

# --- Funções de Carregamento de Dados ---
@st.cache_data
def carregar_dados_kpi(file):
    try:
        xls = pd.ExcelFile(file, engine='openpyxl')
        df = None
        for sheet_name in xls.sheet_names:
            if 'DADO' in sheet_name.upper():
                df = pd.read_excel(xls, sheet_name=sheet_name)
                cols_lower = [str(c).lower() for c in df.columns]
                if not any(k in cols_lower for k in ['ano/mês', 'data', 'ano', 'date', 'dia', 'itens coletados', 'saúde da marca']):
                    df_h1 = pd.read_excel(xls, sheet_name=sheet_name, header=1)
                    cols_h1_lower = [str(c).lower() for c in df_h1.columns]
                    if any(k in cols_h1_lower for k in ['ano/mês', 'data', 'ano', 'date', 'dia', 'itens coletados', 'saúde da marca']):
                        df = df_h1
                break
        if df is None:
            df = pd.read_excel(xls, sheet_name=0)
        return df
    except Exception as e:
        return f"Erro ao carregar KPIs: {e}"

@st.cache_data
def carregar_dados_relatorio_sheets(json_key_path, sheet_id, sheet_name="Dados"):
    try:
        if not HAS_GSPREAD:
            return "Biblioteca gspread não instalada."
        
        # Conectar ao Google Sheets
        gc = gspread.service_account(filename=json_key_path)
        sh = gc.open_by_key(sheet_id)
        worksheet = sh.worksheet(sheet_name)
        
        # Puxar todos os registros e converter para DataFrame
        data = worksheet.get_all_records()
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        return f"Erro ao acessar Google Sheets: {e}"

@st.cache_data
def carregar_dados_saude_marca_sheets(json_key_path, sheet_id, sheet_name="DADOS"):
    """Carrega os dados de Saúde de Marca via Google Sheets API (somente leitura)."""
    try:
        if not HAS_GSPREAD:
            return "Biblioteca gspread não instalada."
        
        gc = gspread.service_account(filename=json_key_path)
        sh = gc.open_by_key(sheet_id)
        worksheet = sh.worksheet(sheet_name)
        
        # Ler todos os valores brutos para detectar header correto
        all_values = worksheet.get_all_values()
        if not all_values:
            return "Planilha de Saúde de Marca está vazia."
        
        # Detectar linha de header: procura a linha que contenha palavras-chave relevantes
        header_row_idx = 0
        keywords = ['ano', 'mês', 'data', 'saúde', 'itens', 'positivo', 'negativo', 'neutro']
        for i, row in enumerate(all_values[:5]):
            row_lower = [str(c).lower() for c in row]
            if any(any(kw in cell for kw in keywords) for cell in row_lower):
                header_row_idx = i
                break
        
        headers = all_values[header_row_idx]
        data_rows = all_values[header_row_idx + 1:]
        df = pd.DataFrame(data_rows, columns=headers)
        
        # Remover colunas sem nome (células vazias de cabeçalho)
        df = df.loc[:, df.columns.str.strip() != '']
        
        # Remover linhas completamente vazias
        df = df.replace('', pd.NA).dropna(how='all')
        
        # Limpar coluna Saúde da marca: "100,00%" → 100.0, "-" → NaN
        col_saude_raw = next(
            (c for c in df.columns if 'sa' in str(c).lower() and 'de' in str(c).lower()),
            None
        )
        if col_saude_raw:
            df[col_saude_raw] = (
                df[col_saude_raw]
                .astype(str)
                .str.replace('%', '', regex=False)
                .str.replace(',', '.', regex=False)
                .str.strip()
                .replace('-', pd.NA)
                .replace('nan', pd.NA)
            )
            df[col_saude_raw] = pd.to_numeric(df[col_saude_raw], errors='coerce')
        
        # Converter colunas numéricas conhecidas
        numeric_kws = ['itens', 'positivo', 'negativo', 'neutro',
                       'mato grosso', 'corumb', 'ladário', 'três lagoas']
        for col in df.columns:
            if any(kw in str(col).lower() for kw in numeric_kws):
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        return df
    except Exception as e:
        return f"Erro ao acessar Saúde de Marca (Sheets): {e}"

def carregar_dados_relatorio(file):
    # Mantendo a função original como fallback para arquivos locais se necessário
    try:
        xls = pd.ExcelFile(file, engine='openpyxl')
        sheet_name = 'Dados' if 'Dados' in xls.sheet_names else xls.sheet_names[0]
        df = pd.read_excel(xls, sheet_name=sheet_name)
        return df
    except Exception as e:
        return f"Erro ao carregar Notícias local: {e}"

# --- Interface Principal ---
# Definindo caminhos fixos para os dados base
PATH_KPI = 'dados-exemplo/Cópia de LHG MINING _ Monitoramento - Dados.xlsx'
GOOGLE_SHEET_ID = '1SOOtsF-YnNyohJaAqUaMT53kjjIBBjP-LzkyqKiWUb4'
GOOGLE_SHEET_ID_SAUDE = '10EjGlvgJCRWfhZRRsKjF5W6DdDzn7cYdxhrCoo8pGBo'
JSON_CREDENTIALS = 'json-acesso/dashboard-lhg-05e1d2eb9646.json'

with st.sidebar:
    # Logo LHG Mining
    st.image("assets/Lhg-01.webp", width=250)
    st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: #FFFFFF; padding: 20px; border-radius: 16px; border: 1px solid rgba(0,0,0,0.02); border-left: 4px solid #FF6600; margin-bottom: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.03);">
        <p style="margin: 0 0 10px 0; font-family: 'Outfit', sans-serif; font-weight: 800; color: #1A1A1A; font-size: 14px; letter-spacing: 1px;">📊 STATUS DO SISTEMA</p>
        <p style="margin: 0; font-size: 13px; color: #666; line-height: 1.6;">
            Conectado à <b>Base de Dados LHG</b>.<br>
            Monitoramento industrial ativo.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: #FFFFFF; padding: 20px; border-radius: 16px; border: 1px solid rgba(0,0,0,0.02); border-left: 4px solid #28A745; margin-bottom: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.03);">
        <p style="margin: 0 0 10px 0; font-family: 'Outfit', sans-serif; font-weight: 800; color: #1A1A1A; font-size: 14px; letter-spacing: 1px;">📰 INTELIGÊNCIA ATIVA</p>
        <p style="margin: 0; font-size: 13px; color: #666; line-height: 1.6;">
            Clipping em tempo real integrado.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Rodapé da Sidebar - 80 20 Marketing
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("""
        <div style="padding: 20px; text-align: center; opacity: 0.8; transition: opacity 0.3s ease;" onmouseover="this.style.opacity=1" onmouseout="this.style.opacity=0.8">
            <p style="font-size: 11px; color: #888; font-family: 'Inter', sans-serif; margin-bottom: 10px; font-weight: 600; letter-spacing: 1px;">DESENVOLVIDO POR</p>
            <img src="data:image/png;base64,{}" width="130" style="filter: drop-shadow(0px 4px 6px rgba(0,0,0,0.1));">
        </div>
    """.format(base64.b64encode(open("assets/Logo-80-20-Marketing_preta.png", "rb").read()).decode()), unsafe_allow_html=True)

with st.spinner("Estruturando matriz de dados..."):
    # Carregando dados de Saúde de Marca via Google Sheets (planilha saude de marca)
    df_kpi = carregar_dados_saude_marca_sheets(JSON_CREDENTIALS, GOOGLE_SHEET_ID_SAUDE, "DADOS")
    
    # Fallback para arquivo local se a conexão com Sheets de saúde falhar
    if isinstance(df_kpi, str) and "Erro" in df_kpi:
        st.warning(f"Conexão com Google Sheets (Saúde de Marca) falhou: {df_kpi}. Carregando arquivo local de backup...")
        df_kpi = carregar_dados_kpi(PATH_KPI)

    # Carregando dados de notícias/relatório via Google Sheets
    df_relatorio = carregar_dados_relatorio_sheets(JSON_CREDENTIALS, GOOGLE_SHEET_ID, "Dados")
    
    # Fallback se a conexão com Sheets de relatório falhar
    if isinstance(df_relatorio, str) and "Erro ao acessar Google Sheets" in df_relatorio:
        st.warning("Conexão com Google Sheets (Relatório) falhou. Tentando carregar arquivo local de backup...")
        df_relatorio = carregar_dados_relatorio('dados-exemplo/dados-lhg.xlsx')

if isinstance(df_kpi, str): st.error(f"Erro ao carregar KPI: {df_kpi}"); st.stop()
if isinstance(df_relatorio, str): st.error(f"Erro ao carregar Relatório: {df_relatorio}"); st.stop()

# --- Limpeza e Filtros df_kpi ---
x_col_kpi = None
for col in df_kpi.columns:
    if str(col).lower() in ['ano/mês', 'data', 'ano', 'date', 'mês/ano', 'dia']:
        x_col_kpi = col
        break

if x_col_kpi:
    df_kpi = df_kpi.dropna(subset=[x_col_kpi]).copy()
    df_kpi[x_col_kpi] = df_kpi[x_col_kpi].astype(str)
    
    # REMOVER DADOS DE 2024
    df_kpi = df_kpi[~df_kpi[x_col_kpi].str.contains('2024', na=False)]
    df_kpi = df_kpi.sort_values(by=x_col_kpi)

cols_kpi_lower = {str(c).lower(): c for c in df_kpi.columns}
col_saude = cols_kpi_lower.get('saúde da marca')
col_itens = cols_kpi_lower.get('itens coletados')
col_positivo = cols_kpi_lower.get('positivo')
col_negativo = cols_kpi_lower.get('negativo')
col_neutro = cols_kpi_lower.get('neutro')

# Limpeza Notícias
cols_rel_lower = {str(c).lower(): c for c in df_relatorio.columns}
col_data_news = cols_rel_lower.get('data')
col_sentimento_news = cols_rel_lower.get('sentimento')
col_portal_news = cols_rel_lower.get('portal') or cols_rel_lower.get('veículo')
col_titulo_news = cols_rel_lower.get('título') or cols_rel_lower.get('titulo')
col_link_news = cols_rel_lower.get('link') or cols_rel_lower.get('url')


@st.cache_data(show_spinner=False)
def gerar_pdf_completo(df_kpi, df_news, _figs_dict, kpi_data):
    from fpdf import FPDF
    import tempfile
    import os
    
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # --- Página 1: Sumário e Métricas Operacionais ---
    pdf.add_page()
    pdf.set_fill_color(0, 0, 0)  # Solid Black
    pdf.rect(0, 0, 210, 45, 'F')
    pdf.set_font("Helvetica", 'B', 24)
    pdf.set_text_color(255, 255, 255)
    pdf.set_xy(20, 15)
    pdf.cell(0, 10, "LHG MINING", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", 'B', 12)
    pdf.set_text_color(255, 102, 0) # Orange
    pdf.set_x(20)
    pdf.cell(0, 10, "RELATORIO DE INTELIGENCIA ESTRATEGICA", new_x="LMARGIN", new_y="NEXT")
    
    # Logo LHG Mining (Header)
    try:
        # Converter webp para png temporário para o fpdf se necessário, 
        # mas fpdf2 costuma aceitar se tiver Pillow. Vamos tentar direto.
        pdf.image("assets/Lhg-01.webp", x=160, y=10, w=35)
    except:
        pass
        
    pdf.set_font("Helvetica", '', 9)
    pdf.set_text_color(150, 150, 150)
    pdf.set_xy(20, 32)
    pdf.cell(0, 8, f"Relatorio Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_fill_color(255, 102, 0) # Orange
    pdf.rect(0, 45, 210, 2, 'F')
    pdf.ln(20)
    
    # KPIs Section
    pdf.set_font("Helvetica", 'B', 14)
    pdf.set_text_color(26, 26, 26)
    pdf.cell(0, 10, "1. INDICADORES DE PERFORMANCE (KPIs)", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    
    # Desenhar "Cards" de KPI no PDF
    col_w = 80
    pdf.set_font("Helvetica", 'B', 9)
    y_start_kpi = pdf.get_y()
    for i, (label, value) in enumerate(kpi_data):
        x = 20 + (i % 2) * (col_w + 10)
        row = i // 2
        curr_y = y_start_kpi + (row * 22)
        pdf.set_xy(x, curr_y)
        pdf.set_fill_color(245, 245, 245)
        pdf.rect(x, curr_y, col_w, 18, 'F')
        pdf.set_fill_color(255, 102, 0)
        pdf.rect(x, curr_y, 1.5, 18, 'F')
        pdf.set_text_color(100, 100, 100)
        pdf.set_xy(x + 5, curr_y + 3)
        pdf.cell(col_w - 5, 5, label.upper())
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Helvetica", 'B', 14)
        pdf.set_xy(x + 5, curr_y + 8)
        pdf.cell(col_w - 5, 8, str(value))
        pdf.set_font("Helvetica", 'B', 9)
    
    pdf.set_y(y_start_kpi + 50)
    
    # Inserir Gráficos de Métricas
    for fig_key in ['saude', 'stack']:
        if fig_key in _figs_dict:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
                # Aumentando escala para 3 e ajustando dimensões para legibilidade
                _figs_dict[fig_key].write_image(tmpfile.name, width=1200, height=600, scale=3)
                pdf.image(tmpfile.name, x=15, w=180)
                os.unlink(tmpfile.name)
            pdf.ln(8)
            
    # --- Inteligência de Mídia ---
    if pdf.get_y() > 220: pdf.add_page()
    else: pdf.ln(10)
    
    pdf.set_font("Helvetica", 'B', 14)
    pdf.set_text_color(26, 26, 26)
    pdf.cell(0, 10, "2. ANALISE DE EXPOSICAO E SENTIMENTO", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    
    for fig_key in ['pie', 'portal', 'time']:
        if fig_key in _figs_dict:
            if pdf.get_y() > 210: pdf.add_page()
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
                h_img = 500 if fig_key == 'pie' else 600
                _figs_dict[fig_key].write_image(tmpfile.name, width=1200, height=h_img, scale=3)
                # Se for o pizza, aumentar significativamente e centralizar
                w_img = 150 if fig_key == 'pie' else 180
                x_img = 30 if fig_key == 'pie' else 15
                pdf.image(tmpfile.name, x=x_img, w=w_img)
                os.unlink(tmpfile.name)
            pdf.ln(8)
            
    # --- Radar de Notícias ---
    if pdf.get_y() > 200: pdf.add_page()
    else: pdf.ln(10)
    
    pdf.set_font("Helvetica", 'B', 14)
    pdf.set_text_color(26, 26, 26)
    pdf.cell(0, 10, "3. RADAR DE EVENTOS (ULTIMAS MATERIAS)", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    
    for _, row in df_news.head(30).iterrows():
        if pdf.get_y() > 260: pdf.add_page()
        
        sent = str(row.get(col_sentimento_news, 'Neutro')).lower()
        if 'pos' in sent: color = (46, 125, 50)
        elif 'neg' in sent: color = (198, 40, 40)
        else: color = (100, 100, 100)
        
        pdf.set_fill_color(*color)
        pdf.rect(20, pdf.get_y(), 1.5, 12, 'F')
        
        pdf.set_x(25)
        pdf.set_font("Helvetica", 'B', 8)
        pdf.set_text_color(color[0], color[1], color[2])
        portal = str(row.get(col_portal_news, 'N/A'))
        pdf.cell(0, 4, f"{portal.upper()}", new_x="LMARGIN", new_y="NEXT")
        
        pdf.set_x(25)
        pdf.set_font("Helvetica", '', 8)
        pdf.set_text_color(30, 30, 30)
        titulo = str(row.get(col_titulo_news, 'Sem título'))[:180]
        pdf.multi_cell(165, 4, titulo)
        
        # Link no PDF
        link = row.get(col_link_news)
        if pd.notna(link) and str(link).startswith('http'):
            pdf.set_x(25)
            pdf.set_font("Helvetica", 'I', 7)
            pdf.set_text_color(0, 102, 204)
            pdf.cell(0, 4, "Acessar materia original", new_x="LMARGIN", new_y="NEXT", link=str(link))
            
        pdf.ln(2)
        pdf.set_draw_color(230, 230, 230)
        pdf.line(20, pdf.get_y(), 190, pdf.get_y())
        pdf.ln(3)
        
    # Rodapé Final com Logo 80 20
    pdf.add_page()
    pdf.set_y(100)
    pdf.set_font("Helvetica", 'I', 10)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 10, "Relatorio desenvolvido por", new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.ln(5)
    try:
        pdf.image("assets/Logo-80-20-Marketing_preta.png", x=85, w=40)
    except:
        pass
        
    # Salvar em bytes via output interno do fpdf2
    pdf_out = pdf.output()
    return bytes(pdf_out) if not isinstance(pdf_out, bytes) else pdf_out

# --- Central de Processamento de Dados e Gráficos (Para Exportação) ---
col_saude_plot = None
disp_atual, disp_delta, delta_class = "N/A", "N/A", "delta-neutral"
total_itens, total_pos, total_neg = 0, 0, 0
figs_para_pdf = {}

if x_col_kpi and not df_kpi.empty:
    if col_saude:
        df_kpi[col_saude] = pd.to_numeric(df_kpi[col_saude], errors='coerce')
        is_decimal = df_kpi[col_saude].max() <= 1.5
        df_kpi['Saúde da Marca (%)'] = (df_kpi[col_saude] * 100 if is_decimal else df_kpi[col_saude]).round(1)
        col_saude_plot = 'Saúde da Marca (%)'
        val_atual = df_kpi['Saúde da Marca (%)'].iloc[-1]
        val_ant = df_kpi['Saúde da Marca (%)'].iloc[-2] if len(df_kpi) > 1 else val_atual
        try:
            delta = float(val_atual) - float(val_ant)
            disp_delta = f"{'+' if delta > 0 else ''}{delta:.1f}%".replace('.', ',')
            delta_class = "delta-up" if delta > 0 else ("delta-down" if delta < 0 else "delta-neutral")
        except: pass
        disp_atual = f"{float(val_atual):.1f}%".replace('.', ',') if pd.notna(val_atual) else "N/A"

    total_itens = int(df_kpi[col_itens].sum()) if col_itens else 0
    total_pos = int(df_kpi[col_positivo].sum()) if col_positivo else 0
    total_neg = int(df_kpi[col_negativo].sum()) if col_negativo else 0

    # Gerar figuras antecipadamente para o PDF
    if col_saude:
        fig_saude = go.Figure()
        fig_saude.add_trace(go.Scatter(
            x=df_kpi[x_col_kpi], y=df_kpi[col_saude_plot],
            mode='lines+markers+text', 
            line=dict(color='#F37021', width=5, shape='spline'),
            marker=dict(size=14, color='#F37021', line=dict(width=3, color='#FFFFFF'), symbol='circle'),
            text=df_kpi[col_saude_plot].apply(lambda x: f"{x}%"),
            textposition="top center",
            textfont=dict(size=11, color="#2C3E50", family="Outfit"),
            fill='tozeroy', fillcolor='rgba(243,112,33,0.1)', name='Saúde da Marca'
        ))
        fig_saude.update_layout(**plotly_layout_defaults, title_text='EVOLUÇÃO DO ÍNDICE DE SAÚDE DA MARCA', showlegend=True)
        figs_para_pdf['saude'] = fig_saude

    cols_sent = [c for c in [col_positivo, col_neutro, col_negativo] if c]
    if cols_sent:
        df_melt = df_kpi.melt(id_vars=[x_col_kpi], value_vars=cols_sent, var_name="Sentimento", value_name="Quantidade")
        COLOR_MAP_STACK = {'Positivo': '#52BE80', 'Neutro': '#95A5A6', 'Negativo': '#E74C3C'}
        fig_stack = px.bar(df_melt, x=x_col_kpi, y="Quantidade", color="Sentimento", 
                           template=PLOTLY_TEMPLATE, color_discrete_map=COLOR_MAP_STACK,
                           text="Quantidade")
        fig_stack.update_layout(**plotly_layout_defaults, title_text='COMPOSIÇÃO DE IMPACTO POR CICLO', barmode='stack', showlegend=True)
        fig_stack.update_traces(textposition='inside', marker_line_width=0)
        figs_para_pdf['stack'] = fig_stack

# Processamento de Mídia
if col_sentimento_news:
    df_news_plot = df_relatorio.copy()
    def padronizar_sentimento(val):
        val = str(val).lower().strip()
        if 'pos' in val: return 'Positivo'
        elif 'neg' in val: return 'Negativo'
        else: return 'Neutro'
    df_news_plot[col_sentimento_news] = df_news_plot[col_sentimento_news].apply(padronizar_sentimento)
    
    cont_sent = df_news_plot[col_sentimento_news].value_counts().reset_index()
    cont_sent.columns = ['Sentimento', 'Volume']
    fig_pie = px.pie(cont_sent, names='Sentimento', values='Volume', color='Sentimento', color_discrete_map=COLOR_MAP, template=PLOTLY_TEMPLATE, hole=0.6)
    fig_pie.update_layout(**plotly_layout_defaults, title_text='PROPORÇÃO GLOBAL DE MÍDIA', showlegend=True, legend_orientation='h', legend_yanchor='bottom', legend_y=-0.2, legend_xanchor='center', legend_x=0.5)
    figs_para_pdf['pie'] = fig_pie

    if col_portal_news:
        df_portais = df_news_plot.groupby([col_portal_news, col_sentimento_news]).size().reset_index(name='Quantidade')
        top_portais = df_news_plot[col_portal_news].value_counts().nlargest(8).index
        df_portais_top = df_portais[df_portais[col_portal_news].isin(top_portais)]
        fig_portal = px.bar(df_portais_top, y=col_portal_news, x='Quantidade', color=col_sentimento_news, orientation='h', template=PLOTLY_TEMPLATE, color_discrete_map=COLOR_MAP)
        fig_portal.update_layout(**plotly_layout_defaults, title_text='TOP VEÍCULOS / PORTAIS', showlegend=True, legend_orientation='h', legend_y=1.05)
        figs_para_pdf['portal'] = fig_portal

    if col_data_news:
        try:
            df_news_plot[col_data_news] = pd.to_datetime(df_news_plot[col_data_news], dayfirst=True)
            df_tempo = df_news_plot.groupby([pd.Grouper(key=col_data_news, freq='W-MON'), col_sentimento_news]).size().reset_index(name='Quantidade')
            fig_time = px.line(df_tempo, x=col_data_news, y='Quantidade', color=col_sentimento_news, template=PLOTLY_TEMPLATE, color_discrete_map=COLOR_MAP, markers=True)
            fig_time.update_layout(**plotly_layout_defaults, title_text='TENDÊNCIA TEMPORAL (VOLUME DE NOTÍCIAS)', showlegend=True, legend_orientation='h', legend_y=1.05)
            fig_time.update_yaxes(rangemode='tozero')
            figs_para_pdf['time'] = fig_time
        except: pass

# --- Header Dinâmico com Botão de Exportação ---
head_col1, head_col2 = st.columns([3, 1])

with head_col1:
    st.markdown("""
    <div style="margin-bottom: 30px; border-left: 5px solid #FF6600; padding-left: 20px;">
        <h1 style="margin-bottom: 5px; font-size: 2.5rem; color: #1A1A1A !important;">Monitoramento Estratégico</h1>
        <p style="color: #6C757D; font-size: 1rem; margin: 0; text-transform: uppercase; letter-spacing: 1px;">Consolidado de Inteligência Industrial | LHG Mining</p>
    </div>
    """, unsafe_allow_html=True)

with head_col2:
    st.markdown("<div style='margin-top: 12px;'></div>", unsafe_allow_html=True)
    if HAS_FPDF:
        kpi_vals = [
            ("Saude da Marca", disp_atual),
            ("Volume Total", total_itens),
            ("Midia Positiva", total_pos),
            ("Midia Negativa", total_neg)
        ]
        try:
            with st.spinner("Preparando PDF..."):
                pdf_bytes = gerar_pdf_completo(df_kpi, df_relatorio, figs_para_pdf, kpi_vals)
            
            st.download_button(
                label="📥 Exportar Relatorio PDF",
                data=pdf_bytes,
                file_name=f"Relatorio_Estrategico_LHG_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/octet-stream"
            )
        except Exception as _pdf_err:
            st.error(f"Erro ao gerar PDF: {_pdf_err}")
    else:
        st.warning("Instale fpdf2 para exportar: pip install fpdf2")



# --- Abas Premium ---
tab_dados, tab_news, tab_feed = st.tabs(["Métricas Operacionais", "Inteligência de Mídia", "Radar de Eventos"])


# ====== ABA 1: DADOS (Monitoramento) ======
with tab_dados:
    if x_col_kpi and not df_kpi.empty:
        
        # 1. Tratamento Saúde da Marca e KPIs
        if col_saude:
            df_kpi[col_saude] = pd.to_numeric(df_kpi[col_saude], errors='coerce')
            is_decimal = df_kpi[col_saude].max() <= 1.5
            df_kpi['Saúde da Marca (%)'] = (df_kpi[col_saude] * 100 if is_decimal else df_kpi[col_saude]).round(1)
            col_saude_plot = 'Saúde da Marca (%)'
            
            val_atual = df_kpi['Saúde da Marca (%)'].iloc[-1]
            val_ant = df_kpi['Saúde da Marca (%)'].iloc[-2] if len(df_kpi) > 1 else val_atual
            
            try:
                delta = float(val_atual) - float(val_ant)
                disp_delta = f"{'+' if delta > 0 else ''}{delta:.1f}%".replace('.', ',')
                if delta > 0: delta_class = "delta-up"
                elif delta < 0: delta_class = "delta-down"
                else: delta_class = "delta-neutral"
            except:
                disp_delta = "0,0%"
                delta_class = "delta-neutral"
                
            disp_atual = f"{float(val_atual):.1f}%".replace('.', ',') if pd.notna(val_atual) else "N/A"
        else:
            disp_atual = "N/A"
            disp_delta = "N/A"
            delta_class = "delta-neutral"

        total_itens = int(df_kpi[col_itens].sum()) if col_itens else 0
        total_pos = int(df_kpi[col_positivo].sum()) if col_positivo else 0
        total_neg = int(df_kpi[col_negativo].sum()) if col_negativo else 0
        
        # HTML Customizado para KPI Cards
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-card brand">
                <div class="kpi-title">Saúde da Marca Atual</div>
                <div class="kpi-value">{disp_atual}</div>
                <div class="kpi-delta {delta_class}">
                    <span style="font-size: 1.1em; margin-right: 2px;">{'↑' if delta_class == 'delta-up' else '↓' if delta_class == 'delta-down' else '-'}</span>
                    {disp_delta} no ciclo
                </div>
            </div>
            <div class="kpi-card dark">
                <div class="kpi-title">Volume Capturado</div>
                <div class="kpi-value">{total_itens}</div>
                <div class="kpi-delta delta-neutral">
                    Registros totais analisados
                </div>
            </div>
            <div class="kpi-card earth">
                <div class="kpi-title">Mídia Positiva</div>
                <div class="kpi-value">{total_pos}</div>
                <div class="kpi-delta delta-neutral">
                    Impactos favoráveis consolidados
                </div>
            </div>
            <div class="kpi-card rust">
                <div class="kpi-title">Mídia Negativa</div>
                <div class="kpi-value">{total_neg}</div>
                <div class="kpi-delta delta-neutral">
                    Registros de atenção / crise
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 2. Evolução da Saúde da Marca
        if col_saude:
            st.markdown("<h3 style='font-size: 1.2rem; margin-bottom: 25px; color:#1A1A1A; letter-spacing:1px; font-weight:800;'>EVOLUÇÃO DO ÍNDICE DE SAÚDE DA MARCA</h3>", unsafe_allow_html=True)
            fig_saude = go.Figure()
            fig_saude.add_trace(go.Scatter(
                x=df_kpi[x_col_kpi], y=df_kpi[col_saude_plot],
                mode='lines+markers+text',
                line=dict(color='#FF6600', width=5, shape='spline'),
                marker=dict(size=16, color='#FFFFFF', line=dict(width=4, color='#FF6600'), symbol='circle'),
                text=df_kpi[col_saude_plot].apply(lambda x: f"<b>{x}%</b>"),
                textposition="top center",
                textfont=dict(size=13, color="#FF6600", family="Outfit"),
                fill='tozeroy',
                fillcolor='rgba(255, 102, 0, 0.1)',
                hovertemplate="<b>Período:</b> %{x}<br><b>Saúde:</b> %{y:.1f}%<extra></extra>",
                name='Saúde da Marca'
            ))
            fig_saude.add_hline(y=50, line_dash='dash', line_color='#A0AAB5', annotation_text='META 50%',
                                annotation_font_color='#888', annotation_font_size=11, opacity=0.7)
            fig_saude.update_layout(
                **plotly_layout_defaults,
                showlegend=False
            )
            fig_saude.update_yaxes(rangemode='tozero', ticksuffix='%')
            st.plotly_chart(fig_saude, use_container_width=True, config={'displayModeBar': False}, theme=None)
            
        # 3. Empilhamento de Sentimentos
        cols_sent = [c for c in [col_positivo, col_neutro, col_negativo] if c]
        if cols_sent:
            st.markdown("<h3 style='font-size: 1.2rem; margin-bottom: 25px; margin-top: 40px; color:#1A1A1A; letter-spacing:1px; font-weight:800;'>COMPOSIÇÃO DE IMPACTO POR CICLO</h3>", unsafe_allow_html=True)
            df_melt = df_kpi.melt(id_vars=[x_col_kpi], value_vars=cols_sent, var_name="Sentimento", value_name="Quantidade")
            COLOR_MAP_STACK = {'Positivo': '#52BE80', 'Neutro': '#95A5A6', 'Negativo': '#E74C3C'}
            fig_stack = px.bar(
                df_melt, x=x_col_kpi, y="Quantidade", color="Sentimento",
                template=PLOTLY_TEMPLATE,
                color_discrete_map=COLOR_MAP_STACK
            )
            fig_stack.update_layout(
                **plotly_layout_defaults,
                barmode='stack'
            )
            fig_stack.update_traces(marker_line_width=0, opacity=0.9, hovertemplate="<b>%{x}</b><br>%{color}: %{y}<extra></extra>")
            st.plotly_chart(fig_stack, use_container_width=True, config={'displayModeBar': False}, theme=None)

        pass

    elif not x_col_kpi:
        st.warning("Falha ao localizar coluna de Tempo na aba DADOS.")
    else:
        st.info("A base resultou vazia após o filtro (>2024). Insira dados atualizados.")

# ====== ABA 2: ANÁLISE DE MÍDIA ======
with tab_news:
    st.markdown("<br>", unsafe_allow_html=True)
    if col_sentimento_news:
        df_news_plot = df_relatorio.copy()
        def padronizar_sentimento(val):
            val = str(val).lower().strip()
            if 'pos' in val: return 'Positivo'
            elif 'neg' in val: return 'Negativo'
            else: return 'Neutro'
        df_news_plot[col_sentimento_news] = df_news_plot[col_sentimento_news].apply(padronizar_sentimento)
        
        c1, c2 = st.columns([1, 1.2], gap="large")
        
        with c1:
            st.markdown("<h3 style='font-size: 1.2rem; margin-bottom: 25px; color:#1A1A1A; letter-spacing:1px; font-weight:800;'>PROPORÇÃO GLOBAL DE MÍDIA</h3>", unsafe_allow_html=True)
            cont_sent = df_news_plot[col_sentimento_news].value_counts().reset_index()
            cont_sent.columns = ['Sentimento', 'Volume']
            COLOR_PIE = {'Positivo': '#52BE80', 'Negativo': '#E74C3C', 'Neutro': '#95A5A6'}
            fig_pie = px.pie(
                cont_sent, names='Sentimento', values='Volume',
                color='Sentimento', color_discrete_map=COLOR_PIE,
                template=PLOTLY_TEMPLATE, hole=0.65
            )
            fig_pie.update_traces(
                textposition='outside', textinfo='percent+label',
                textfont=dict(size=14, color='#1A1A1A', family='Outfit', weight="bold"),
                marker=dict(line=dict(color='#FFFFFF', width=4)),
                pull=[0.02, 0.02, 0.02],
                hovertemplate="<b>%{label}</b><br>Volume: %{value} (%{percent})<extra></extra>"
            )
            fig_pie.update_layout(
                **plotly_layout_defaults,
                showlegend=False
            )
            st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False}, theme=None)
        
        with c2:
            if col_portal_news:
                st.markdown("<h3 style='font-size: 1.2rem; margin-bottom: 25px; color:#1A1A1A; letter-spacing:1px; font-weight:800;'>TOP VEÍCULOS / PORTAIS</h3>", unsafe_allow_html=True)
                df_portais = df_news_plot.groupby([col_portal_news, col_sentimento_news]).size().reset_index(name='Quantidade')
                top_portais = df_news_plot[col_portal_news].value_counts().nlargest(8).index
                df_portais_top = df_portais[df_portais[col_portal_news].isin(top_portais)]
                COLOR_PORTAL = {'Positivo': '#52BE80', 'Negativo': '#E74C3C', 'Neutro': '#95A5A6'}
                fig_portal = px.bar(
                    df_portais_top, y=col_portal_news, x='Quantidade', color=col_sentimento_news,
                    orientation='h', template=PLOTLY_TEMPLATE, color_discrete_map=COLOR_PORTAL
                )
                fig_portal.update_layout(
                    **plotly_layout_defaults,
                    showlegend=True
                )
                fig_portal.update_layout(
                    legend=dict(yanchor="bottom", y=1.02, xanchor="right", x=1, orientation="h")
                )
                fig_portal.update_yaxes(categoryorder='total ascending', title="", tickfont=dict(size=12, color="#1A1A1A"))
                fig_portal.update_traces(marker_line_width=0, opacity=0.9, hovertemplate="<b>%{y}</b><br>%{color}: %{x}<extra></extra>")
                st.plotly_chart(fig_portal, use_container_width=True, config={'displayModeBar': False}, theme=None)
        
        st.markdown("<hr style='margin: 40px 0; border: none; height: 1px; background: linear-gradient(90deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0.05) 50%, rgba(0,0,0,0) 100%);'>", unsafe_allow_html=True)
        
        if col_data_news:
            try:
                st.markdown("<h3 style='font-size: 1.2rem; margin-bottom: 25px; color:#1A1A1A; letter-spacing:1px; font-weight:800;'>TENDÊNCIA TEMPORAL (VOLUME DE NOTÍCIAS)</h3>", unsafe_allow_html=True)
                df_news_plot[col_data_news] = pd.to_datetime(df_news_plot[col_data_news], dayfirst=True)
                df_tempo = df_news_plot.groupby([pd.Grouper(key=col_data_news, freq='W-MON'), col_sentimento_news]).size().reset_index(name='Quantidade')
                COLOR_TIME = {'Positivo': '#52BE80', 'Negativo': '#E74C3C', 'Neutro': '#95A5A6'}
                fig_time = px.line(
                    df_tempo, x=col_data_news, y='Quantidade', color=col_sentimento_news,
                    template=PLOTLY_TEMPLATE, color_discrete_map=COLOR_TIME, markers=True
                )
                fig_time.update_traces(
                    line=dict(width=4, shape='spline'),
                    marker=dict(size=12, line=dict(width=3, color='#FFFFFF'), symbol='circle'),
                    opacity=0.9,
                    hovertemplate="<b>Data:</b> %{x}<br><b>Volume:</b> %{y}<extra></extra>"
                )
                fig_time.update_layout(
                    **plotly_layout_defaults,
                    showlegend=True
                )
                fig_time.update_layout(
                    legend=dict(yanchor="bottom", y=1.02, xanchor="right", x=1, orientation="h")
                )
                fig_time.update_yaxes(rangemode='tozero', zeroline=True, zerolinecolor='#F1F3F5', title="")
                fig_time.update_xaxes(title="")
                st.plotly_chart(fig_time, use_container_width=True, config={'displayModeBar': False}, theme=None)
            except:
                pass
    else:
        st.info("A coluna Sentimento não foi identificada nas Notícias.")

# ====== ABA 3: FEED VISUAL DE EVENTOS ======
with tab_feed:
    st.markdown("<br>", unsafe_allow_html=True)
    
    if col_data_news and col_titulo_news:
        
        filtro_sentimento = st.selectbox(
            "Filtrar por Sentimento:", 
            ["Todas", "Positivas", "Neutras", "Negativas"],
            index=0
        )
        st.markdown("<br>", unsafe_allow_html=True)

        df_feed = df_relatorio.copy()
        
        if filtro_sentimento != "Todas":
            sent_prefix = filtro_sentimento.lower()[:3]
            if col_sentimento_news:
                df_feed = df_feed[df_feed[col_sentimento_news].astype(str).str.lower().str.contains(sent_prefix, na=False)]
                
        try:
            df_feed[col_data_news] = pd.to_datetime(df_feed[col_data_news], dayfirst=True)
            df_feed = df_feed.sort_values(by=col_data_news, ascending=False).head(30)
        except:
            df_feed = df_feed.head(30)
            
        # Container Grid Nativo CSS
        cards_html = "<div class='news-grid'>"
        
        for idx, row in df_feed.iterrows():
            titulo = row[col_titulo_news] if pd.notna(row[col_titulo_news]) else "Matéria sem título"
            try:
                if isinstance(row[col_data_news], pd.Timestamp):
                    data_str = row[col_data_news].strftime('%d/%m/%Y')
                else:
                    data_str = str(row[col_data_news]).split(' ')[0]
            except:
                data_str = str(row[col_data_news])
            
            sent_val = row[col_sentimento_news] if col_sentimento_news else "Neutro"
            sent_val_str = str(sent_val).lower().strip() if pd.notna(sent_val) else ""
            if 'pos' in sent_val_str:
                sentimento = 'Positivo'
                badge_class = "badge-pos"
            elif 'neg' in sent_val_str:
                sentimento = 'Negativo'
                badge_class = "badge-neg"
            else:
                sentimento = 'Neutro'
                badge_class = "badge-neu"
                
            portal_info = f"{row[col_portal_news]}" if col_portal_news and pd.notna(row[col_portal_news]) else "Veículo não informado"
            link_url = row[col_link_news] if col_link_news and pd.notna(row[col_link_news]) else "#"
            link_display = "display: inline-block;" if link_url != "#" else "display: none;"
            
            cards_html += f"""
<div class="news-card-premium {badge_class.replace('badge-', '')}">
    <div>
        <span class="news-header-badge {badge_class}">{sentimento}</span>
        <div class="news-card-title">{html.escape(str(titulo))}</div>
    </div>
    <div>
        <div class="news-card-footer">
            <div>
                <div class="news-portal">{html.escape(str(portal_info))}</div>
                <div class="news-date">{data_str}</div>
            </div>
        </div>
        <div style="margin-top: 20px; {link_display}">
            <a href="{link_url}" target="_blank" class="news-action">Ler matéria completa ↗</a>
        </div>
    </div>
</div>
"""
            
        cards_html += "</div>"
        st.markdown(cards_html, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        pass

        st.markdown("<br><br>", unsafe_allow_html=True)
    else:
        st.warning("Colunas Título/Data ausentes na planilha de Notícias.")
