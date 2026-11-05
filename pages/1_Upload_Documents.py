import streamlit as st

from components.shell import render_shell
from components.ui import error_state, page_header
from services.api_client import APIError, api_client
from utils.styles import inject_styles

st.set_page_config(page_title="Upload documents | Zorvanta", layout="wide")
inject_styles()
client = api_client()
render_shell(client)
page_header("Knowledge operations", "Upload documents", "Add governed source material to your workspace knowledge index.")

if client.mock:
    st.warning("Demo mode is active (`USE_MOCK=true`). Files are not uploaded to S3. Set `USE_MOCK=false` and configure the API before uploading.")

files = st.file_uploader("Drop PDF or TXT files here", type=["pdf", "txt"], accept_multiple_files=True, help="Files are encrypted in transit and processed asynchronously.")
if files:
    st.markdown(f"**{len(files)} file(s) ready**")
    if st.button("Start secure upload", type="primary", disabled=client.mock):
        for file in files:
            with st.status(f"Processing {file.name}", expanded=True) as status:
                try:
                    st.write("Requesting secure upload URL…")
                    upload = client.upload_url(file.name)
                    st.write("Uploading to encrypted storage…")
                    client.upload_to_presigned_url(upload.get("upload_url", ""), file.getvalue(), upload.get("headers"))
                    st.write("Submitting for indexing…")
                    result = client.ingest(upload["document_id"])
                    status.update(label=f"{file.name} · {result.get('status', 'Submitted').title()}", state="complete")
                except (APIError, KeyError) as exc:
                    status.update(label=f"{file.name} · Upload failed", state="error")
                    error_state(str(exc))
else:
    st.markdown('<div class="card"><strong>Secure, governed ingestion</strong><br><span style="color:#6D7B8C">Supported formats: PDF and TXT · Maximum size follows workspace policy · Every upload is audit logged.</span></div>', unsafe_allow_html=True)
