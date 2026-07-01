# Multi-Agent Digest System

<div align="center">


**An AI-Powered Multi-Agent Pipeline for Intelligent Document Processing**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)
[![OpenAI API](https://img.shields.io/badge/OpenAI-API-green.svg)](https://openai.com/)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

---

## 🚀 Overview

Multi-Agent Digest is a **modular, containerized pipeline** that processes multiple documents through a series of specialized AI agents to produce intelligent, prioritized daily digests. Each agent performs a specific task in sequence, creating a powerful workflow for information processing.

### ✨ Key Features

- **📥 Ingestor Agent** - Aggregates content from multiple input files
- **🤖 Summarizer Agent** - Uses OpenAI's GPT-4o-mini to extract key insights
- **🎯 Prioritizer Agent** - Intelligently ranks insights by importance
- **📄 Formatter Agent** - Produces beautiful, structured markdown output
- **🐳 Docker Compose** - Easy orchestration with service dependencies
- **🔄 Sequential Processing** - Each agent waits for the previous to complete

---

## 🏗️ Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                  │     │                  │     │                  │     │                  │
│   📁 INPUT       │────▶│   INGESTOR      │────▶│   SUMMARIZER    │────▶│   PRIORITIZER   │
│   FILES         │     │   Agent          │     │   Agent (LLM)    │     │   Agent          │
│                  │     │                  │     │                  │     │                  │
└─────────────────┘     └─────────────────┘     └─────────────────┘     └─────────────────┘
                                                                           │
                                                                           ▼
┌─────────────────┐     ┌─────────────────┐
│                  │     │                  │
│   FORMATTER     │────▶│   📄 OUTPUT      │
│   Agent         │     │   daily_digest.md│
│                  │     │                  │
└─────────────────┘     └─────────────────┘
```

---

## 📦 Project Structure

```
multi-agent-digest/
├── agents/
│   ├── ingestor/
│   │   ├── app.py           # Combines input files into single document
│   │   └── Dockerfile       # Python 3.10 slim container
│   │
│   ├── summarizer/
│   │   ├── app.py           # OpenAI LLM summarization with retry logic
│   │   └── Dockerfile       # Python container with OpenAI client
│   │
│   ├── prioritizer/
│   │   ├── app.py           # Keyword-based priority scoring
│   │   └── Dockerfile       # Python 3.10 slim container
│   │
│   └── formatter/
│       ├── app.py           # Markdown formatting with timestamps
│       └── Dockerfile       # Python 3.10 slim container
│
├── data/
│   ├── input/               # Source documents to process
│   │   ├── meeting_notes.txt
│   │   ├── newsletter_ai.txt
│   │   └── test.txt
│   ├── ingested.txt         # Combined content (ingestor output)
│   ├── summary.txt          # LLM summary (summarizer output)
│   └── prioritized.txt      # Scored insights (prioritizer output)
│
├── output/
│   └── daily_digest.md      # Final formatted digest
│
├── tests/
│   └── test_prioritizer.py  # Unit tests for prioritizer logic
│
├── docker-compose.yml       # Orchestrates all agents
├── .env                     # Environment variables (OPENAI_API_KEY)
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites

- [Docker](https://www.docker.com/) (v20.10+)
- [Docker Compose](https://docs.docker.com/compose/) (v2.0+)
- [OpenAI API Key](https://platform.openai.com/api-keys)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd multi-agent-digest
   ```

2. **Set your OpenAI API key:**
   ```bash
   echo "OPENAI_API_KEY=your-api-key-here" > .env
   ```
   Or edit the existing `.env` file.

3. **Add your documents:**
   Place any text files into the `data/input/` directory. The system will process all files in this folder.

4. **Run the pipeline:**
   ```bash
   docker-compose up --build
   ```

5. **View your digest:**
   The final output will be available at `output/daily_digest.md`

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key for the Summarizer agent | Yes | None |

### Customizing Priority Keywords

The Prioritizer agent uses specific keywords to score and rank insights. Edit `agents/prioritizer/app.py`:

```python
PRIORITY_KEYWORDS = [
    "urgent", "today", "asap", "important",
    "deadline", "critical", "action required"
]
```

Add or remove keywords based on your organization's terminology.

### LLM Model Configuration

The Summarizer uses GPT-4o-mini by default. You can change this in `agents/summarizer/app.py`:

```python
def summarize(text, retries=MAX_RETRIES):
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Change to "gpt-4o", "gpt-4", etc.
        max_tokens=1000,
        temperature=0.3,
    )
```

---

## 🤖 Agent Details

### 📥 Ingestor Agent

**Purpose:** Aggregates content from multiple input files into a single document.

**Input:** Files in `data/input/` directory
**Output:** `data/ingested.txt`

**Features:**
- Processes all `.txt` files in the input directory
- Preserves file names as section headers
- Handles UTF-8 encoding
- JSON logging for observability

### 🤖 Summarizer Agent

**Purpose:** Uses OpenAI's LLM to extract key insights from the ingested content.

**Input:** `data/ingested.txt`
**Output:** `data/summary.txt`

**Features:**
- Automatic retry logic for rate limits (3 attempts)
- Exponential backoff between retries
- Truncates input to 8000 tokens (fits most models)
- Configurable temperature and max tokens
- Graceful fallback on API errors

**System Prompt:**
```
"You are a helpful assistant that summarizes long text into key bullet 
points. Each bullet should be one concise sentence capturing a core insight."
```

### 🎯 Prioritizer Agent

**Purpose:** Intelligently scores and ranks summary lines by importance.

**Input:** `data/summary.txt`
**Output:** `data/prioritized.txt`

**Algorithm:**
- Scores each line based on keyword matches
- Sorts lines by score (descending)
- Prefixes each line with its score (e.g., `[3] Important deadline`)

**Default Keywords:** `urgent`, `today`, `asap`, `important`, `deadline`, `critical`, `action required`

### 📄 Formatter Agent

**Purpose:** Creates a beautifully formatted markdown digest.

**Input:** `data/prioritized.txt`
**Output:** `output/daily_digest.md`

**Output Format:**
```markdown
# Your Daily AI Digest

**Date:** 2025-07-01

## Top Insights

- **Priority 3**: Critical deadline approaching for Q2 deliverables
- **Priority 2**: Team meeting scheduled for tomorrow
- **Priority 1**: Regular status update
```

---

## 🧪 Testing

Run the prioritizer unit tests:

```bash
python -m pytest tests/test_prioritizer.py -v
```

**Test Coverage:**
- ✅ Single keyword matching
- ✅ Multiple keyword stacking
- ✅ No keywords scoring
- ✅ Case-insensitive matching

---

## 📊 Example Workflow

### Input Files

**`data/input/newsletter_ai.txt`:**
```
AI Weekly Roundup - January 2025
OpenAI released a new reasoning model this week.
URGENT: New EU AI Act regulations take effect in March.
Google announced updates to their Gemini model family.
A startup raised $50M for AI-powered code review tools.
```

**`data/input/meeting_notes.txt`:**
```
Team Meeting Notes
- Q2 planning session scheduled
- Budget approval required ASAP
- Important: Security audit due Friday
```

### Processing Pipeline

1. **Ingestor** combines both files:
   ```
   --- meeting_notes.txt ---
   Team Meeting Notes
   - Q2 planning session scheduled
   - Budget approval required ASAP
   - Important: Security audit due Friday
   
   --- newsletter_ai.txt ---
   AI Weekly Roundup - January 2025
   OpenAI released a new reasoning model this week.
   URGENT: New EU AI Act regulations take effect in March.
   Google announced updates to their Gemini model family.
   A startup raised $50M for AI-powered code review tools.
   ```

2. **Summarizer** creates bullet points (LLM):
   ```
   - New EU AI Act regulations take effect in March
   - Budget approval required for Q2 planning
   - Security audit due this Friday
   - OpenAI released a new reasoning model
   - Google updated their Gemini model family
   ```

3. **Prioritizer** scores and sorts:
   ```
   [2] URGENT: New EU AI Act regulations take effect in March
   [2] Budget approval required ASAP
   [1] Important: Security audit due Friday
   [0] OpenAI released a new reasoning model
   [0] Google updated their Gemini model family
   ```

4. **Formatter** creates final digest:
   ```markdown
   # Your Daily AI Digest

   **Date:** 2025-07-01

   ## Top Insights

   - **Priority 2**: URGENT: New EU AI Act regulations take effect in March
   - **Priority 2**: Budget approval required ASAP
   - **Priority 1**: Important: Security audit due Friday
   - **Priority 0**: OpenAI released a new reasoning model
   - **Priority 0**: Google updated their Gemini model family
   ```

---

## 🛠️ Development

### Running Individual Agents

To test a specific agent locally:

```bash
# Ingestor
cd agents/ingestor
python app.py

# Summarizer (requires OPENAI_API_KEY)
export OPENAI_API_KEY=your-key
cd agents/summarizer
python app.py

# Prioritizer
cd agents/prioritizer
python app.py

# Formatter
cd agents/formatter
python app.py
```

### Adding New Agents

1. Create a new directory under `agents/`
2. Add `app.py` with your agent logic
3. Create a `Dockerfile`
4. Update `docker-compose.yml` with the new service
5. Set dependencies appropriately

---

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **OpenAI** - For providing the powerful LLM models
- **Docker** - For containerization that makes this pipeline portable
- **Python** - For the excellent standard library and ecosystem

---

## 📞 Support

For questions, issues, or feature requests, please open an issue on the GitHub repository.

---

<div align="center">

**Built with ❤️ and AI** | **Multi-Agent Digest System** | **v1.0.0**

</div>
