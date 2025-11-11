import os
import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Dashboard with Streamlit", layout="wide")
st.title("📊 Dashboard")
st.sidebar.header("Settings")                                                               # Select the folder where the databases are located
folder = st.sidebar.text_input("Directory path containing the database:", value="/tmp")     # Folder selection box (user types or chooses)

if os.path.isdir(folder):                                                                   # List available db's
    db_files = [f for f in os.listdir(folder) if f.startswith('xapp_db_')]
else:
    db_files = []
    st.warning('Path not found or folder does not have a database starting with "xapp_db_".', icon="⚠️")

if db_files:
    st.sidebar.write('---')
    db_selected = st.sidebar.selectbox("Select the database:", db_files)                    # Choose bd
    try:
        db_path = os.path.join(folder, db_selected)
        conn = sqlite3.connect(db_path)                                                     # Connect to db
        tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn) # Save selected tables
        tables_list = tables['name'].tolist()                                               # Save names from tables

        if not tables_list:                                                                 # db is empty
            st.error("No tables detected in this database.")
        else:
            table_selected = st.sidebar.selectbox("Select table:", tables_list)

            query = f"SELECT * FROM {table_selected}"                                       # Save dataframe
            df = pd.read_sql_query(query, conn)
            conn.close()

            st.subheader(f"Table: `{table_selected}`")                                      # Show df
            st.dataframe(df)

            num_cols = df.select_dtypes(include=["number"]).columns.tolist()
            st.write('---')
            if len(num_cols) >= 2:                                                          # Select columns for the plot
                x_col = st.selectbox("Axis X:", num_cols)
                y_col = st.selectbox("Axis Y:", num_cols, index=min(1, len(num_cols)-1))

                fig = px.scatter(df, x=x_col, y=y_col, title=f"{y_col} vs {x_col}")
                st.plotly_chart(fig)
            else:
                st.info("The table needs to have at least two numerical columns to plot a graph.")
    except:
        st.error('A file is not a database.', icon="🚨")