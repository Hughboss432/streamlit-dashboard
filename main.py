import os
import sqlite3
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

def plot_graph(df, num_cols, num_plots):                                                     # Plot and config graphs
    st.sidebar.write("---") 
    x_col = st.sidebar.selectbox("Axis X:", num_cols)
    y_list = [
        st.sidebar.selectbox(f"Axis Y - {i+1}:", num_cols) for i in range(num_plots)
    ]

    dashboard = go.Figure()
    for i in range(num_plots):
        dashboard.add_trace(
            go.Scatter(
                x=df[x_col],
                y=df[y_list[i]],
                mode='lines',
                name=y_list[i]
            )
        )
    st.plotly_chart(dashboard)
    st.info('To hide a subgraph, click on the label of the line you want to hide!', icon="ℹ️")

st.set_page_config(page_title="Dashboard with Streamlit", layout="wide")
st.title("📊 Dashboard")
st.sidebar.header("Settings")                                                               # Select the folder where the databases are located
folder = st.sidebar.text_input("Directory path containing the database:", value="/tmp")     # Folder selection box (user types or chooses)

if os.path.isdir(folder):                                                                   # List available db's
    db_files = [f for f in os.listdir(folder) if f.startswith('xapp_db_')]
else:
    db_files = []
    st.warning('Path not found or folder does not have a database starting with "xapp_db_".', icon="⚠️")
# ------
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
            num_plots = st.sidebar.select_slider(
                "Select the number of plots",
                options=[1,2,3,4,5,6,7,8,9,10]
            )
            # --------
            st.write('---')
            if len(num_cols) >= 2:                                                          # Select columns for the plot
                plot_graph(df,num_cols,num_plots)
            else:
                st.info("The table needs to have at least two numerical columns to plot a graph.")
    except:
        st.error('A file is not a database.', icon="🚨")