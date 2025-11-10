import os
import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Dashboard com Streamlit", layout="wide")

st.title("📊 Dashboard")
st.sidebar.header("Configurações")                                                          # Selecionar pasta onde estão os bancos
folder = st.sidebar.text_input("Caminho da pasta com os bancos de dados:", value="/tmp")    # Caixa de seleção de pasta (usuário digita ou escolhe)
if os.path.isdir(folder):                                                                   # Listar bancos disponíveis
    db_files = [f for f in os.listdir(folder) if f.startswith('xapp_db_')]
else:
    db_files = []
    st.warning('Caminho não encontrado ou pasta não tem um banco de dados com inicio "xapp_db_".', icon="⚠️")

if db_files:
    db_selected = st.sidebar.selectbox("Selecione o banco de dados:", db_files)             # Escolher banco
    try:
        db_path = os.path.join(folder, db_selected)
        conn = sqlite3.connect(db_path)                                                     # Conectar db
        tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn) # Retirar tabelas
        tables_list = tables['name'].tolist()                                               # Retirar nomes para selecionar

        if not tables_list:                                                                 # db vazio
            st.error("Nenhuma tabela encontrada neste banco de dados.")
        else:
            table_selected = st.sidebar.selectbox("Selecione a tabela:", tables_list)

            query = f"SELECT * FROM {table_selected}"                                       # Retirar dataframe
            df = pd.read_sql_query(query, conn)
            conn.close()

            st.subheader(f"Tabela: `{table_selected}`")                                     # Mostrar df
            st.dataframe(df)

            num_cols = df.select_dtypes(include=["number"]).columns.tolist()
            st.write('---')
            if len(num_cols) >= 2:                                                          # Selecionar colunas para plot
                x_col = st.selectbox("Eixo X:", num_cols)
                y_col = st.selectbox("Eixo Y:", num_cols, index=min(1, len(num_cols)-1))

                fig = px.scatter(df, x=x_col, y=y_col, title=f"{y_col} vs {x_col}")
                st.plotly_chart(fig)
            else:
                st.info("A tabela precisa ter ao menos duas colunas numéricas para plotar um gráfico.")
    except:
        st.error('Arquivo não é banco de dados.', icon="🚨")