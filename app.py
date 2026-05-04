import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import html

# --- Configuração da Página ---
st.set_page_config(
    page_title="LHG Mining",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Estética Premium (Clean & Minimalista, Identidade LHG Mining) ---
st.markdown("""
    <style>
    /* Importação de Fontes Premium */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Inter:wght@400;500;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 800 !important;
        color: #111111 !important;
        letter-spacing: -0.5px;
    }
    
    /* Fundo da Aplicação */
    .stApp {
        background-color: #F7F8FA;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #EBEBEB;
    }
    
    /* Esconder elementos padrão desnecessários, mantendo o toggle do sidebar */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header { visibility: hidden; }
    [data-testid="stSidebarCollapseAction"] { visibility: visible !important; }
    .stDeployButton { display: none !important; }
    
    /* Customização das Abas (Tabs) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        border-bottom: 2px solid #EBEBEB;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 0px 0px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
        font-family: 'Outfit', sans-serif;
        font-weight: 600;
        font-size: 1.1rem;
        color: #777777;
    }
    .stTabs [aria-selected="true"] {
        color: #111111 !important;
        border-bottom: 3px solid #FF5A00 !important;
    }
    
    /* Container customizado para KPIs (estilo premium) */
    .kpi-container {
        display: flex;
        gap: 20px;
        margin-bottom: 30px;
        margin-top: 10px;
        flex-wrap: wrap;
    }
    .kpi-card {
        flex: 1;
        min-width: 200px;
        background: #FFFFFF;
        padding: 24px 30px;
        border-radius: 16px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.03);
        border: 1px solid rgba(0,0,0,0.02);
        position: relative;
        overflow: hidden;
    }
    /* Linha de sotaque no card de KPI */
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 4px;
        background: #EBEBEB;
    }
    .kpi-card.brand::before { background: #FF5A00; }
    .kpi-card.rust::before { background: #A64030; }
    .kpi-card.earth::before { background: #4A7045; }
    .kpi-card.dark::before { background: #111111; }
    
    .kpi-title {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
        color: #888888;
        margin-bottom: 10px;
    }
    .kpi-value {
        font-family: 'Outfit', sans-serif;
        font-size: 2.8rem;
        font-weight: 800;
        color: #111111;
        line-height: 1;
        margin-bottom: 5px;
    }
    .kpi-delta {
        font-size: 0.9rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 5px;
    }
    .delta-up { color: #4A7045; }
    .delta-down { color: #A64030; }
    .delta-neutral { color: #888888; }
    
    /* Feed de Notícias Premium */
    .news-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
        gap: 24px;
        margin-top: 20px;
    }
    .news-card-premium {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 30px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.03);
        border: 1px solid rgba(0,0,0,0.03);
        display: flex;
        flex-direction: column;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .news-card-premium:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 50px rgba(0,0,0,0.06);
    }
    .news-header-badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 16px;
    }
    .badge-pos { background: #EDF3ED; color: #4A7045; }
    .badge-neg { background: #FAEDEB; color: #A64030; }
    .badge-neu { background: #F5F5F5; color: #777777; }
    
    .news-card-title {
        font-family: 'Outfit', sans-serif;
        font-size: 1.25rem;
        font-weight: 700;
        color: #111111;
        line-height: 1.3;
        margin-bottom: 16px;
    }
    
    .news-card-footer {
        margin-top: auto;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-top: 1px solid #F0F0F0;
        padding-top: 16px;
    }
    .news-date {
        font-size: 0.85rem;
        color: #888888;
        font-weight: 500;
    }
    .news-portal {
        font-size: 0.85rem;
        color: #111111;
        font-weight: 600;
    }
    .news-action {
        display: inline-block;
        margin-top: 15px;
        color: #FF5A00;
        text-decoration: none;
        font-weight: 600;
        font-size: 0.9rem;
        transition: color 0.2s;
    }
    .news-action:hover { color: #A64030; }
    
    /* Customização dos Expander e gráficos */
    .streamlit-expanderHeader {
        font-family: 'Outfit', sans-serif;
        font-weight: 600;
    }
    
    /* Uploaders de Arquivos */
    [data-testid="stFileUploader"] {
        background-color: transparent !important;
    }
    [data-testid="stFileUploadDropzone"] {
        background-color: #FFFFFF !important;
        border: 2px dashed #FF5A00 !important;
        border-radius: 12px;
        padding: 20px;
        transition: all 0.3s ease;
    }
    [data-testid="stFileUploadDropzone"]:hover {
        background-color: #FFF3EB !important;
        border-color: #A64030 !important;
    }
    [data-testid="stFileUploadDropzone"] svg {
        fill: #FF5A00 !important;
        color: #FF5A00 !important;
    }
    [data-testid="stFileUploadDropzone"] *, 
    [data-testid="stFileUploader"] * {
        color: #111111 !important;
    }
    [data-testid="stFileUploadDropzone"] button {
        background-color: #F7F8FA !important;
        color: #111111 !important;
        border: 1px solid #EBEBEB !important;
    }
    [data-testid="stFileUploadDropzone"] small {
        display: none !important; /* Esconde texto genérico (limit 200mb) */
    }
    
    /* Estilo Premium para Gráficos */
    [data-testid="stPlotlyChart"] {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 15px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.04);
        border: 1px solid #F0F0F0;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    [data-testid="stPlotlyChart"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 32px rgba(0,0,0,0.08);
    }
    </style>
""", unsafe_allow_html=True)

# Paleta global (LHG Mining)
# Laranja vibrante: #FF5A00 | Vermelho Ferrugem: #A64030 | Verde Pantanal: #4A7045 | Preto/Cinza Chumbo: #111111
COLOR_MAP = {'Positivo': '#4A7045', 'Negativo': '#A64030', 'Neutro': '#999999'}
CHART_COLORS = ['#FF5A00', '#111111', '#A64030', '#4A7045', '#888888']
PLOTLY_TEMPLATE = 'plotly_white'

# Ocultando gráficos nativos que parecem poluídos
plotly_layout_defaults = dict(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#333333"),
    xaxis=dict(showgrid=False, zeroline=False),
    yaxis=dict(showgrid=True, gridcolor="#EBEBEB", zeroline=False),
    margin=dict(l=0, r=0, t=70, b=40)
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
def carregar_dados_relatorio(file):
    try:
        xls = pd.ExcelFile(file, engine='openpyxl')
        sheet_name = 'Dados' if 'Dados' in xls.sheet_names else xls.sheet_names[0]
        df = pd.read_excel(xls, sheet_name=sheet_name)
        return df
    except Exception as e:
        return f"Erro ao carregar Notícias: {e}"

# --- Interface Principal ---
# Definindo caminhos fixos para os dados base
PATH_KPI = 'dados-exemplo/Cópia de LHG MINING _ Monitoramento - Dados.xlsx'
PATH_RELATORIO = 'dados-exemplo/dados-lhg.xlsx'

with st.sidebar:
    # Logo LHG Mining (Cliente/Visualizador)
    st.image("assets/Lhg-01.webp", width=250)
    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background-color: #FFFFFF; padding: 16px; border-radius: 12px; border: 1px solid #EBEBEB; border-left: 4px solid #FF5A00; margin-bottom: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.02);">
        <p style="margin: 0 0 8px 0; font-family: 'Outfit', sans-serif; font-weight: 700; color: #111; font-size: 14px; letter-spacing: 0.5px;">📊 STATUS DO SISTEMA</p>
        <p style="margin: 0; font-size: 12px; color: #666; line-height: 1.5;">
            Conectado à <b>Base de Dados LHG</b>.<br>
            Os dados são atualizados automaticamente a partir do repositório central.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background-color: #FFFFFF; padding: 16px; border-radius: 12px; border: 1px solid #EBEBEB; border-left: 4px solid #4A7045; margin-bottom: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.02);">
        <p style="margin: 0 0 8px 0; font-family: 'Outfit', sans-serif; font-weight: 700; color: #111; font-size: 14px; letter-spacing: 0.5px;">📰 INTELIGÊNCIA ATIVA</p>
        <p style="margin: 0; font-size: 12px; color: #666; line-height: 1.5;">
            Monitoramento de mídia e clipping em tempo real integrado.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Rodapé da Sidebar - 80 20 Marketing
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
        <div style="padding: 20px; border-top: 1px solid #EBEBEB; margin-top: 20px; text-align: center;">
    """, unsafe_allow_html=True)
    st.image("assets/Logo-80-20-Marketing_preta.png", width=120)
    st.markdown("</div>", unsafe_allow_html=True)

with st.spinner("Estruturando matriz de dados..."):
    df_kpi = carregar_dados_kpi(PATH_KPI)
    df_relatorio = carregar_dados_relatorio(PATH_RELATORIO)

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

# --- Header Dinâmico ---
st.markdown("""
<div style="margin-bottom: 30px;">
    <h1 style="margin-bottom: 5px; font-size: 2.2rem;">Monitoramento Estratégico</h1>
    <p style="color: #666; font-size: 1.1rem; margin: 0;">Visão consolidada de inteligência de mercado e saúde da marca (Dados a partir de 2025).</p>
</div>
""", unsafe_allow_html=True)

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
                    {disp_delta} em relação ao ciclo anterior
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
            st.markdown("<h3 style='font-size: 1.2rem; margin-bottom: 20px;'>EVOLUÇÃO DO ÍNDICE DE SAÚDE DA MARCA</h3>", unsafe_allow_html=True)
            fig_saude = px.line(
                df_kpi, x=x_col_kpi, y=col_saude_plot, 
                template=PLOTLY_TEMPLATE,
                color_discrete_sequence=['#FF5A00'],
                markers=True
            )
            fig_saude.update_traces(
                fill='tozeroy', 
                fillcolor='rgba(255, 90, 0, 0.15)', 
                line=dict(width=5, shape='spline'),
                marker=dict(size=10, color='#FF5A00', line=dict(width=3, color='#FFFFFF')),
                hovertemplate="<b>Período:</b> %{x}<br><b>Saúde:</b> %{y:.1f}%<extra></extra>"
            )
            fig_saude.update_layout(
                **plotly_layout_defaults,
                hoverlabel=dict(bgcolor="white", font_size=14, font_family="Outfit")
            )
            fig_saude.update_yaxes(rangemode="tozero")
            st.plotly_chart(fig_saude, use_container_width=True, config={'displayModeBar': False}, theme=None)
            
        # 3. Empilhamento de Sentimentos
        cols_sent = [c for c in [col_positivo, col_neutro, col_negativo] if c]
        if cols_sent:
            st.markdown("<h3 style='font-size: 1.2rem; margin-bottom: 20px; margin-top: 20px;'>COMPOSIÇÃO DE IMPACTO POR CICLO</h3>", unsafe_allow_html=True)
            df_melt = df_kpi.melt(id_vars=[x_col_kpi], value_vars=cols_sent, var_name="Sentimento", value_name="Quantidade")
            fig_stack = px.bar(
                df_melt, x=x_col_kpi, y="Quantidade", color="Sentimento",
                template=PLOTLY_TEMPLATE,
                color_discrete_map=COLOR_MAP
            )
            fig_stack.update_traces(marker_line_width=1, marker_line_color='#FFFFFF')
            fig_stack.update_layout(
                **plotly_layout_defaults,
                barmode='stack',
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5, title=""),
                hoverlabel=dict(bgcolor="white", font_family="Outfit")
            )
            st.plotly_chart(fig_stack, use_container_width=True, config={'displayModeBar': False}, theme=None)
            
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
            st.markdown("<h3 style='font-size: 1.2rem; margin-bottom: 20px;'>PROPORÇÃO GLOBAL DE MÍDIA</h3>", unsafe_allow_html=True)
            cont_sent = df_news_plot[col_sentimento_news].value_counts().reset_index()
            cont_sent.columns = ['Sentimento', 'Volume']
            fig_pie = px.pie(
                cont_sent, names='Sentimento', values='Volume', 
                color='Sentimento', color_discrete_map=COLOR_MAP,
                template=PLOTLY_TEMPLATE, hole=0.7
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent', marker=dict(line=dict(color='#FFFFFF', width=2)))
            fig_pie.update_layout(
                **plotly_layout_defaults, 
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5, title="Legenda de Sentimentos:"),
                hoverlabel=dict(bgcolor="white", font_family="Outfit")
            )
            st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False}, theme=None)
        
        with c2:
            if col_portal_news:
                st.markdown("<h3 style='font-size: 1.2rem; margin-bottom: 20px;'>TOP VEÍCULOS IMPRESSA / PORTAIS</h3>", unsafe_allow_html=True)
                df_portais = df_news_plot.groupby([col_portal_news, col_sentimento_news]).size().reset_index(name='Quantidade')
                top_portais = df_news_plot[col_portal_news].value_counts().nlargest(8).index
                df_portais_top = df_portais[df_portais[col_portal_news].isin(top_portais)]
                
                fig_portal = px.bar(
                    df_portais_top, y=col_portal_news, x='Quantidade', color=col_sentimento_news,
                    orientation='h', template=PLOTLY_TEMPLATE, color_discrete_map=COLOR_MAP
                )
                fig_portal.update_layout(
                    **plotly_layout_defaults,
                    showlegend=True,
                    legend=dict(title="Sentimento:", orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5),
                    hoverlabel=dict(bgcolor="white", font_family="Outfit")
                )
                fig_portal.update_yaxes(categoryorder='total ascending')
                fig_portal.update_traces(marker_line_width=1, marker_line_color='#FFFFFF')
                st.plotly_chart(fig_portal, use_container_width=True, config={'displayModeBar': False}, theme=None)
        
        st.markdown("<hr style='margin: 40px 0;'>", unsafe_allow_html=True)
        
        if col_data_news:
            try:
                st.markdown("<h3 style='font-size: 1.2rem; margin-bottom: 20px;'>TENDÊNCIA TEMPORAL (VOLUME DE NOTÍCIAS)</h3>", unsafe_allow_html=True)
                df_news_plot[col_data_news] = pd.to_datetime(df_news_plot[col_data_news], dayfirst=True)
                df_tempo = df_news_plot.groupby([pd.Grouper(key=col_data_news, freq='W-MON'), col_sentimento_news]).size().reset_index(name='Quantidade')
                fig_time = px.line(
                    df_tempo, x=col_data_news, y='Quantidade', color=col_sentimento_news,
                    template=PLOTLY_TEMPLATE, color_discrete_map=COLOR_MAP, markers=True
                )
                fig_time.update_traces(line=dict(width=4, shape='spline'), marker=dict(size=10, line=dict(width=2, color='#FFFFFF')))
                fig_time.update_layout(
                    **plotly_layout_defaults,
                    showlegend=True,
                    legend=dict(title="Sentimento:", orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5),
                    hoverlabel=dict(bgcolor="white", font_family="Outfit")
                )
                fig_time.update_yaxes(rangemode="tozero")
                st.plotly_chart(fig_time, use_container_width=True, config={'displayModeBar': False}, theme=None)
            except:
                pass
    else:
        st.info("A coluna Sentimento não foi identificada nas Notícias.")

# ====== ABA 3: FEED VISUAL DE EVENTOS ======
with tab_feed:
    st.markdown("<br>", unsafe_allow_html=True)
    col_titulo_news = cols_rel_lower.get('título') or cols_rel_lower.get('titulo')
    col_link_news = cols_rel_lower.get('link') or cols_rel_lower.get('url')
    
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
<div class="news-card-premium">
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
        <a href="{link_url}" target="_blank" class="news-action" style="{link_display}">Ler matéria completa →</a>
    </div>
</div>
"""
            
        cards_html += "</div>"
        st.markdown(cards_html, unsafe_allow_html=True)
        st.markdown("<br><br>", unsafe_allow_html=True)
    else:
        st.warning("Colunas Título/Data ausentes na planilha de Notícias.")
