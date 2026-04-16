import streamlit as st
import pandas as pd

st.set_page_config(page_title="DataTrust Relay", layout="wide")

st.title("DataTrust Relay")
st.write("AI investigation workspace for data quality incidents.")

incidents = pd.read_csv("data/sample_incidents.csv")
tables = pd.read_csv("data/sample_tables.csv")
lineage = pd.read_csv("data/sample_lineage.csv")

severity_options = ["All"] + sorted(incidents["severity"].unique().tolist())
selected_severity = st.selectbox("Filter by severity", severity_options)

if selected_severity != "All":
    filtered_incidents = incidents[incidents["severity"] == selected_severity]
else:
    filtered_incidents = incidents

col1, col2, col3 = st.columns(3)
col1.metric("Total incidents", len(filtered_incidents))
col2.metric("High severity", len(filtered_incidents[filtered_incidents["severity"] == "High"]))
col3.metric("Tables affected", filtered_incidents["table_name"].nunique())

st.subheader("Incident preview")
st.dataframe(filtered_incidents, width="stretch")

st.subheader("Table metadata")
st.dataframe(tables, width="stretch")

st.subheader("Lineage preview")
st.dataframe(lineage, width="stretch")