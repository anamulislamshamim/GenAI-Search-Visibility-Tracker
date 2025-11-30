
---

# 🌐 GenAI Search Visibility Tracker (GSVT)

A full-stack application designed to mirror the architecture, workflow, and generative search principles used at **elelem AI**—the world’s most advanced Generative Engine Optimization (GEO) platform.

This project demonstrates dual-environment deployment (GCP Cloud Run + Docker), integration with GenAI models (Gemini), and end-to-end data pipelines using MongoDB, Elasticsearch, Redis, and BigQuery.

---

# 🧭 Purpose of the Project

GSVT allows users to:

* Query a **GenAI model (Gemini Free Plan)** to check how a brand appears in AI-generated responses.
* Store, index, and analyze these responses through a **RAG-like relevance system** built on Elasticsearch.
* Compute a **visibility score** that reflects brand discoverability inside GenAI platforms.
* Visualize analytics in a React dashboard.

This aligns directly with **elelem AI’s mission**:

> "Help brands dominate AI-driven search through GEO-powered insights, RAG analytics, and AI visibility tracking."

---

# 🔄 How It Works

The GenAI Search Visibility Tracker (GSVT) follows a simple but powerful pipeline designed to mirror how elelem AI analyzes GenAI-driven brand visibility.

---

## **1️⃣ User Searches With a Brand Name (Not Full Questions)**

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

## **2️⃣ Backend Queries Gemini & Performs RAG-Based Scoring**

Once a brand name is submitted, the backend performs the following steps:

### **A. Query Gemini (or another LLM)**

* Sends the brand keyword as the query.
* Receives an AI-generated response describing the brand.
* Stores the **raw LLM response** in MongoDB (for traceability + replay + auditing).

### **B. Trigger Elasticsearch Indexing**

* The system indexes the response text in Elasticsearch.
* This enables:

  * keyword extraction
  * similarity search
  * RAG-style ranking
  * document retrieval
  * contextual comparison

### **C. Run Visibility Scoring (NLP + Embeddings)**

Using **NLTK + HuggingFace embeddings**, the backend computes:

| Metric                       | Description                                                              |
| ---------------------------- | ------------------------------------------------------------------------ |
| **Brand Mention Score**      | Whether and how strongly the brand appears in the response               |
| **Content Accuracy Score**   | Checks if the AI model generated relevant, truthful, or expected content |
| **Relevance Score**          | How closely the response matches Elasticsearch-ranked documents          |
| **Visibility Score (0–100)** | Combined weighted score measuring brand visibility inside GenAI          |

A simplified visibility calculation might include:

* Brand frequency
* Keyword matching
* Semantic similarity
* Sentiment (optional)

### **D. Store Calculated Metrics in Analytics Storage**

Metrics are stored in:

* **BigQuery** (cloud mode)
* **PostgreSQL** (local mode)

Each record includes:

* brand name
* timestamp
* raw LLM response ID
* visibility score
* keyword extraction data
* LLM model used (e.g., Gemini 1.5 Flash)

This creates a traceable, analytic-friendly dataset.

---

## **3️⃣ User Retrieves Visibility Metrics**

Users can query the analytics API to retrieve metrics such as:

### **A. Number of Queries Made for a Brand**

Example:

```json
{
  "brand": "Pathao",
  "query_count": 14
}
```

### **B. Average Visibility Score**

Example:

```json
{
  "brand": "Pathao",
  "average_visibility_score": 82.5
}
```

### **C. Latest Indexed Responses (Optional)**

Example:

* Last 5 responses
* Latest brand accuracy trend
* Daily/weekly visibility changes

This gives users insight into:

* How often the brand is checked
* How clearly the brand appears in LLMs
* Whether visibility is improving or declining

---

# 📘 Example Workflow Summary

```
User → Brand Query → Backend → Gemini → Store Raw Response (MongoDB)
       → Elasticsearch Indexing → NLP/Embedding Scoring
       → Save Metrics (BigQuery/PostgreSQL) → User Fetches Metrics
```

---

# 🛠️ Technologies & Why They Were Chosen

| Component               | Technology                                | Why This Technology?                                                                                          |
| ----------------------- | ----------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| **Backend Framework**   | **FastAPI**                               | High-performance Python framework used heavily at elelem; async-first; ideal for microservices + Cloud Run.   |
| **GenAI Integration**   | **Gemini Free API**                       | Allows testing LLM-response behavior without paid credits; matches elelem’s GenAI data ingestion workflow.    |
| **Primary Database**    | **MongoDB Atlas / Docker MongoDB**        | Flexible schema for storing LLM responses, brand logs, user profiles; identical to elelem’s backend design.   |
| **Cache Layer**         | **Redis / Redis Cloud**                   | Used for throttling, caching LLM responses, and improving API latency; mirrors elelem’s cloud stack.          |
| **Search & RAG Engine** | **Elasticsearch**                         | Core requirement; supports vectorization, similarity search, and indexing LLM answers—critical for GEO tasks. |
| **Analytics Warehouse** | **BigQuery (Cloud) / PostgreSQL (Local)** | Enables aggregation + trend analysis; exactly matches elelem’s GCP data pipeline.                             |
| **Frontend**            | **React (Cloud Run)**                     | Interactive dashboard for brand visibility analytics.                                                         |
environment mirroring cloud behavior.                                       |
| **Deployment**          | **GCP Cloud Run + Docker Compose**        | Fully managed, scalable, and compatible with elelem’s production deployment ecosystem.                        |
| **Configuration**       | **Pydantic BaseSettings**                 | Clean, type-safe environment-based configuration switching between cloud/local.                               |
| **Security**            | **JWT + Bcrypt**                          | Stateless, secure, production-ready authentication approach.                                                  |
| **Server**              | **Uvicorn**                               | Blazing-fast ASGI server optimized for FastAPI.                                                               |

---

# ⚙️ Setup Instructions

## Prerequisites

* Python **3.9+**
* MongoDB Atlas OR Docker MongoDB
* Redis (local or Redis Cloud)
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
```python
ENVIRONMENT=LOCAL
# LOCAL | CLOUD (determines database/LLM usage)
LLM_PROVIDER=GEMINI  # HUGGINGFACE | GEMINI | OPENAI
HUGGINGFACE_MODEL=local/brand-visibility-mock-model
GEMINI_API_KEY=
OPENAI_API_KEY=
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
```

> All behavior switches based on `RUN_ENV`.

---

# Running the Application

### **Local (Docker Compose)**

* If you use MongoDB, Postgresql, and Elasticsearch locally in Docker
```bash
cd GenAI-Search-Visibility-Tracker
docker-compose up -d
```
* If you will use cloud based solution then you do not need docker-compose for this project.

Local services started:

* FastAPI backend
* React app
* MongoDB, Elasticsearch, PostgreSQL

### **Cloud (GCP Cloud Run)**

Build + deploy:

```bash
We can follow the above steps for Cloud as well or can buit CI/CD
```

Frontend is deployed separately to Cloud Run.

---

# 🔒 API Endpoints

## Authentication

| Method | Endpoint       | Description           |
| ------ | -------------- | --------------------- |
| POST   | `/auth/signup` | Register user         |
| POST   | `/auth/login`  | Login with JWT cookie |

---

## Brand Visibility + Analytics

| Method | Endpoint                   | Description                             |
| ------ | -------------------------- | --------------------------------------- |
| POST   | `/api/v1/brand/query`         | Query Gemini for brand visibility       |
| GET    | `/api/v1/metrics/aggregate/brand`  | Aggregated visibility metrics           |
| GET    | `/api/v1/query/<response_id>` | Check specific LLM response + RAG score |

---

# 📊 What This Backend Provides

✔ GenAI-search visibility tracking<br>
✔ RAG-style response scoring<br>
✔ MongoDB + Elasticsearch integration<br>
✔ BigQuery/Postgres analytical pipeline<br>
✔ Dual cloud/local deployment<br>
✔ Production-ready FastAPI architecture<br>
✔ JWT-based secure authentication

---

# 🎯 Summary

This project is intentionally designed to mimic the architecture, engineering culture, and technical expectations of **elelem AI**.
By using the same cloud stack, caching, search engine, and GenAI-driven data pipeline, this application demonstrates:

* Practical backend engineering skills
* Strong architectural thinking
* Experience with GEO-style systems
* Cloud-native deployment proficiency
* Ability to work in a distributed, multi-environment system

---
