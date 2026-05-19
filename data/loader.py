import pandas as pd
import streamlit as st

try:
    import gspread
    HAS_GSPREAD = True
except ImportError:
    HAS_GSPREAD = False

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
def carregar_dados_relatorio_sheets(sheet_id, sheet_name="Dados"):
    try:
        if not HAS_GSPREAD:
            return "Biblioteca gspread não instalada."
        
        # Connect using Streamlit Secrets for Production
        gc = gspread.service_account_from_dict(dict(st.secrets["gcp_service_account"]))
        sh = gc.open_by_key(sheet_id)
        worksheet = sh.worksheet(sheet_name)
        
        data = worksheet.get_all_records()
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        return f"Erro ao acessar Google Sheets: {e}"

@st.cache_data
def carregar_dados_saude_marca_sheets(sheet_id, sheet_name="DADOS"):
    try:
        if not HAS_GSPREAD:
            return "Biblioteca gspread não instalada."
        
        # Connect using Streamlit Secrets for Production
        gc = gspread.service_account_from_dict(dict(st.secrets["gcp_service_account"]))
        sh = gc.open_by_key(sheet_id)
        worksheet = sh.worksheet(sheet_name)
        
        all_values = worksheet.get_all_values()
        if not all_values:
            return "Planilha de Saúde de Marca está vazia."
        
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
        
        df = df.loc[:, df.columns.str.strip() != '']
        df = df.replace('', pd.NA).dropna(how='all')
        
        col_saude_raw = next((c for c in df.columns if 'sa' in str(c).lower() and 'de' in str(c).lower()), None)
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
        
        numeric_kws = ['itens', 'positivo', 'negativo', 'neutro', 'mato grosso', 'corumb', 'ladário', 'três lagoas']
        for col in df.columns:
            if any(kw in str(col).lower() for kw in numeric_kws):
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        return df
    except Exception as e:
        return f"Erro ao acessar Saúde de Marca (Sheets): {e}"

def carregar_dados_relatorio(file):
    try:
        xls = pd.ExcelFile(file, engine='openpyxl')
        sheet_name = 'Dados' if 'Dados' in xls.sheet_names else xls.sheet_names[0]
        df = pd.read_excel(xls, sheet_name=sheet_name)
        return df
    except Exception as e:
        return f"Erro ao carregar Notícias local: {e}"
