import streamlit as st
from datetime import datetime
import pandas as pd
import os

# Base path of 'producao/' folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def gerar_pdf_completo(df_kpi, df_news, _figs_dict, kpi_data):
    from fpdf import FPDF
    import tempfile
    import os
    
    cols_rel_lower = {str(c).lower(): c for c in df_news.columns}
    col_sentimento_news = cols_rel_lower.get('sentimento')
    col_portal_news = cols_rel_lower.get('portal') or cols_rel_lower.get('veículo')
    col_titulo_news = cols_rel_lower.get('título') or cols_rel_lower.get('titulo')
    col_link_news = cols_rel_lower.get('link') or cols_rel_lower.get('url')
    col_data_news = cols_rel_lower.get('data') or cols_rel_lower.get('data da notícia') or cols_rel_lower.get('data noticia')

    class LHGPDF(FPDF):
        current_section = ""
        is_cover = True
        
        def header(self):
            # 1. Background color for all pages: #F8FAFC (Ultra-light Slate)
            self.set_fill_color(248, 250, 252)
            self.rect(0, 0, 210, 297, 'F')
            
            if self.is_cover or not self.current_section:
                return
                
            # 2. Modern section divider
            self.set_font("Helvetica", 'B', 12)
            self.set_text_color(15, 23, 42) # #0F172A (Texto Principal)
            self.set_xy(25, 15)
            self.cell(100, 10, self.current_section.upper())
            
            try:
                img_path = os.path.join(BASE_DIR, "assets", "Lhg-01.webp")
                self.image(img_path, x=160, y=13, w=25)
            except:
                pass
                
            # Line horizontal inferior (Orange accent instead of grey for a touch of brand)
            self.set_draw_color(255, 102, 0)
            self.set_line_width(0.6)
            self.line(25, 26, 185, 26)
            
            self.set_y(35)

        def footer(self):
            if not self.is_cover:
                # Thin horizontal line separating the content from the footer
                self.set_draw_color(226, 232, 240)
                self.set_line_width(0.4)
                self.line(25, 282, 185, 282)
                
                self.set_y(-14)
                self.set_font("Helvetica", "", 8)
                self.set_text_color(100, 116, 139) # #64748B (Texto Secundário)
                
                # Left side text
                self.set_x(25)
                self.cell(100, 10, "LHG Mining | Inteligência Estratégica", align="L")
                
                # Right side pagination
                self.set_x(140)
                self.cell(45, 10, f"Página {self.page_no()} de {{nb}}", align="R")

    def check_space(pdf, required_h):
        if pdf.get_y() + required_h > 270:
            pdf.add_page()

    pdf = LHGPDF()
    pdf.alias_nb_pages()
    pdf.set_margins(25, 25, 25)
    pdf.set_auto_page_break(auto=True, margin=25)
    
    # --- Capa (Página 1) - Redesenho Total ---
    pdf.add_page()
    
    # 1. Background color: #F8FAFC
    pdf.set_fill_color(248, 250, 252)
    pdf.rect(0, 0, 210, 297, 'F')
    
    # Topo: Nome da empresa LHG MINING spaced out
    pdf.set_y(55)
    pdf.set_font("Helvetica", 'B', 12)
    pdf.set_text_color(100, 116, 139) # #64748B
    pdf.cell(0, 10, "M O N I T O R A M E N T O   E S T R A T É G I C O", align="C", new_x="LMARGIN", new_y="NEXT")
    
    # Centro: Título principal
    pdf.set_y(110)
    pdf.set_font("Helvetica", 'B', 26)
    pdf.set_text_color(15, 23, 42) # #0F172A
    pdf.cell(0, 15, "CONSOLIDADO DE INTELIGÊNCIA", align="C", new_x="LMARGIN", new_y="NEXT")
    
    pdf.ln(3)
    pdf.set_font("Helvetica", '', 13)
    pdf.set_text_color(100, 116, 139) # #64748B
    pdf.cell(0, 10, "LHG Mining | Inteligência Industrial", align="C", new_x="LMARGIN", new_y="NEXT")
    
    # Thin orange accent line: #FF6600
    pdf.set_fill_color(255, 102, 0)
    pdf.rect(85, 146, 40, 2.5, 'F')
    
    # Rodapé: Data e hora centralizadas
    pdf.set_font("Helvetica", 'I', 9.5)
    pdf.set_text_color(100, 116, 139)
    pdf.set_xy(25, 235)
    pdf.cell(160, 10, f"Gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M')}", align="C")
    
    # Logo da agência centralizado no terço inferior
    try:
        logo_path = os.path.join(BASE_DIR, "assets", "Logo-80-20-Marketing_preta.png")
        pdf.image(logo_path, x=85, y=180, w=40)
    except:
        pass
        
    pdf.is_cover = False

    # --- Página 2: Indicadores ---
    pdf.current_section = "1. Indicadores de Performance (KPIs)"
    pdf.add_page()
    
    # Render KPI Cards
    col_w = 75
    card_h = 24
    y_start_kpi = pdf.get_y()
    for i, (label, value) in enumerate(kpi_data):
        x = 25 + (i % 2) * (col_w + 10)
        row = i // 2
        curr_y = y_start_kpi + (row * (card_h + 6))
        
        pdf.set_xy(x, curr_y)
        
        # White card body with rounded corners
        pdf.set_fill_color(255, 255, 255)
        pdf.set_draw_color(226, 232, 240)
        pdf.set_line_width(0.15)
        pdf.rect(x, curr_y, col_w, card_h, style='DF', round_corners=True, corner_radius=2.5)
        
        # Left Accent Strip (rounded on external edges)
        if 'SAUDE' in label.upper() or 'SAÚDE' in label.upper():
            accent_color = (255, 102, 0) # Laranja LHG
        elif 'TOTAL' in label.upper():
            accent_color = (100, 116, 139) # Slate 500
        elif 'POSITIVA' in label.upper():
            accent_color = (0, 168, 107)
        elif 'NEGATIVA' in label.upper():
            accent_color = (224, 79, 95)
        else:
            accent_color = (142, 155, 176)
            
        pdf.set_fill_color(*accent_color)
        pdf.rect(x, curr_y, 1.5, card_h, style='F', round_corners=('TOP_LEFT', 'BOTTOM_LEFT'), corner_radius=1.5)
        
        # Text alignment
        pdf.set_text_color(100, 116, 139) # #64748B
        pdf.set_font("Helvetica", 'B', 8)
        pdf.set_xy(x + 3, curr_y + 4)
        pdf.cell(col_w - 3, 4, label.upper(), align="C")
        
        pdf.set_text_color(15, 23, 42) # #0F172A
        pdf.set_font("Helvetica", 'B', 15)
        pdf.set_xy(x + 3, curr_y + 11)
        pdf.cell(col_w - 3, 8, str(value), align="C")
    
    pdf.set_y(y_start_kpi + 62)
    
    # Charts for KPIs
    for fig_key in ['saude', 'stack']:
        if fig_key in _figs_dict:
            check_space(pdf, 85)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
                _figs_dict[fig_key].write_image(tmpfile.name, width=1000, height=450, scale=1.5)
                pdf.image(tmpfile.name, x=25, w=160)
                os.unlink(tmpfile.name)
            pdf.ln(5)
            
    # --- Página 3: Análise de Mídia ---
    pdf.current_section = "2. Análise de Exposição e Sentimento"
    pdf.add_page()
    
    for fig_key in ['pie', 'portal', 'time']:
        if fig_key in _figs_dict:
            check_space(pdf, 85)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
                h_img = 480 if fig_key == 'pie' else 550
                _figs_dict[fig_key].write_image(tmpfile.name, width=1000, height=h_img, scale=1.5)
                w_img = 130 if fig_key == 'pie' else 160
                x_img = 40 if fig_key == 'pie' else 25
                pdf.image(tmpfile.name, x=x_img, w=w_img)
                os.unlink(tmpfile.name)
            pdf.ln(10)
            
    # --- Página 4: Radar de Eventos ---
    pdf.current_section = "3. Radar de Eventos (Últimas Matérias)"
    pdf.add_page()
    
    pdf.set_font("Helvetica", '', 9.5)
    pdf.set_text_color(100, 116, 139) # #64748B
    pdf.cell(0, 5, "Listagem consolidada das publicações mais recentes capturadas pelo sistema.", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)
    
    for _, row in df_news.head(30).iterrows():
        titulo = str(row.get(col_titulo_news, 'Sem título'))[:180]
        link = row.get(col_link_news)
        has_link = pd.notna(link) and str(link).startswith('http')
        
        # Try to parse date
        try:
            if isinstance(row.get(col_data_news), pd.Timestamp):
                data_str = row.get(col_data_news).strftime('%d/%m/%Y')
            else:
                data_str = str(row.get(col_data_news)).split(' ')[0]
        except:
            data_str = str(row.get(col_data_news))
            
        portal = str(row.get(col_portal_news, 'N/A')).upper()
        header_text = f"{portal}  |  {data_str}"
        
        # Safe dynamic height estimation
        lines = max(1, len(titulo) // 80)
        title_h = lines * 5
        card_h = 5 + 4 + 2 + title_h + (12.5 if has_link else 6)
            
        check_space(pdf, card_h + 8)
        
        curr_y = pdf.get_y()
        card_w = 160
        
        # Sentiment-based color coding
        sent = str(row.get(col_sentimento_news, 'Neutro')).lower()
        if 'pos' in sent: 
            accent_color = (0, 168, 107) # #00A86B (Verde)
        elif 'neg' in sent: 
            accent_color = (224, 79, 95) # #E04F5F (Vermelho)
        else: 
            accent_color = (142, 155, 176) # #8E9BB0 (Cinza)
            
        # White card body with rounded corners (radius 3.0 for premium look)
        pdf.set_fill_color(255, 255, 255)
        pdf.set_draw_color(226, 232, 240)
        pdf.set_line_width(0.15)
        pdf.rect(25, curr_y, card_w, card_h, style='DF', round_corners=True, corner_radius=3.0)
        
        # Left Accent Strip (rounded on external edges, slightly wider 2.0mm)
        pdf.set_fill_color(*accent_color)
        pdf.rect(25, curr_y, 2.0, card_h, style='F', round_corners=('TOP_LEFT', 'BOTTOM_LEFT'), corner_radius=1.8)
        
        # --- 1. Combined Header (Portal & Date in Elegant Slate) ---
        pdf.set_xy(33, curr_y + 5)
        pdf.set_font("Helvetica", 'B', 7.5)
        pdf.set_text_color(100, 116, 139) # Slate 500
        pdf.cell(100, 4, header_text, align="L")
        
        # --- Sentiment Tag Badge in Top Right with subtle borders ---
        badge_w = 18
        badge_h = 4.2
        badge_x = 25 + card_w - badge_w - 8
        badge_y = curr_y + 5
        
        if 'pos' in sent:
            bg_badge = (230, 244, 234)
            border_badge = (206, 234, 214)
            txt_badge = (19, 115, 51)
            lbl_badge = "POSITIVO"
        elif 'neg' in sent:
            bg_badge = (252, 232, 230)
            border_badge = (250, 210, 207)
            txt_badge = (197, 34, 31)
            lbl_badge = "NEGATIVO"
        else:
            bg_badge = (241, 243, 244)
            border_badge = (232, 234, 237)
            txt_badge = (95, 99, 104)
            lbl_badge = "NEUTRO"
            
        pdf.set_fill_color(*bg_badge)
        pdf.set_draw_color(*border_badge)
        pdf.set_line_width(0.12)
        pdf.rect(badge_x, badge_y, badge_w, badge_h, style='DF', round_corners=True, corner_radius=1.0)
        
        pdf.set_xy(badge_x, badge_y + 0.3)
        pdf.set_font("Helvetica", 'B', 6)
        pdf.set_text_color(*txt_badge)
        pdf.cell(badge_w, badge_h - 0.6, lbl_badge, align="C")
        
        # --- 2. Title of the News Article (Premium Charcoal #2D3748) ---
        pdf.set_xy(33, curr_y + 11)
        pdf.set_font("Helvetica", '', 9.8)
        pdf.set_text_color(45, 55, 72) # #2D3748
        pdf.multi_cell(card_w - 16, 5, titulo)
        
        # --- 3. Sleek Button "VER MATÉRIA ORIGINAL" ---
        if has_link:
            btn_w = 40
            btn_h = 5.5
            btn_x = 25 + card_w - btn_w - 8
            btn_y = curr_y + card_h - btn_h - 5
            
            # Off-white elegant button with outline
            pdf.set_fill_color(247, 250, 252) # #F7FAFC
            pdf.set_draw_color(226, 232, 240) # #E2E8F0
            pdf.set_line_width(0.15)
            pdf.rect(btn_x, btn_y, btn_w, btn_h, style='DF', round_corners=True, corner_radius=1.2)
            
            # Clickable target covering full area
            pdf.set_xy(btn_x, btn_y)
            pdf.set_font("Helvetica", 'B', 6.5)
            pdf.set_text_color(74, 85, 104) # #4A5568
            pdf.cell(btn_w, btn_h, "VER MATÉRIA ORIGINAL", align="C", link=str(link))
            
        pdf.set_y(curr_y + card_h + 5)
        
    # --- Contracapa ---
    pdf.current_section = ""
    pdf.add_page()
    pdf.set_y(120)
    pdf.set_font("Helvetica", 'B', 12)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 10, "Relatório desenvolvido por", new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.ln(5)
    try:
        logo_path = os.path.join(BASE_DIR, "assets", "Logo-80-20-Marketing_preta.png")
        pdf.image(logo_path, x=85, w=40)
    except:
        pass
        
    pdf_out = pdf.output()
    return bytes(pdf_out) if not isinstance(pdf_out, bytes) else pdf_out
