# from dataclasses import dataclass
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from dotenv import load_dotenv
import openai
import os
import sqlite3

load_dotenv()
openai.api_key = os.environ['OPENAI_API_USER_KEY']

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

SQLITE_PATH = "cached_queries.db"


def initialize_sqlite():
    conn = sqlite3.connect(SQLITE_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS cached_queries
        (query TEXT PRIMARY KEY, response TEXT)
    ''')
    conn.commit()
    conn.close()


def get_cached_response(query):
    conn = sqlite3.connect(SQLITE_PATH)
    c = conn.cursor()
    c.execute('SELECT response FROM cached_queries WHERE query=?', (query,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None


def cache_query_response(query, response):
    conn = sqlite3.connect(SQLITE_PATH)
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO cached_queries (query, response) VALUES (?, ?)', (query, response))
    conn.commit()
    conn.close()


def run_user_query(query):
    initialize_sqlite()
    # Check if the query already exists in SQLite
    cached_response = get_cached_response(query=query)

    if cached_response:
        # Using the cached response as the incoming query was already answered
        return cached_response

    # Prepare the DB.
    db = load_chroma_data()

    # Search the DB.
    results = db.similarity_search_with_relevance_scores(query, k=3)
    if len(results) == 0 or results[0][1] < 0.7: 
        print(f"Unable to find matching results. \n\tHighest similarity score: {results[0][1]}\n\tResults: {results}")
        return "Unable to find matching results."

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query)
    print(prompt)

    model = ChatOpenAI(api_key=openai.api_key)
    response_text = model.predict(prompt)
    cache_query_response(query=query, response=response_text) # Caching the result in SQLite3
    return response_text


def load_chroma_data():
    embedding_function = OpenAIEmbeddings(api_key=openai.api_key)
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
    return db


if __name__ == "__main__":
    query = input("Enter your query here: ")
    run_user_query(query=query)
