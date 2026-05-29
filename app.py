import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import os

# Base path of 'producao/' folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

from config.settings import PATH_KPI, GOOGLE_SHEET_ID, GOOGLE_SHEET_ID_SAUDE, plotly_layout_defaults, PLOTLY_TEMPLATE, COLOR_MAP
from config.style import apply_custom_style
from data.loader import carregar_dados_kpi, carregar_dados_relatorio_sheets, carregar_dados_saude_marca_sheets, carregar_dados_relatorio
from utils.pdf_export import gerar_pdf_completo
from views.sidebar import render_sidebar
from views.tab_metrics import render_metrics_tab
from views.tab_media import render_media_tab
from views.tab_feed import render_feed_tab

try:
    from fpdf import FPDF
    HAS_FPDF = True
except ImportError:
    HAS_FPDF = False

# --- Configuração da Página ---
st.set_page_config(
    page_title="LHG Mining",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Aplicar Estilo Customizado ---
apply_custom_style()

# --- Interface Principal ---
render_sidebar()

with st.spinner("Estruturando matriz de dados..."):
    # Carregando dados do Google Sheets usando Streamlit Secrets (sem JSON local)
    df_kpi = carregar_dados_saude_marca_sheets(GOOGLE_SHEET_ID_SAUDE, "DADOS")
    
    if isinstance(df_kpi, str) and "Erro" in df_kpi:
        st.warning(f"Conexão com Google Sheets (Saúde de Marca) falhou: {df_kpi}. Carregando arquivo local de backup...")
        df_kpi = carregar_dados_kpi(PATH_KPI)

    df_relatorio = carregar_dados_relatorio_sheets(GOOGLE_SHEET_ID, "Dados")
    
    if isinstance(df_relatorio, str) and "Erro ao acessar Google Sheets" in df_relatorio:
        st.warning("Conexão com Google Sheets (Relatório) falhou. Tentando carregar arquivo local de backup...")
        df_relatorio = carregar_dados_relatorio(os.path.join(BASE_DIR, 'dados-exemplo', 'dados-lhg.xlsx'))

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

# --- Header Dinâmico e Filtro ---
head_col1, head_col2, head_col3 = st.columns([2.5, 0.8, 1])

import base64

with head_col1:
    lhg_b64 = ""
    try:
        img_path = os.path.join(BASE_DIR, "assets", "Lhg-01.webp")
        with open(img_path, "rb") as img_file:
            lhg_b64 = base64.b64encode(img_file.read()).decode()
        img_html = f'<img src="data:image/webp;base64,{lhg_b64}" width="180">'
    except Exception:
        img_html = ""
        
    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 24px; margin-bottom: 32px;">
        {img_html}
        <div style="border-left: 4px solid #FF6600; padding-left: 24px;">
            <h1 style="margin-bottom: 8px; font-size: 2.2rem; color: #0F172A !important; font-weight: 800; letter-spacing: -0.025em;">Monitoramento Estratégico</h1>
            <p style="color: #64748B; font-size: 1rem; margin: 0; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 500;">Consolidado de Inteligência Industrial | LHG Mining</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with head_col2:
    st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)
    if x_col_kpi:
        opcoes_data = ["Todos"] + list(df_kpi[x_col_kpi].unique())
        data_selecionada = st.selectbox("Mês de Referência", opcoes_data, index=0)
    else:
        data_selecionada = "Todos"

# --- Filtro Temporal Global ---
if data_selecionada != "Todos":
    df_kpi = df_kpi[df_kpi[x_col_kpi] == data_selecionada]
    
    if col_data_news:
        try:
            ano_sel, mes_sel = data_selecionada.split('/')
            df_rel_dt = pd.to_datetime(df_relatorio[col_data_news], dayfirst=True, errors='coerce')
            mask = (df_rel_dt.dt.year == int(ano_sel)) & (df_rel_dt.dt.month == int(mes_sel))
            df_relatorio = df_relatorio[mask]
        except Exception as e:
            pass

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

    if col_saude:
        fig_saude = go.Figure()
        fig_saude.add_trace(go.Scatter(
            x=df_kpi[x_col_kpi], y=df_kpi[col_saude_plot],
            mode='lines+markers+text', 
            line=dict(color='#FF6600', width=4, shape='spline', smoothing=1.3),
            marker=dict(size=14, color='#FF6600', line=dict(width=3, color='#FFFFFF'), symbol='circle'),
            text=df_kpi[col_saude_plot].apply(lambda x: f"{x}%"),
            textposition="top center",
            textfont=dict(size=11, color="#2C3E50", family="Outfit"),
            fill='tozeroy', fillcolor='rgba(255,102,0,0.08)', name='Saúde da Marca'
        ))
        fig_saude.update_layout(**plotly_layout_defaults, title_text='EVOLUÇÃO DO ÍNDICE DE SAÚDE DA MARCA', showlegend=True)
        figs_para_pdf['saude'] = fig_saude

    cols_sent = [c for c in [col_positivo, col_neutro, col_negativo] if c]
    if cols_sent:
        df_melt = df_kpi.melt(id_vars=[x_col_kpi], value_vars=cols_sent, var_name="Sentimento", value_name="Quantidade")
        COLOR_MAP_STACK = {'Positivo': '#00A86B', 'Neutro': '#8E9BB0', 'Negativo': '#E04F5F'}
        fig_stack = px.bar(df_melt, x=x_col_kpi, y="Quantidade", color="Sentimento", 
                           template=PLOTLY_TEMPLATE, color_discrete_map=COLOR_MAP_STACK,
                           text="Quantidade")
        fig_stack.update_layout(**plotly_layout_defaults, title_text='COMPOSIÇÃO DE IMPACTO POR CICLO', barmode='stack', showlegend=True)
        fig_stack.update_traces(
            textposition='inside', 
            marker_line_width=0, 
            marker_cornerradius=4,
            textfont=dict(size=11, family="Inter", color="#FFFFFF", weight="bold")
        )
        figs_para_pdf['stack'] = fig_stack

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
    fig_pie.update_traces(textfont=dict(size=13, color='#334155'), marker=dict(line=dict(color='#FFFFFF', width=3)))
    fig_pie.update_layout(**plotly_layout_defaults, title_text='PROPORÇÃO GLOBAL DE MÍDIA', showlegend=True, legend_orientation='h', legend_yanchor='bottom', legend_y=-0.2, legend_xanchor='center', legend_x=0.5)
    figs_para_pdf['pie'] = fig_pie

    if col_portal_news:
        df_portais = df_news_plot.groupby([col_portal_news, col_sentimento_news]).size().reset_index(name='Quantidade')
        top_portais = df_news_plot[col_portal_news].value_counts().nlargest(8).index
        df_portais_top = df_portais[df_portais[col_portal_news].isin(top_portais)]
        fig_portal = px.bar(df_portais_top, y=col_portal_news, x='Quantidade', color=col_sentimento_news, orientation='h', template=PLOTLY_TEMPLATE, color_discrete_map=COLOR_MAP, text='Quantidade')
        fig_portal.update_traces(
            marker_line_width=0, 
            marker_cornerradius=4,
            textposition='inside',
            textfont=dict(size=11, family="Inter", color="#FFFFFF", weight="bold")
        )
        fig_portal.update_layout(
            **plotly_layout_defaults, 
            title_text='TOP VEÍCULOS / PORTAIS', 
            showlegend=True
        )
        fig_portal.update_layout(
            legend=dict(orientation="h", yanchor="top", y=-0.2, xanchor="center", x=0.5)
        )
        figs_para_pdf['portal'] = fig_portal

    if col_data_news:
        try:
            df_news_plot[col_data_news] = pd.to_datetime(df_news_plot[col_data_news], dayfirst=True)
            df_tempo = df_news_plot.groupby([pd.Grouper(key=col_data_news, freq='MS'), col_sentimento_news]).size().reset_index(name='Quantidade')
            fig_time = px.line(df_tempo, x=col_data_news, y='Quantidade', color=col_sentimento_news, template=PLOTLY_TEMPLATE, color_discrete_map=COLOR_MAP, markers=True, text='Quantidade')
            fig_time.update_traces(
                line=dict(width=3, shape='spline', smoothing=1.3),
                marker=dict(size=10, line=dict(width=2, color='#FFFFFF')),
                textposition='top center',
                textfont=dict(size=11, family="Inter", color="#475569", weight="bold")
            )
            fig_time.update_layout(
                **plotly_layout_defaults, 
                title_text='TENDÊNCIA TEMPORAL (VOLUME DE NOTÍCIAS)', 
                showlegend=True
            )
            fig_time.update_layout(
                legend=dict(orientation="h", yanchor="top", y=-0.25, xanchor="center", x=0.5)
            )
            fig_time.update_yaxes(rangemode='tozero')
            figs_para_pdf['time'] = fig_time
        except: pass

# --- Botão de Exportação PDF ---
with head_col3:
    st.markdown("<div style='margin-top: 52px;'></div>", unsafe_allow_html=True)
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

with tab_dados:
    if x_col_kpi and not df_kpi.empty:
        render_metrics_tab(df_kpi, x_col_kpi, col_saude, col_saude_plot, disp_atual, disp_delta, delta_class, total_itens, total_pos, total_neg, col_positivo, col_neutro, col_negativo)
    elif not x_col_kpi:
        st.warning("Falha ao localizar coluna de Tempo na aba DADOS.")
    else:
        st.info("A base resultou vazia após o filtro (>2024). Insira dados atualizados.")

with tab_news:
    render_media_tab(df_relatorio, col_sentimento_news, col_portal_news, col_data_news)

with tab_feed:
    render_feed_tab(df_relatorio, col_data_news, col_titulo_news, col_sentimento_news, col_portal_news, col_link_news)
