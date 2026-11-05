"""REST client for the Zorvanta FastAPI service, including a deterministic demo mode."""

from __future__ import annotations

import os
import time
import uuid
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()


class APIError(RuntimeError):
    """A user-safe error returned by the copilot API."""


class APIClient:
    def __init__(self) -> None:
        self.base_url = os.getenv("API_BASE_URL", "http://localhost:8000").rstrip("/")
        self.mock = os.getenv("USE_MOCK", "false").lower() in {"1", "true", "yes"}
        self.timeout = float(os.getenv("API_TIMEOUT_SECONDS", "30"))

    def _request(self, method: str, path: str, **kwargs: Any) -> dict[str, Any]:
        try:
            response = requests.request(method, f"{self.base_url}{path}", timeout=self.timeout, **kwargs)
            if not response.ok:
                try:
                    detail = response.json().get("detail", response.text)
                except ValueError:
                    detail = response.text
                raise APIError(f"{response.status_code}: {detail or 'Backend request failed'}")
            return response.json() if response.content else {}
        except requests.RequestException as exc:
            raise APIError(
                f"The Zorvanta service is unavailable at {self.base_url}. "
                "Start the FastAPI backend or check API_BASE_URL."
            ) from exc

    def chat(self, question: str, conversation_id: str | None = None) -> dict[str, Any]:
        if self.mock:
            return {
                "answer": (
                    "Based on the indexed workspace knowledge, the recommended path is to "
                    "validate the policy owner, confirm the effective date, and record the "
                    "decision in the audit trail."
                ),
                "sources": [
                    {"title": "Enterprise Access Policy", "page": 12, "snippet": "Policy owners must review access quarterly."},
                    {"title": "Operations Handbook", "page": 4, "snippet": "Decisions require an auditable approval record."},
                ],
                "conversation_id": conversation_id or str(uuid.uuid4()),
                "status": "complete",
            }
        payload: dict[str, Any] = {"question": question}
        if conversation_id:
            payload["conversation_id"] = conversation_id
        return self._request("POST", "/api/chat", json=payload)

    def documents(self) -> list[dict[str, Any]]:
        if self.mock:
            return [
                {"id": "doc-001", "title": "Enterprise Access Policy.pdf", "status": "ready", "current_version": 3, "created_at": "2026-10-28T09:32:00Z"},
                {"id": "doc-002", "title": "Operations Handbook.txt", "status": "processing", "current_version": 1, "created_at": "2026-10-30T14:10:00Z"},
                {"id": "doc-003", "title": "Incident Response Playbook.pdf", "status": "failed", "current_version": 2, "created_at": "2026-11-01T08:44:00Z"},
                {"id": "doc-004", "title": "Vendor Risk Framework.pdf", "status": "ready", "current_version": 1, "created_at": "2026-11-02T16:20:00Z"},
            ]
        return self._request("GET", "/api/documents").get("documents", [])

    def upload_url(self, filename: str) -> dict[str, Any]:
        if self.mock:
            return {"document_id": str(uuid.uuid4()), "upload_url": "", "headers": {}}
        try:
            return self._request("POST", "/api/upload-url", json={"filename": filename})
        except APIError as first_error:
            try:
                return self._request("POST", "/api/documents/uploads", json={"filename": filename})
            except APIError:
                raise first_error

    def upload_to_presigned_url(self, url: str, content: bytes, headers: dict[str, str] | None = None) -> None:
        if self.mock:
            time.sleep(0.15)
            return
        if not url:
            raise APIError("The upload service did not return a secure storage URL.")
        try:
            response = requests.put(url, data=content, headers=headers or {}, timeout=self.timeout)
            if not response.ok:
                detail = response.text.strip().replace("\n", " ")
                raise APIError(
                    f"S3 upload failed ({response.status_code})"
                    + (f": {detail[:300]}" if detail else "")
                )
        except requests.RequestException as exc:
            raise APIError("The file could not be uploaded to secure storage.") from exc

    def ingest(self, document_id: str) -> dict[str, Any]:
        if self.mock:
            return {"status": "indexed", "document_id": document_id}
        return self._request("POST", "/api/documents/complete", json={"document_id": document_id})

    def approvals(self) -> list[dict[str, Any]]:
        if self.mock:
            return [
                {"id": "apr-1024", "requester": "ayse.demir", "question": "Delete the legacy vendor policy", "status": "pending", "created_at": "2026-11-04T10:12:00Z"},
                {"id": "apr-1018", "requester": "mehmet.kaya", "question": "Export quarterly access report", "status": "approved", "reviewer": "admin@zorvanta.com", "created_at": "2026-11-03T11:00:00Z"},
            ]
        return self._request("GET", "/api/approvals").get("approvals", [])

    def decide_approval(self, approval_id: str, approve: bool, comment: str = "") -> dict[str, Any]:
        if self.mock:
            return {"status": "approved" if approve else "rejected"}
        return self._request("POST", f"/api/approvals/{approval_id}/decision", json={"approve": approve, "comment": comment})

    def metrics(self) -> dict[str, Any]:
        if self.mock:
            return {"total_queries": 1284, "avg_latency_ms": 842, "error_rate": 0.8, "token_usage": 483920, "blocked_requests": 23}
        try:
            return self._request("GET", "/api/metrics")
        except APIError:
            return self._request("GET", "/api/admin/metrics")


def api_client() -> APIClient:
    return APIClient()
