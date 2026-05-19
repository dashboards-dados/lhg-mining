import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from config.settings import plotly_layout_defaults, PLOTLY_TEMPLATE, COLOR_MAP

def render_metrics_tab(df_kpi, x_col_kpi, col_saude, col_saude_plot, disp_atual, disp_delta, delta_class, total_itens, total_pos, total_neg, col_positivo, col_neutro, col_negativo):
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
        st.markdown("<h3 style='font-size: 1.1rem; margin-bottom: 24px; color:#0F172A; letter-spacing:-0.025em; font-weight:700;'>Evolução do Índice de Saúde da Marca</h3>", unsafe_allow_html=True)
        fig_saude = go.Figure()
        fig_saude.add_trace(go.Scatter(
            x=df_kpi[x_col_kpi], y=df_kpi[col_saude_plot],
            mode='lines+markers+text',
            line=dict(color='#FF6600', width=4, shape='spline', smoothing=1.3),
            marker=dict(size=14, color='#FFFFFF', line=dict(width=3, color='#FF6600'), symbol='circle'),
            text=df_kpi[col_saude_plot].apply(lambda x: f"<b>{x}%</b>"),
            textposition="top center",
            textfont=dict(size=13, color="#FF6600", family="Inter", weight="bold"),
            fill='tozeroy',
            fillcolor='rgba(255, 102, 0, 0.08)',
            hovertemplate="<b>Período:</b> %{x}<br><b>Saúde:</b> %{y:.1f}%<extra></extra>",
            name='Saúde da Marca'
        ))
        fig_saude.update_layout(
            **plotly_layout_defaults,
            showlegend=False
        )
        fig_saude.update_yaxes(rangemode='tozero', ticksuffix='%')
        st.plotly_chart(fig_saude, use_container_width=True, config={'displayModeBar': False}, theme=None)
        
    # 3. Empilhamento de Sentimentos
    cols_sent = [c for c in [col_positivo, col_neutro, col_negativo] if c]
    if cols_sent:
        st.markdown("<h3 style='font-size: 1.1rem; margin-bottom: 24px; margin-top: 32px; color:#0F172A; letter-spacing:-0.025em; font-weight:700;'>Composição de Impacto por Ciclo</h3>", unsafe_allow_html=True)
        df_melt = df_kpi.melt(id_vars=[x_col_kpi], value_vars=cols_sent, var_name="Sentimento", value_name="Quantidade")
        
        # Mapping for the stack chart specifically
        COLOR_MAP_STACK = {'Positivo': '#00A86B', 'Neutro': '#8E9BB0', 'Negativo': '#E04F5F'}
        
        fig_stack = px.bar(
            df_melt, x=x_col_kpi, y="Quantidade", color="Sentimento",
            template=PLOTLY_TEMPLATE,
            color_discrete_map=COLOR_MAP_STACK,
            text="Quantidade"
        )
        fig_stack.update_layout(
            **plotly_layout_defaults,
            barmode='stack'
        )
        fig_stack.update_traces(
            marker_line_width=0, 
            opacity=0.9, 
            hovertemplate="<b>%{x}</b><br>%{color}: %{y}<extra></extra>",
            marker_cornerradius=4,
            textposition='inside',
            textfont=dict(size=11, family="Inter", color="#FFFFFF", weight="bold")
        )
        st.plotly_chart(fig_stack, use_container_width=True, config={'displayModeBar': False}, theme=None)
