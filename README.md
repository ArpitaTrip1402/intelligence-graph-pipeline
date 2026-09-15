# Intelligence Graph Pipeline

An AI data ingestion pipeline that collects research-paper metadata, correlates papers with GitHub repositories, extracts structured information using LLMs, performs deterministic entity resolution, and stores the resulting data in JSON, Excel, and PostgreSQL.

## Features

* Research paper metadata extraction from arXiv
* GitHub repository discovery and current star-count collection
* Asynchronous paper crawling using `asyncio` and `aiohttp`
* Concurrent HTTP requests with connection limits
* Retry mechanism with exponential backoff and jitter
* LLM-based structured data extraction
* LLM fallback chain using Gemini and Groq
* Input truncation for oversized content
* Deterministic entity normalization and alias mapping
* PostgreSQL storage for research-paper records
* Excel dataset generation with six required sheets
* News article candidate collection and full-text extraction
* Publication timestamp extraction and last-24-hour filtering
* Source URL traceability
* No fabricated records

---

## Project Structure

```text
intelligence-graph-pipeline/
│
├── architecture.pdf
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── research_papers.json
│   └── intelligence_graph_dataset.xlsx
│
├── src/
│   ├── crawlers/
│   │   ├── paper_crawler.py
│   │   ├── github_crawler.py
│   │   ├── github_search.py
│   │   ├── async_paper_crawler.py
│   │   ├── async_github_crawler.py
│   │   ├── news_crawler.py
│   │   └── retry.py
│   │
│   ├── llm/
│   │   └── extractor.py
│   │
│   ├── database/
│   │   ├── postgres.py
│   │   ├── insert_papers.py
│   │   ├── create_dataset.py
│   │   └── test_postgres.py
│   │
│   └── pipeline/
│       ├── paper_pipeline.py
│       ├── async_paper_pipeline.py
│       └── entity_resolution.py
│
└── tests/
    └── test_llm.py
```

---

## Tech Stack

* **Python 3.11**
* **Requests**
* **BeautifulSoup**
* **aiohttp**
* **asyncio**
* **Google Gemini API**
* **Groq API**
* **PostgreSQL**
* **psycopg**
* **OpenPyXL**
* **python-dotenv**

---

# 1. Research Paper Pipeline

The research-paper pipeline retrieves metadata from arXiv and correlates papers with GitHub repositories.

### Extracted fields

```json
{
  "schemaVersion": "1.0",
  "recordType": "RESEARCH_PAPER",
  "title": "...",
  "authors": "...",
  "paper_url": "...",
  "github_url": "...",
  "github_stars": 0,
  "published_date": "..."
}
```

### Workflow

```text
arXiv Paper URL
       ↓
Paper Metadata Extraction
       ↓
Paper Title
       ↓
GitHub Repository Search
       ↓
Repository Information
       ↓
GitHub Star Count
       ↓
Structured Research Paper Record
```

The GitHub correlation uses repository search and a title/description matching heuristic. Since repository matching is heuristic-based, results are retained only when a matching repository is found.

---

# 2. Asynchronous Crawling

The project includes an asynchronous crawler implemented using `asyncio` and `aiohttp`.

Multiple paper URLs can be processed concurrently instead of making every request sequentially.

A connection limit is used through `aiohttp.TCPConnector` to control concurrency.

Example:

```python
connector = aiohttp.TCPConnector(limit=10)
```

The asynchronous pipeline combines:

```text
Async Paper Crawler
        +
Async GitHub Search
        +
Concurrent Pipeline Processing
```

The implemented pipeline was tested with multiple arXiv papers and successfully retrieved paper metadata and GitHub information.

---

# 3. Retry and Backoff

The project includes retry handling for transient failures.

The retry mechanism uses:

* Multiple attempts
* Exponential backoff
* Random jitter

The delay increases between attempts:

```text
Attempt 1 → short delay
Attempt 2 → longer delay
Attempt 3 → final attempt
```

This helps reduce repeated requests during temporary failures or API rate limits.

---

# 4. LLM Structured Extraction

The project includes an LLM extraction module that converts unstructured text into structured JSON.

The implemented fallback order is:

```text
Gemini
   ↓
Groq
   ↓
DeepSeek (optional fallback)
```

The extractor:

1. Receives source text
2. Limits oversized input
3. Sends the content to an LLM
4. Requests structured JSON
5. Parses the response
6. Falls back to another provider when necessary

Example output:

```json
{
  "name": "OpenAI",
  "description": "An artificial intelligence research and deployment company...",
  "source_url": "https://example.com/openai"
}
```

API credentials are loaded through environment variables and are not stored in the repository.

---

# 5. News Article Extraction

The project includes a news crawler for AI-related news sources.

The implemented crawler collects article candidates and extracts:

* Article URL
* Publication timestamp
* Full article text

Publication timestamps are normalized into timezone-aware datetime values and can be checked against a 24-hour freshness window.

The crawler was tested with TechCrunch AI and The Verge AI article pages.

---

# 6. Entity Resolution

The project implements deterministic entity normalization using predefined aliases.

Examples:

```text
Open AI        → OpenAI
OpenAI Inc.    → OpenAI
DeepMind       → Google DeepMind
Microsoft Corp → Microsoft
Meta Platforms → Meta
```

The mapping process records:

```text
raw_entity
canonical_entity
entity_type
reason
```

This mapping information is also included in the generated Excel dataset.

---

# 7. PostgreSQL Storage

PostgreSQL is used to store research-paper records.

Database:

```text
intelligence_graph
```

Table:

```text
research_papers
```

The table stores:

* Schema version
* Record type
* Title
* Authors
* Paper URL
* GitHub URL
* GitHub stars
* Published date

The paper URL is unique to prevent duplicate records.

The pipeline uses `psycopg` for PostgreSQL connectivity.

---

# 8. Excel Dataset

The project generates:

```text
data/intelligence_graph_dataset.xlsx
```

The workbook contains the six required sheets:

```text
Startups
Products
Research Papers
Jobs
News
Entity Mapping Log
```

The Research Papers sheet is populated from the collected research-paper data.

The other source-specific sheets are kept empty when verified source data has not been collected, rather than inserting fabricated records.

---

# 9. Data Quality

The pipeline follows a source-first approach.

Each collected record maintains its original source URL where applicable.

The project avoids generating unsupported records or inventing missing information.

For GitHub correlation, repository information is obtained from the GitHub API rather than manually assigning repository URLs or star counts.

---

# 10. Running the Project

Create and activate a Python virtual environment:

```powershell
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Create a `.env` file containing the required API credentials.

### Run the research-paper pipeline

```powershell
python -m src.pipeline.paper_pipeline
```

This generates:

```text
data/research_papers.json
```

### Run the asynchronous pipeline

```powershell
python -m src.pipeline.async_paper_pipeline
```

### Generate the Excel dataset

```powershell
python -m src.database.create_dataset
```

### Insert research papers into PostgreSQL

```powershell
python -m src.database.insert_papers
```

### Test PostgreSQL connection

```powershell
python -m src.database.test_postgres
```

### Test LLM extraction

```powershell
python tests/test_llm.py
```

---

# 11. Environment Variables

API keys are stored locally in `.env`.

Example:

```env
GEMINI_API_KEY=your_key
GROQ_API_KEY=your_key
DEEPSEEK_API_KEY=your_key
```

The `.env` file is excluded from Git using `.gitignore`.

---

# 12. Architecture

The detailed system architecture is available in:

```text
architecture.pdf
```

The architecture document describes the implemented pipeline and separates implemented components from production-scale extensions.

---

## Implementation Status

### Implemented and tested

* arXiv research-paper crawler
* GitHub repository search
* GitHub star collection
* Async crawling with `aiohttp`
* Concurrent paper processing
* Retry with exponential backoff and jitter
* LLM structured extraction
* LLM fallback handling
* Input truncation
* News article extraction
* Publication date filtering
* Deterministic entity resolution
* PostgreSQL storage
* Excel dataset generation
* Source URL traceability

### Not claimed as implemented

The following are not presented as deployed/implemented features:

* Distributed message queues
* Multi-worker production deployment
* Playwright-based crawling
* Vector database
* Graph database
* Production observability infrastructure
* 500k+ record production deployment

These are discussed separately in the architecture document as possible production-scale extensions.

---

## Repository

GitHub:

https://github.com/ArpitaTrip1402/intelligence-graph-pipeline

## License

This project was developed as part of an AI Engineer technical assessment.
