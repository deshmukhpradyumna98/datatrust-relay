import streamlit as st
import pandas as pd

st.set_page_config(page_title="DataTrust Relay", layout="wide")

st.title("DataTrust Relay")
st.write("AI investigation workspace for data quality incidents.")

with st.sidebar:
    st.header("Data source")
    mode = st.radio("Choose mode", ["Demo data", "Upload incidents CSV"])

if mode == "Demo data":
    incidents = pd.read_csv("data/sample_incidents.csv")
    tables = pd.read_csv("data/sample_tables.csv")
    lineage = pd.read_csv("data/sample_lineage.csv")
else:
    uploaded_file = st.file_uploader("Upload incidents CSV", type=["csv"])
    if uploaded_file is not None:
        incidents = pd.read_csv(uploaded_file)
        tables = pd.read_csv("data/sample_tables.csv")
        lineage = pd.read_csv("data/sample_lineage.csv")
    else:
        st.warning("Please upload an incidents CSV file to continue.")
        st.stop()

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

st.subheader("Ask DataTrust Relay")

user_question = st.text_area(
    "Ask a question about your data incidents",
    placeholder="Example: Why did the customers table fail?",
    height=120
)

if st.button("Investigate", width="stretch"):
    if not user_question.strip():
        st.warning("Please enter a question before investigating.")
    else:
        q = user_question.lower()

        st.markdown("### Relay response")

        if "customer" in q:
            st.info(
                "The customers issue looks related to an upstream CRM sync problem. "
                "Start by checking recent null-rate changes, source delivery status, and last successful refresh time."
            )
        elif "order" in q:
            st.info(
                "The orders issue appears linked to freshness failure. "
                "Check whether the ETL schedule ran on time, whether source extracts landed, and whether downstream models were refreshed."
            )
        elif "invoice" in q:
            st.info(
                "The invoices issue suggests a row count drop. "
                "Compare source vs target row counts and inspect extraction logs for partial loads or failed filters."
            )
        elif "high" in q:
            st.success(
                "High-severity incidents should be triaged first. "
                "Focus on customers, invoices, and payments because they have the largest potential downstream impact."
            )
        else:
            st.info(
                "Possible root cause: the issue may be linked to an upstream data sync, ETL delay, or schema change. "
                "Check refresh timestamps, anomaly history, and recent pipeline changes first."
            )
st.subheader("Incident investigation details")

for _, row in filtered_incidents.iterrows():
    with st.expander(f"{row['incident_id']} - {row['table_name']} - {row['issue_type']}"):
        st.markdown(f"""
**Severity:** {row['severity']}  
**Detected at:** {row['detected_at']}  
**Summary:** {row['summary']}  
**Suspected cause:** {row['suspected_cause']}  
""")

        st.markdown("**Recommended next checks**")
        if row["issue_type"] == "Null spike":
            st.markdown("""
- Check the upstream source extract.
- Compare null percentage vs previous load.
- Validate mandatory fields in the source system.
""")
        elif row["issue_type"] == "Freshness failure":
            st.markdown("""
- Check the ETL schedule and job logs.
- Confirm source file or API delivery time.
- Verify downstream refresh dependencies.
""")
        elif row["issue_type"] == "Row count drop":
            st.markdown("""
- Compare source and target row counts.
- Check filters introduced in the last deployment.
- Review partial load or failed batch logs.
""")
        elif row["issue_type"] == "Schema drift":
            st.markdown("""
- Compare new values or columns against expected schema.
- Review recent application releases.
- Update validation and transformation rules if needed.
""")
        else:
            st.markdown("""
- Review the latest pipeline run logs.
- Compare this incident with recent anomaly history.
- Check upstream changes and downstream impact.
""")

        st.json({
            "incident_id": row["incident_id"],
            "table_name": row["table_name"],
            "issue_type": row["issue_type"],
            "severity": row["severity"]
        }, expanded=False)