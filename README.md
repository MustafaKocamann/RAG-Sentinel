<div align="center">

# RAG Sentinel

### Governed enterprise knowledge copilot

<a href="https://github.com/MustafaKocamann/RAG-Sentinel/actions">
  <img src="https://img.shields.io/github/actions/workflow/status/MustafaKocamann/RAG-Sentinel/cicd.yaml?branch=main&style=for-the-badge&label=CI%2FCD" alt="CI/CD status">
</a>
<img src="https://img.shields.io/badge/Python-3.13%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.13+">
<img src="https://img.shields.io/badge/FastAPI-REST-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
<img src="https://img.shields.io/badge/Streamlit-Workspace-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
<img src="https://img.shields.io/badge/License-TBD-6B7280?style=for-the-badge" alt="License">

<br><br>

<img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&size=18&duration=2800&pause=900&color=5EEAD4&center=true&vCenter=true&width=720&lines=Ask+with+confidence.;Retrieve+only+authorized+evidence.;Keep+every+decision+auditable." alt="RAG Sentinel value proposition">

<br>

**RAG Sentinel**, kurumsal belgelerden kanıta dayalı yanıtlar üreten, tenant izolasyonu ve ACL filtreli retrieval sağlayan bir RAG platformudur.

[Hızlı Başlangıç](#-hızlı-başlangıç) · [Mimari](#-mimari) · [Özellikler](#-öne-çıkan-özellikler) · [API](#-api-yüzeyi) · [Dağıtım](#-dağıtım)

</div>

> **Ürün yüzleri:** FastAPI backend/UI katmanı **Atlas**, Streamlit operasyon workspace’i ise **Zorvanta** olarak adlandırılır.

---

## 🎞️ Ürün ritmi

<div align="center">
  <img src="https://raw.githubusercontent.com/DenverCoder1/readme-typing-svg/main/demo/demo.gif" width="640" alt="Animated developer workflow">
</div>

> README’deki animasyon harici bir görsel kaynaktan yüklenir; uygulamanın runtime bağımlılığı değildir.

---

## Neden RAG Sentinel?

Kurumsal bir copilot yalnızca “iyi cevap” vermemeli; **doğru belgeyi**, **doğru kullanıcıya**, **izlenebilir bir şekilde** sunmalıdır. RAG Sentinel bu akışı şu prensiplerle sınırlar:

- **Grounded answers:** Yanıtlar yalnızca yetkili ve eşik üstü retrieval sonuçlarından üretilir.
- **Tenant-aware access:** Pinecone namespace’leri tenant bazında ayrılır; sonuçlar grup/owner ACL filtresinden geçer.
- **Human-in-the-loop:** Silme, dışa aktarma, politika güncelleme ve gönderme gibi aksiyonlar onaya yönlendirilir.
- **Defence in depth:** Input prompt-injection kontrolleri, output sensitive-data guardrail’leri ve audit event’leri.
- **Operational visibility:** Doküman durumu, feedback, approval ve guardrail metrikleri izlenebilir.

## ✨ Öne çıkan özellikler

| Alan | Yetenek |
|---|---|
| 💬 Copilot | Conversation memory ile takip soruları, kaynak pasajları ve güvenli yanıt üretimi |
| 📚 Ingestion | PDF, DOCX, TXT ve Markdown; S3 presigned upload; chunk + embedding + index |
| 🔐 Erişim | Tenant namespace, `allowed_groups` ve `owner_sub` tabanlı filtreleme |
| 🛡️ Guardrails | Prompt injection, secret request ve hassas çıktı engelleme |
| ✅ Approvals | Admin onayı, karar kaydı ve audit trail |
| 📈 Yönetim | Doküman envanteri, feedback, approval ve workspace metrikleri |
| 🧪 Demo mode | Backend olmadan `USE_MOCK=true` ile deterministik UI demosu |
| 🚀 Delivery | GitHub Actions ile syntax check, Docker build, ECR push ve self-hosted deploy |

---

## 🧭 Mimari

```mermaid
flowchart LR
    U[👤 Kullanıcı] --> UI[Atlas HTML UI / Zorvanta Streamlit]
    UI --> API[FastAPI REST API]
    API --> G[LangGraph RAG graph]
    G --> GR[Input guardrail]
    GR --> E[Google Embeddings]
    E --> V[(Pinecone<br/>tenant namespace)]
    V --> ACL{ACL + relevance filter}
    ACL --> LLM[OpenRouter LLM]
    LLM --> OG[Output guardrail]
    OG --> UI
    API --> PG[(PostgreSQL<br/>documents · approvals · audit)]
    UI --> S3[(Amazon S3<br/>source files)]
    S3 --> ING[Ingestion worker]
    ING --> E
    ING --> V
```

### Soru-cevap akışı

```mermaid
sequenceDiagram
    autonumber
    participant C as Client
    participant A as FastAPI
    participant G as Guardrails
    participant P as Pinecone
    participant M as LLM
    participant D as PostgreSQL

    C->>A: POST /api/chat
    A->>G: classify_input(question)
    alt Riskli istek
        G-->>A: blocked
        A->>D: audit guardrail event
        A-->>C: 400
    else Güvenli istek
        A->>P: embedding + ACL filtered query
        P-->>A: authorized passages
        alt Evidence bulunamadı
            A-->>C: no_evidence
        else Evidence bulundu
            A->>M: question + evidence + history
            M-->>A: grounded answer
            A->>G: sensitive output check
            A->>D: save conversation + audit
            A-->>C: answer + sources + status
        end
    end
```

### Güvenli doküman yaşam döngüsü

```mermaid
stateDiagram-v2
    [*] --> pending: Upload kaydı
    pending --> processing: /api/documents/complete
    processing --> ready: Parse + chunk + embed + upsert
    processing --> failed: Validation / provider error
    failed --> processing: Retry
    ready --> retired: Lifecycle policy
    retired --> [*]
```

---

## 🛠️ Teknoloji yığını

```text
Presentation      FastAPI + Jinja2 + static UI | Streamlit
Orchestration     LangGraph
LLM               OpenRouter (configurable model)
Embeddings        Google Generative AI embeddings
Vector search     Pinecone Serverless, cosine similarity
Object storage    Amazon S3, presigned PUT
Relational data   PostgreSQL via psycopg
Documents         pypdf, python-docx
Observability     GlassFlow RIUS integration (optional)
Delivery          Docker + GitHub Actions + Amazon ECR
```

---

## 🚀 Hızlı Başlangıç

### 1. Kurulum

Windows PowerShell:

```powershell
git clone https://github.com/MustafaKocamann/RAG-Sentinel.git
cd RAG-Sentinel

python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

Python gereksinimi: **3.13 veya üzeri**.

### 2. Konfigürasyon

`.env` dosyasını oluşturun; gerçek secret değerlerini commit etmeyin:

```dotenv
API_BASE_URL=http://localhost:8000
USE_MOCK=false
API_TIMEOUT_SECONDS=30

AWS_REGION=eu-north-1
S3_BUCKET_NAME=your-bucket
DATABASE_URL=postgresql://user:password@host:5432/database

OPENROUTER_API_KEY=...
OPENROUTER_MODEL=nvidia/nemotron-3-ultra-550b-a55b:free
GOOGLE_API_KEY=...
GOOGLE_EMBED_MODEL=gemini-embedding-001
EMBED_DIM=768

PINECONE_API_KEY=...
PINECONE_INDEX_NAME=rag-sentinel-index
PINECONE_CLOUD=aws
PINECONE_REGION=eu-north-1
```

Tam değişken listesi için [`.env.example`](./.env.example) dosyasına bakın. Production değerlerini GitHub Actions secrets olarak sağlayın.

### 3. Veritabanını hazırla

[`infra/schema.sql`](./infra/schema.sql) tabloları oluşturur:

```powershell
python scripts/init_db.py
```

Alternatif olarak SQL’i PostgreSQL üzerinde çalıştırabilirsiniz:

```powershell
psql "$env:DATABASE_URL" -f infra/schema.sql
```

### 4. Backend’i çalıştır

```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- UI: `http://localhost:8000`
- Swagger: `http://localhost:8000/api/docs`
- Liveness: `http://localhost:8000/health/live`
- Readiness: `http://localhost:8000/health/ready`

### 5. Streamlit workspace’i çalıştır

Ayrı bir terminalde:

```powershell
.venv\Scripts\activate
streamlit run app.py
```

Backend bağımlılıkları olmadan UI demosu:

```powershell
$env:USE_MOCK="true"
streamlit run app.py
```

> Mock mode’da upload devre dışıdır; dosya S3’e yazılmaz.

---

## 📥 Ingestion nasıl çalışır?

1. Client, `/api/documents/uploads` üzerinden S3 presigned URL alır.
2. Dosya doğrudan S3’e yüklenir.
3. `/api/documents/complete` ingestion’ı başlatır.
4. Worker dosyayı doğrular ve PDF/DOCX/TXT/MD içeriğini çıkarır.
5. Metin, **1200 karakterlik chunk** ve **180 karakter overlap** ile bölünür.
6. Google embedding’leri üretilir ve Pinecone’a tenant namespace içinde yazılır.
7. ACL metadata’sı (`allowed_groups`, `owner_sub`) vector kaydında tutulur.
8. Doküman `ready` durumuna alınır ve audit event yazılır.

> Taranmış PDF’ler OCR içermez; extractable text yoksa ingestion `failed` olur.

---

## 🔌 API yüzeyi

| Method | Endpoint | Amaç |
|---|---|---|
| `GET` | `/health/live` | Process liveness |
| `GET` | `/health/ready` | PostgreSQL readiness |
| `POST` | `/api/documents/uploads` | S3 upload URL + document kaydı |
| `POST` | `/api/documents/complete` | Ingestion başlatma |
| `GET` | `/api/documents` | ACL filtreli doküman listesi |
| `POST` | `/api/chat` | Guardrailed RAG soru-cevap |
| `GET` | `/api/conversations/{id}/messages` | Conversation history |
| `POST` | `/api/feedback` | Yanıt feedback’i |
| `GET` | `/api/approvals` | Admin approval listesi |
| `POST` | `/api/approvals/{id}/decision` | Approval kararı |
| `GET` | `/api/admin/metrics` | Doküman ve feedback metrikleri |
| `GET` | `/api/admin/guardrails` | Guardrail metrikleri |

Swagger sözleşmesi için backend çalışırken [`/api/docs`](http://localhost:8000/api/docs) adresini açın.

---

## 🗃️ Veri modeli

```mermaid
erDiagram
    DOCUMENTS {
        uuid id PK
        text tenant_id
        text title
        text owner_sub
        text[] allowed_groups
        text s3_key UK
        text status
        int current_version
    }
    CHAT_MESSAGES {
        bigint id PK
        text tenant_id
        uuid conversation_id
        text role
        text content
    }
    APPROVALS {
        uuid id PK
        text tenant_id
        text requester
        text question
        text status
        text reviewer
    }
    AUDIT_EVENTS {
        bigint id PK
        text actor
        text tenant_id
        text action
        jsonb detail
    }
    FEEDBACK {
        bigint id PK
        text tenant_id
        text actor
        int rating
    }
```

Şema kaynağı: [`infra/schema.sql`](./infra/schema.sql).

---

## 📁 Proje yapısı

```text
.
├── app.py                       # Streamlit ana workspace
├── app/
│   ├── main.py                 # FastAPI app ve REST endpoint’leri
│   ├── graph.py                # LangGraph guard → retrieve → generate → validate
│   ├── rag.py                  # RAG graph facade
│   ├── vector.py               # Pinecone namespace, ACL ve search
│   ├── guardrails.py           # Input/output güvenlik kontrolleri
│   ├── memory.py               # PostgreSQL conversation memory
│   └── observability.py        # Opsiyonel RIUS tracing
├── worker/ingest.py             # S3 → parse → chunk → embed → Pinecone
├── services/api_client.py       # Streamlit REST client + mock provider
├── pages/                       # Uploads, documents, approvals, metrics
├── components/                  # Shared Streamlit shell/UI
├── infra/schema.sql             # PostgreSQL şeması ve index’ler
├── .github/workflows/cicd.yaml  # CI, ECR ve deployment pipeline
└── Dockerfile                   # Non-root FastAPI container
```

---

## 🐳 Docker

Backend image’ını lokal olarak build edip çalıştırın:

```powershell
docker build -t rag-sentinel:local .
docker run --rm -p 8000:8000 --env-file .env rag-sentinel:local
```

Container `python:3.13-slim` kullanır, `atlas` isimli non-root kullanıcıyla çalışır ve `8000` portunu expose eder.

---

## 🔁 CI/CD

[`cicd.yaml`](./.github/workflows/cicd.yaml) `main` branch push’larında:

```mermaid
flowchart LR
    A[Push main] --> B[Install Python 3.13]
    B --> C[Compileall syntax check]
    C --> D[Docker build]
    D --> E[Build + push ECR]
    E --> F[Validate production secrets]
    F --> G[Deploy self-hosted EC2]
    G --> H[Container running check]
    H --> I[/health/live smoke test]
```

Gerekli production secrets; AWS credentials, S3, PostgreSQL, OpenRouter, Google embeddings, Pinecone ve RIUS ayarlarını kapsar. Workflow `README.md` değişikliklerinde otomatik tetiklenmez.

---

## 🔒 Güvenlik notları

- `.env` ve API anahtarlarını asla commit etmeyin.
- `USE_MOCK=true` yalnızca demo içindir; gerçek dosya akışını doğrulamaz.
- Guardrail’ler yardımcı bir savunma katmanıdır; IAM, network policy ve gerçek kimlik doğrulamanın yerine geçmez.
- Production’da S3 bucket policy, PostgreSQL erişim listesi, Pinecone index erişimi ve secret rotation ayrıca yapılandırılmalıdır.
- Hassas belgeleri test ortamına yüklemeden önce tenant ve ACL davranışını doğrulayın.

## 🧪 Doğrulama

```powershell
python -m compileall -q app worker services scripts app.py
```

API ayağa kalktıktan sonra:

```powershell
Invoke-RestMethod http://localhost:8000/health/live
Invoke-RestMethod http://localhost:8000/health/ready
```

---

## 📌 Bilinen sınırlar

- Kimlik doğrulama/demo principal katmanı gerçek bir IdP entegrasyonu değildir.
- OCR pipeline’ı yoktur; taranmış PDF’ler metin çıkarımı başarısız olabilir.
- Ingestion mevcut akışta completion çağrısıyla tetiklenir; harici queue/worker orchestration eklenmemiştir.
- `OPENROUTER_MODEL`, embedding modeli ve `EMBED_DIM` değerleri Pinecone index konfigürasyonuyla uyumlu olmalıdır.

## 🤝 Katkı

1. Feature branch oluşturun.
2. Değişikliği küçük ve test edilebilir tutun.
3. Syntax check ve ilgili smoke test’leri çalıştırın.
4. PR açıklamasında veri akışı, güvenlik etkisi ve konfigürasyon değişikliklerini belirtin.

## 📄 Lisans

Bu repository için lisans henüz belirtilmemiştir. Lisans eklenene kadar kullanım ve yeniden dağıtım kararlarını repository sahibiyle netleştirin.

---

<div align="center">

**RAG Sentinel · Evidence first. Governance always.**

</div>
