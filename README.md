![Architecture](images/gen_ai_architecture.png)

# Example Workflow Summary
```
User → Brand Query → FastAPI Backend → OLAMA gemma:2B/Gemini → Store Query Details (MongoDB)
       → Elasticsearch Indexing (Used later for calculating consistency) → NLP/Embedding Scoring
       → Save Metrics (BigQuery/PostgreSQL) → User Fetches Metrics
```
# **Video Presentation**
[![Video Presentation](images/gen_ai_visibility_2.png)](https://www.loom.com/share/b770db2b82fe4cbc8ea04b645d0f0c5e)
# **Project Structure**
```
project/
│
├── app/
│   ├── analysis/
│   │   ├── __init__.py
│   │   └── nlp_pipeline.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── router.py
│   │
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   └── utils.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── auth_models.py
│   │   └── routers/
│   │       ├── __init__.py
│   │       └── auth_router.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── models.py
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   ├── utils.py
│   │   ├── big_query/
│   │   │   ├── __init__.py
│   │   │   ├── client.py
│   │   │   ├── schemas.py
│   │   │   └── service.py
│   │   ├── elasticsearch/
│   │   │   ├── __init__.py
│   │   │   ├── client.py
│   │   │   └── indexing.py
│   │   ├── mongodb/
│   │   │   ├── __init__.py
│   │   │   ├── client.py
│   │   │   └── storage.py
│   │   └── postgres/
│   │       ├── __init__.py
│   │       ├── client.py
│   │       └── storage.py
│   │
│   └── middlewares/
│       ├── __init__.py
│       └── auth_middleware.py
│
├── services/
├── gsvt-frontend/
├── images/
├── .dockerignore
├── .gitignore
├── main.py
├── docker-compose.yaml
├── Dockerfile
├── requirements.txt
├── README.md
└── requirements.txt
```
# GenAI Search Visibility Tracker (GSVT)

A full-stack application designed to mirror the architecture, workflow, and generative search principles used at **elelem AI**—the world’s most advanced Generative Engine Optimization (GEO) platform.

This project demonstrates dual-environment deployment (GCP Cloud Run + Docker), integration with GenAI models (Gemini), and end-to-end data pipelines using MongoDB, Elasticsearch, Redis, and BigQuery.

---

# Purpose of the Project

GSVT allows users to:

* Query a **GenAI model (OLAMA/GEMINI)** to check how a brand appears in AI-generated responses.
* Store, index, and analyze these responses through a **RAG-like relevance system** built on Elasticsearch.
* Compute a **visibility score** that reflects brand discoverability inside GenAI platforms.
* Visualize analytics in a React dashboard.

This aligns directly with **elelem AI’s mission**:

> "Help brands dominate AI-driven search through GEO-powered insights, RAG analytics, and AI visibility tracking."

---

# How It Works

The GenAI Search Visibility Tracker (GSVT) follows a simple but powerful pipeline designed to mirror how elelem AI analyzes GenAI-driven brand visibility.

---

## **User Searches With a Brand Name (Not Full Questions)**

The user provides a **brand keyword**, such as:

* `"Pathao"`
* `"Uber"`
* `"Tesla"`
* `"Starbucks"`

Unlike typical LLM prompts, the system is optimized for **brand-centered search**, not full natural-language questions.

Example input:

```json
{
  "brand": "Pathao"
}
```

This aligns with GEO (Generative Engine Optimization) workflows, where brand-level query monitoring is the goal.

---
### **How We Calculate Visibility Score**
* **sentiment_score** — Measures overall sentiment of the LLM response (positive, neutral, negative).
* **semantic_similarity** — Vector-based similarity between the LLM response and ground-truth brand information.
* **keyword_match** — Ratio of expected brand-related keywords found in the LLM response.
* **brand_freq** — How frequently the brand name appears within the LLM response.
* **correctness** — Checks factual accuracy of the LLM response against known brand attributes.
* **consistency** — Measures whether the LLM response aligns consistently with previous responses for the same brand.
```bash
weights = {
    "sentiment": 0.20,
    "semantic": 0.25,
    "keyword": 0.15,
    "brand_freq": 0.15,
    "correctness": 0.15,
    "consistency": 0.10,
}
```
```bash
score = (
    sentiment_score * weights["sentiment"] +
    semantic_similarity * weights["semantic"] +
    keyword_match * weights["keyword"] +
    brand_freq * weights["brand_freq"] +
    correctness * weights["correctness"] +
    consistency * weights["consistency"]
)
```

### **Store Calculated Metrics in Analytics Storage**

Metrics are stored in:

* **BigQuery** (cloud mode)
* **PostgreSQL** (local mode)

---

## **User Retrieves Visibility Metrics**

Users can query the analytics API to retrieve metrics such as:

### **A. Number of Queries Made for a Brand**

Example:

```json
{
  "brand": "Pathao",
}
```

### **Response**

Example:

```json
{
  "brand": "Pathao",
  "query_count": 14,
  "average_visibility_score": 82.5
}
```
---

# Technologies & Why They Were Chosen

| Component               | Technology                                | Why This Technology?                                                                                          |
| ----------------------- | ----------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| **Backend Framework**   | **FastAPI**                               | High-performance Python framework used heavily at elelem; async-first; ideal for microservices + Cloud Run.   |
| **GenAI Integration**   | **Gemini/OLAMA gemma:2B**                       | Allows testing LLM-response behavior without paid credits; matches elelem’s GenAI data ingestion workflow.    |
| **Primary Database**    | **MongoDB Atlas / Docker MongoDB**        | Flexible schema for storing LLM responses, brand logs, user profiles; identical to elelem’s backend design.   |
| **Search & RAG Engine** | **Elasticsearch**                         | Core requirement; supports vectorization, similarity search, and indexing LLM answers—critical for GEO tasks. |
| **Analytics Warehouse** | **BigQuery (Cloud) / PostgreSQL (Local)** | Enables aggregation + trend analysis; exactly matches elelem’s GCP data pipeline.                             |
| **Frontend**            | **React (Cloud Run)**                     | Interactive dashboard for brand visibility analytics.                                                         |
environment mirroring cloud behavior.                                       |
| **Deployment**          | **GCP Cloud Run + Docker Compose**        | Fully managed, scalable, and compatible with elelem’s production deployment ecosystem.                        |
| **Configuration**       | **Pydantic BaseSettings**                 | Clean, type-safe environment-based configuration switching between cloud/local.                               |
| **Security**            | **JWT + Bcrypt**                          | Stateless, secure, production-ready authentication approach.                                                  |
| **Server**              | **Uvicorn**                               | Blazing-fast ASGI server optimized for FastAPI.                                                               |

---

# Setup Instructions

## Prerequisites

* Python **3.9+**
* MongoDB Atlas OR Docker MongoDB
* OLLAMA (Download and Installed it locally)
* Elasticsearch 8.x (local or Elastic Cloud)
* Node.js (for React/Electron)
* Docker Desktop (for local multi-service environment)

---

## 1️. Clone Project
```bash
git clone https://github.com/anamulislamshamim/GenAI-Search-Visibility-Tracker.git
```

## 2. Virtual Environment Setup

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
# OR
.venv\Scripts\activate      # Windows
```

---

## 3. Install Backend Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment

Create a `.env` file and set:
```bash
ENVIRONMENT=CLOUD
# LOCAL | CLOUD (determines database/LLM usage)
LLM_PROVIDER=GEMINI  # HUGGINGFACE | GEMINI | OPENAI | Ollama
HUGGINGFACE_MODEL=local/brand-visibility-mock-model
GEMINI_API_KEY=AIzaSyASsLTqTP53YaAD5geDLycB9s63mQ99VUI
OLLAMA_MODEL=gemma:2b

# --- Data Store Configuration (Local Docker) ---
MONGO_URI=""
MONGO_DB_NAME="query_analytics"
MONGO_COLLECTION_NAME="brand_analysis"
ELASTICSEARCH_URL=""
ELASTICSEARCH_API_KEY=""
ES_INDEX_NAME="brand_analysis"
POSTGRES_URL=""
POSTGRES_TABLE="brand_analysis"

# JWT AUTH
SECRET_KEY="secret-Es9nWgtOMlzHz6UdzW"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# big query
GCP_PROJECT_ID=''
BQ_DATASET_ID=''
BQ_TABLE_ID=''
```

> All behavior switches based on `.env`.

---

# Running the Application

### **Local (Docker Compose)**

* If you use MongoDB, Postgresql, and Elasticsearch locally in Docker
```bash
# to start ollama server
ollama serve
cd GenAI-Search-Visibility-Tracker
docker-compose up -d
```
* If you will use cloud based solution then you do not need docker-compose for this project.

Local services started:

* FastAPI backend
* React app
* MongoDB, Elasticsearch, PostgreSQL

### **Cloud (GCP Cloud Run)**

```bash
We can follow the above steps for Cloud as well or can buit CI/CD
```

### **Frontend**
In this project, I focused on backend. That's I don't want to share much about fronted. I containerized frontend.
Run the following commands.
```bash
cd gsvt-frontend
# build image from the Dockerfile
docker build -t gsvt-frontend .
# Build and run container
docker run -p 3000:80 gsvt-frontend
```

---

# API Endpoints

## Authentication

| Method | Endpoint       | Description           |
| ------ | -------------- | --------------------- |
| POST   | `/auth/signup` | Register user         |
| POST   | `/auth/login`  | Login with JWT cookie |

---

## Brand Visibility + Analytics

| Method | Endpoint                   | Description                             |
| ------ | -------------------------- | --------------------------------------- |
| POST   | `/api/v1/brand-query`         | Query Gemini for brand visibility       |
| GET    | `/api/v1/metrics/aggregate/{brand_name}`  | Aggregated visibility metrics           |
| GET    | `/api/v1/query/<response_id>` | Check specific LLM response + RAG score |

---

# What This Backend Provides

✔ GenAI-search visibility tracking<br>
✔ RAG-style response scoring<br>
✔ MongoDB + Elasticsearch integration<br>
✔ BigQuery/Postgres analytical pipeline<br>
✔ Dual cloud/local deployment<br>
✔ Production-ready FastAPI architecture<br>
✔ JWT-based secure authentication

---

# Summary

This project is intentionally designed to mimic the architecture, engineering culture, and technical expectations of **elelem AI**.
By using the same cloud stack, search engine, and GenAI-driven data pipeline, this application demonstrates:

* Practical backend engineering skills
* Strong architectural thinking
* Experience with GEO-style systems
* Cloud-native deployment proficiency
* Ability to work in a distributed, multi-environment system
