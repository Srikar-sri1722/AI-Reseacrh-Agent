# 🚀 AI Research Agent

An intelligent **multi-agent AI research assistant** built using **LangChain**, **Mistral AI**, **Tavily Search**, and **Streamlit**. The application automates the complete research workflow by searching the web, extracting detailed information, generating a comprehensive report, and reviewing it using multiple AI agents.

## 🌐 Live Demo

🔗 https://ai-reseacrh-agent-srikar1704.streamlit.app/

---

## 📌 Features

- 🔍 **Search Agent**
  - Searches the web using Tavily Search API.
  - Retrieves reliable and relevant sources for the given topic.

- 📖 **Reader Agent**
  - Selects the most relevant source.
  - Scrapes detailed information for deeper understanding.

- ✍️ **Writer Chain**
  - Combines search results and scraped content.
  - Generates a well-structured research report.

- 📝 **Critic Chain**
  - Reviews the generated report.
  - Provides feedback and suggestions for improvement.

- 📥 Download the generated report as a Markdown file.

- 🎨 Beautiful futuristic Streamlit UI with:
  - Aurora animated background
  - Live multi-agent workflow visualization
  - Progress tracking
  - Interactive dashboard

---

# 🏗️ Architecture

```
                 User Query
                      │
                      ▼
              🔍 Search Agent
                      │
                      ▼
              📖 Reader Agent
                      │
                      ▼
              ✍️ Writer Chain
                      │
                      ▼
              📝 Critic Chain
                      │
                      ▼
              Final Research Report
```

---

# 🛠️ Tech Stack

### Programming Language

- Python

### Frameworks

- Streamlit
- LangChain

### AI Model

- Mistral AI

### Search Engine

- Tavily Search API

### Web Scraping

- BeautifulSoup
- Requests

### Environment

- Python Dotenv

---

# 📂 Project Structure

```
AI-Research-Agent/
│
├── app.py
├── agents.py
├── pipeline.py
├── tools.py
├── requirements.txt
├── .env
└── README.md
```

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/Srikar-sri1722/AI-Reseacrh-Agent.git
```

Go inside the folder

```bash
cd AI-Reseacrh-Agent
```

Create virtual environment

```bash
python -m venv .venv
```

Activate it

### Windows

```bash
.venv\Scripts\activate
```

### Linux / Mac

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file and add:

```env
MISTRAL_API_KEY=YOUR_MISTRAL_API_KEY
TAVILY_API_KEY=YOUR_TAVILY_API_KEY
```

---

# ▶️ Run the Application

```bash
streamlit run app.py
```

---

# 📸 Workflow

1. Enter a research topic.
2. Search Agent searches the web.
3. Reader Agent extracts detailed content.
4. Writer Chain prepares the research report.
5. Critic Chain reviews the report.
6. Download the report.

---

# 🚀 Deployment

The application is deployed on **Streamlit Community Cloud**.

Live Website:

https://ai-reseacrh-agent-srikar1704.streamlit.app/

---

# 📦 Requirements

Some of the major packages used:

- streamlit
- langchain
- langchain-core
- langchain-community
- langchain-mistralai
- tavily-python
- beautifulsoup4
- requests
- python-dotenv

---

# 🔮 Future Improvements

- PDF report generation
- Citation support
- Multi-source comparison
- Research history
- Export to DOCX and PDF
- Voice input support
- Multi-language research

---

# 👨‍💻 Author

**Kandula Srikar**

- GitHub: https://github.com/Srikar-sri1722
- LinkedIn: https://www.linkedin.com/in/kandula-srikar-878b19317/

---

## ⭐ If you like this project, consider giving it a Star!
