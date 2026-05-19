import streamlit as st
import pandas as pd
import html

def render_feed_tab(df_relatorio, col_data_news, col_titulo_news, col_sentimento_news, col_portal_news, col_link_news):
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
            sentiment_class = "neu"
            if 'pos' in sent_val_str:
                sentimento = 'Positivo'
                badge_class = "badge-pos"
                sentiment_class = "pos"
            elif 'neg' in sent_val_str:
                sentimento = 'Negativo'
                badge_class = "badge-neg"
                sentiment_class = "neg"
            else:
                sentimento = 'Neutro'
                badge_class = "badge-neu"
                sentiment_class = "neu"
                
            portal_info = f"{row[col_portal_news]}" if col_portal_news and pd.notna(row[col_portal_news]) else "Veículo não informado"
            link_url = row[col_link_news] if col_link_news and pd.notna(row[col_link_news]) else "#"
            link_display = "display: inline-block;" if link_url != "#" else "display: none;"
            
            cards_html += f"""
<div class="news-card-premium">
    <!-- Barra lateral de sentimento com cantos arredondados externos -->
    <div class="news-card-sentiment-bar {sentiment_class}"></div>
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
        <div style="margin-top: 14px; {link_display}">
            <a href="{link_url}" target="_blank" class="news-action">VER MATÉRIA ORIGINAL</a>
        </div>
    </div>
</div>
"""
            
        cards_html += "</div>"
        st.markdown(cards_html, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("<br><br>", unsafe_allow_html=True)
    else:
        st.warning("Colunas Título/Data ausentes na planilha de Notícias.")
