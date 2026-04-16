import streamlit as st
import pandas as pd

st.set_page_config(page_title="DataTrust Relay", layout="wide")

st.title("DataTrust Relay")
st.write("AI investigation workspace for data quality incidents.")

incidents = pd.DataFrame([
    {"incident_id": "INC-001", "table_name": "customers", "issue_type": "Null spike", "severity": "High"},
    {"incident_id": "INC-002", "table_name": "orders", "issue_type": "Freshness failure", "severity": "Medium"},
    {"incident_id": "INC-003", "table_name": "invoices", "issue_type": "Row count drop", "severity": "High"},
])

col1, col2, col3 = st.columns(3)
col1.metric("Total incidents", len(incidents))
col2.metric("High severity", len(incidents[incidents["severity"] == "High"]))
col3.metric("Tables affected", incidents["table_name"].nunique())

st.subheader("Incident preview")
st.dataframe(incidents, width="stretch")