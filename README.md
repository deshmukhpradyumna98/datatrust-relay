# DataTrust Relay

DataTrust Relay is a lightweight AI investigation workspace for data quality incidents, built with free and shareable tools.

## Live demo
[Open the app](PASTE-YOUR-STREAMLIT-URL-HERE)

## What it does
- Loads demo or uploaded incident CSV data
- Filters incidents by severity
- Shows incident details and recommended investigation checks
- Simulates AI-style investigation responses in plain language

## Why this exists
Data teams often have alerts, logs, and incidents, but not a simple way to investigate them in natural language.
DataTrust Relay is an early prototype for a GenAI-style assistant focused on data trust, observability, and incident triage.

## Local setup
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Current status
MVP deployed on Streamlit Community Cloud.

## Next planned improvements
- Connect a real local LLM with Ollama
- Add database-backed storage for incidents and metadata
- Improve CSV validation and upload experience
- Add richer root-cause explanations

## Tech stack
- Streamlit
- Python
- Pandas
- GitHub
- Streamlit Community Cloud