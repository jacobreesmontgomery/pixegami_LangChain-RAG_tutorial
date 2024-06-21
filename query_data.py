# from dataclasses import dataclass
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from dotenv import load_dotenv
import openai
import os

load_dotenv()
openai.api_key = os.environ['OPENAI_API_USER_KEY']

CHROMA_RAG_DB_PATH = "chroma/rag_db"
CHROMA_CACHED_QUERIES_DB_PATH = "chroma/cached_queries_db"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""


def run_user_query(query):
    cached_queries_db = load_chroma_data(CHROMA_CACHED_QUERIES_DB_PATH)

    # Check if the incoming query is similar to one that was already made and answered
    cached_response = cached_queries_db.similarity_search_with_relevance_scores(query=query, k=3)
    if (cached_response and cached_response[0][1] > 0.85):
        print(f"Response was found in cached memory:\n\t{cached_response[0][0].page_content}")
        return cached_response[0][0].page_content

    # Prepare the RAG DB.
    rag_db = load_chroma_data(CHROMA_RAG_DB_PATH)

    # Search the RAG DB.
    results = rag_db.similarity_search_with_relevance_scores(query=query, k=3)
    if len(results) == 0 or results[0][1] < 0.7: 
        print(f"Unable to find matching results. \n\tHighest similarity score: {results[0][1]}\n\tResults: {results}")
        return "Unable to find matching results."

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query)

    model = ChatOpenAI(api_key=openai.api_key)
    response_text = model.predict(prompt)

    # Store the new query and response in the Chroma vector store
    cached_queries_db.add_texts([response_text])
    cached_queries_db.persist()
    
    return response_text


def load_chroma_data(chroma_path):
    embedding_function = OpenAIEmbeddings(api_key=openai.api_key)
    db = Chroma(persist_directory=chroma_path, embedding_function=embedding_function)
    return db


if __name__ == "__main__":
    query = input("Enter your query here: ")
    run_user_query(query=query)
