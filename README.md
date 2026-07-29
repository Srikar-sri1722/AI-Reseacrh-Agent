AI Research Agent



An AI-powered multi-agent research application that searches the web, reads relevant content, writes a structured research report, and reviews the generated response through a critic agent.

Live Demo

Try the deployed application here:

https://ai-reseacrh-agent-srikar1704.streamlit.app/

Overview

The application provides a visual research workflow called Signal Deck. A user enters a research topic, and the system processes it through four stages:

Search Agent – searches for recent and relevant sources.

Reader Agent – selects a useful source and extracts detailed content.

Writer Chain – combines the collected research into a structured report.

Critic Chain – reviews the report and provides improvement notes.

The Streamlit interface displays the progress of each stage through animated nodes, live status cards, statistics, run history, and a downloadable Markdown report.

Features

Multi-agent research pipeline

Web search using Tavily

Webpage content extraction

Report generation using Mistral AI

AI-based report review and feedback

Animated Streamlit user interface

Live pipeline progress tracking

Research statistics display

Session-based run history

Downloadable Markdown reports

Streamlit Community Cloud deployment

Workflow

flowchart LR
    A[User Research Topic] --> B[Search Agent]
    B --> C[Reader Agent]
    C --> D[Writer Chain]
    D --> E[Critic Chain]
    E --> F[Final Report and Review]

Tech Stack

Python

Streamlit

LangChain

Mistral AI

Tavily Search API

Beautiful Soup

Requests

HTML and CSS

Project Structure

AI-Reseacrh-Agent/
│
├── app.py              # Streamlit user interface and live pipeline execution
├── agents.py           # Search agent, scraping agent, writer and critic chains
├── pipeline.py         # Research pipeline logic or shared pipeline components
├── tools.py            # Search and web-scraping tools
├── requirements.txt    # Python dependencies
├── README.md            # Project documentation
└── .env                 # Local API keys; do not upload this file

Installation

1. Clone the repository

git clone https://github.com/Srikar-sri1722/AI-Reseacrh-Agent.git
cd AI-Reseacrh-Agent

2. Create a virtual environment

Using uv:

uv venv

Activate it on Windows PowerShell:

.venv\Scripts\Activate.ps1

3. Install dependencies

uv pip install -r requirements.txt

You can also use regular pip:

pip install -r requirements.txt

Environment Variables

Create a .env file in the project root:

MISTRAL_API_KEY=your_mistral_api_key
TAVILY_API_KEY=your_tavily_api_key

Do not commit your .env file or API keys to GitHub.

Recommended .gitignore entries:

.env
.venv/
__pycache__/
*.pyc
.streamlit/secrets.toml

Run Locally

streamlit run app.py

Or with uv:

uv run streamlit run app.py

The application will normally open at:

http://localhost:8501

How to Use

Open the application.

Enter a research topic in the sidebar.

Click Run the deck.

Watch the Search, Reader, Writer, and Critic stages execute.

Review the generated report and critic feedback.

Download the report as a Markdown file.

Streamlit Cloud Deployment

To deploy the project on Streamlit Community Cloud:

Push the project to GitHub.

Open Streamlit Community Cloud.

Select this repository.

Set the branch to main.

Set the main file path to app.py.

Add the following values under App settings → Secrets:

MISTRAL_API_KEY = "your_mistral_api_key"
TAVILY_API_KEY = "your_tavily_api_key"

Save the secrets and reboot the app.

Security

Never commit API keys to GitHub.

Store local secrets in .env.

Store deployed secrets in Streamlit Community Cloud Secrets.

Regenerate any API key that has been publicly exposed.

Future Improvements

Add citations and clickable source links to the final report

Search and analyze multiple webpages instead of one lead source

Add PDF export support

Add report formatting options

Save research history in a database

Add user authentication

Add retry and fallback handling for API failures

Support additional LLM providers

Add streaming model responses

Author

Kandula Srikar

GitHub: Srikar-sri1722

Live Application: AI Research Agent

License

This project is intended for educational and portfolio purposes. Add a license file if you plan to distribute or reuse it publicly.
