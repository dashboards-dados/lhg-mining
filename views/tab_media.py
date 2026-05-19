import streamlit as st
import plotly.express as px
import pandas as pd
from config.settings import plotly_layout_defaults, PLOTLY_TEMPLATE, COLOR_MAP

def render_media_tab(df_relatorio, col_sentimento_news, col_portal_news, col_data_news):
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
            st.markdown("<h3 style='font-size: 1.1rem; margin-bottom: 24px; color:#0F172A; letter-spacing:-0.025em; font-weight:700;'>Proporção Global de Mídia</h3>", unsafe_allow_html=True)
            cont_sent = df_news_plot[col_sentimento_news].value_counts().reset_index()
            cont_sent.columns = ['Sentimento', 'Volume']
            fig_pie = px.pie(
                cont_sent, names='Sentimento', values='Volume',
                color='Sentimento', color_discrete_map=COLOR_MAP,
                template=PLOTLY_TEMPLATE, hole=0.65
            )
            fig_pie.update_traces(
                textposition='outside', textinfo='percent+label',
                textfont=dict(size=13, color='#334155', family='Inter', weight="bold"),
                marker=dict(line=dict(color='#FFFFFF', width=3)),
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
                st.markdown("<h3 style='font-size: 1.1rem; margin-bottom: 24px; color:#0F172A; letter-spacing:-0.025em; font-weight:700;'>Top Veículos / Portais</h3>", unsafe_allow_html=True)
                df_portais = df_news_plot.groupby([col_portal_news, col_sentimento_news]).size().reset_index(name='Quantidade')
                top_portais = df_news_plot[col_portal_news].value_counts().nlargest(8).index
                df_portais_top = df_portais[df_portais[col_portal_news].isin(top_portais)]
                fig_portal = px.bar(
                    df_portais_top, y=col_portal_news, x='Quantidade', color=col_sentimento_news,
                    orientation='h', template=PLOTLY_TEMPLATE, color_discrete_map=COLOR_MAP,
                    text='Quantidade'
                )
                fig_portal.update_layout(
                    **plotly_layout_defaults,
                    showlegend=True
                )
                fig_portal.update_layout(
                    legend=dict(orientation="h", yanchor="top", y=-0.25, xanchor="center", x=0.5)
                )
                fig_portal.update_yaxes(categoryorder='total ascending', title="", tickfont=dict(size=12, color="#475569"))
                fig_portal.update_traces(
                    marker_line_width=0, 
                    opacity=0.9, 
                    hovertemplate="<b>%{y}</b><br>%{color}: %{x}<extra></extra>", 
                    marker_cornerradius=4,
                    textposition='inside',
                    textfont=dict(size=11, family="Inter", color="#FFFFFF", weight="bold")
                )
                st.plotly_chart(fig_portal, use_container_width=True, config={'displayModeBar': False}, theme=None)
        
        st.markdown("<hr style='margin: 40px 0; border: none; height: 1px; background: linear-gradient(90deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0.05) 50%, rgba(0,0,0,0) 100%);'>", unsafe_allow_html=True)
        
        if col_data_news:
            try:
                st.markdown("<h3 style='font-size: 1.1rem; margin-bottom: 24px; color:#0F172A; letter-spacing:-0.025em; font-weight:700;'>Tendência Temporal (Volume de Notícias)</h3>", unsafe_allow_html=True)
                df_news_plot[col_data_news] = pd.to_datetime(df_news_plot[col_data_news], dayfirst=True)
                df_tempo = df_news_plot.groupby([pd.Grouper(key=col_data_news, freq='MS'), col_sentimento_news]).size().reset_index(name='Quantidade')
                fig_time = px.line(
                    df_tempo, x=col_data_news, y='Quantidade', color=col_sentimento_news,
                    template=PLOTLY_TEMPLATE, color_discrete_map=COLOR_MAP, markers=True,
                    text='Quantidade'
                )
                fig_time.update_traces(
                    line=dict(width=3, shape='spline', smoothing=1.3),
                    marker=dict(size=10, line=dict(width=2, color='#FFFFFF'), symbol='circle'),
                    opacity=0.9,
                    hovertemplate="<b>Data:</b> %{x}<br><b>Volume:</b> %{y}<extra></extra>",
                    textposition='top center',
                    textfont=dict(size=11, family="Inter", color="#475569", weight="bold")
                )
                fig_time.update_layout(
                    **plotly_layout_defaults,
                    showlegend=True
                )
                fig_time.update_layout(
                    legend=dict(orientation="h", yanchor="top", y=-0.25, xanchor="center", x=0.5)
                )
                fig_time.update_yaxes(rangemode='tozero', zeroline=True, zerolinecolor='#F1F5F9', title="")
                fig_time.update_xaxes(title="")
                st.plotly_chart(fig_time, use_container_width=True, config={'displayModeBar': False}, theme=None)
            except:
                pass
    else:
        st.info("A coluna Sentimento não foi identificada nas Notícias.")
