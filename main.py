import os
import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Dashboard com Streamlit", layout="wide")

st.title("📊 Dashboard")
st.sidebar.header("Configurações")                                                          # Selecionar pasta onde estão os bancos
folder = st.sidebar.text_input("Caminho da pasta com os bancos de dados:", value="./dados") # Caixa de seleção de pasta (usuário digita ou escolhe)
if os.path.isdir(folder):                                                                   # Listar bancos disponíveis
    db_files = [f for f in os.listdir(folder)]
else:
    db_files = []
    st.warning('Caminho não encontrado ou pasta vazia.', icon="⚠️")

if (len(db_files) != 0):
    db_selected = st.sidebar.selectbox("Selecione o banco de dados:", db_files)             # Escolher banco
    try:
        db_path = os.path.join(folder, db_selected)
        conn = sqlite3.connect(db_path)                                                     # Mostrar tabelas disponíveis
        tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn)
        tables_list = tables['name'].tolist()

        if not tables_list:
            st.error("Nenhuma tabela encontrada neste banco de dados.")
            st.stop()

        table_selected = st.sidebar.selectbox("Selecione a tabela:", tables_list)

        query = f"SELECT * FROM {table_selected}"
        df = pd.read_sql_query(query, conn)
        conn.close()

        st.subheader(f"Tabela: `{table_selected}`")
        st.dataframe(df.head())

        num_cols = df.select_dtypes(include=["number"]).columns.tolist()

        if len(num_cols) >= 2:
            x_col = st.selectbox("Eixo X:", num_cols)
            y_col = st.selectbox("Eixo Y:", num_cols, index=min(1, len(num_cols)-1))
            
            fig = px.scatter(df, x=x_col, y=y_col, title=f"{y_col} vs {x_col}")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("A tabela precisa ter ao menos duas colunas numéricas para plotar um gráfico.")
    except:
        st.error('Arquivo não é banco de dados.', icon="🚨")