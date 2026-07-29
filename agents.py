from dotenv import load_dotenv
load_dotenv()
from langchain.agents import create_agent
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import searching
from tools import scraping
import os 
import requests

llm=ChatMistralAI(model="ministral-14b-2512")

def build_search_agent():
    return create_agent(llm,tools=[searching])
def build_scraping_agent():
    return create_agent(llm,tools=[scraping])

prompt1=ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.
Topic: {topic}
Research Gathered:
{research}
Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)
Be detailed, factual and professional."""),
])

writer_chain=prompt1|llm|StrOutputParser()

prompt2=ChatPromptTemplate.from_messages([
     ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.
Report:
{report}
Respond in this exact format:
Score: X/10
Strengths:
- ...
- ...
Areas to Improve:
- ...
- ...
One line verdict:
..."""),
])

critic_chain=prompt2|llm|StrOutputParser()

