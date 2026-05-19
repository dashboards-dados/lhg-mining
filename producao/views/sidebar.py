import streamlit as st
import base64
import os

# Base path of 'producao/' folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def render_sidebar():
    with st.sidebar:
        img_path = os.path.join(BASE_DIR, "assets", "Lhg-01.webp")
        st.image(img_path, width=250)
        st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: #FFFFFF; padding: 20px; border-radius: 12px; border: 1px solid #F1F5F9; border-left: 4px solid #FF6600; margin-bottom: 16px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03), 0 2px 4px -1px rgba(0, 0, 0, 0.02);">
            <p style="margin: 0 0 10px 0; font-family: 'Outfit', sans-serif; font-weight: 700; color: #0F172A; font-size: 13px; letter-spacing: 0.05em; text-transform: uppercase;">📊 Status do Sistema</p>
            <p style="margin: 0; font-size: 13px; color: #475569; line-height: 1.6; font-family: 'Inter', sans-serif;">
                Conectado à <b>Base de Dados LHG</b>.<br>
                Monitoramento industrial ativo.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: #FFFFFF; padding: 20px; border-radius: 12px; border: 1px solid #F1F5F9; border-left: 4px solid #10B981; margin-bottom: 16px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03), 0 2px 4px -1px rgba(0, 0, 0, 0.02);">
            <p style="margin: 0 0 10px 0; font-family: 'Outfit', sans-serif; font-weight: 700; color: #0F172A; font-size: 13px; letter-spacing: 0.05em; text-transform: uppercase;">📰 Inteligência Ativa</p>
            <p style="margin: 0; font-size: 13px; color: #475569; line-height: 1.6; font-family: 'Inter', sans-serif;">
                Clipping em tempo real integrado.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br><br><br>", unsafe_allow_html=True)
        try:
            logo_path = os.path.join(BASE_DIR, "assets", "Logo-80-20-Marketing_preta.png")
            with open(logo_path, "rb") as f:
                img_data = base64.b64encode(f.read()).decode()
            st.markdown(f"""
                <div style="padding: 20px; text-align: center; opacity: 0.8; transition: opacity 0.3s ease;" onmouseover="this.style.opacity=1" onmouseout="this.style.opacity=0.8">
                    <p style="font-size: 11px; color: #94A3B8; font-family: 'Inter', sans-serif; margin-bottom: 10px; font-weight: 600; letter-spacing: 0.05em;">DESENVOLVIDO POR</p>
                    <img src="data:image/png;base64,{img_data}" width="130" style="filter: drop-shadow(0px 2px 4px rgba(0,0,0,0.05));">
                </div>
            """, unsafe_allow_html=True)
        except:
            pass
