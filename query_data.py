# from dataclasses import dataclass
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from dotenv import load_dotenv
import openai
import os

load_dotenv()
openai.api_key = os.environ['OPENAI_API_USER_KEY']

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""


def run_user_query(query):
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
    return response_text


def load_chroma_data():
    embedding_function = OpenAIEmbeddings(api_key=openai.api_key)
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
    return db


if __name__ == "__main__":
    query = input("Enter your query here: ")
    run_user_query(query=query)
