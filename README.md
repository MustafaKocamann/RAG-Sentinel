# Zorvanta

Zorvanta is an enterprise Streamlit frontend for a multi-tenant RAG and agentic knowledge copilot. It talks to the existing FastAPI backend over REST and keeps presentation concerns separate from the backend.

## Run locally

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
Copy-Item .env.example .env
streamlit run app.py
```

Set `USE_MOCK=true` to demo the complete UI without a backend. For a live service, set `USE_MOCK=false` and point `API_BASE_URL` at the FastAPI service.
Live uploads also require valid AWS credentials, `AWS_REGION`, and `S3_BUCKET_NAME` (or `S3_BUCKET`) in `.env`. In mock mode, the upload control is disabled because no file is written to S3.

## Frontend layout

- `app.py` — chat workspace and application shell
- `pages/` — uploads, document inventory, approvals, and admin metrics
- `components/` — shared navigation and UI primitives
- `services/api_client.py` — timeout-aware REST client and mock provider
- `utils/styles.py` — corporate theme and responsive CSS

The client uses the deployed `/api/documents/uploads` and `/api/documents/complete` routes for the upload flow.
