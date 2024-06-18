# from dataclasses import dataclass
from langchain_community.vectorstores import Chroma
from create_database import SentenceTransformersEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate

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

    model = ChatOllama()
    response_text = model.predict(prompt)

    sources = [doc.metadata.get("source", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)
    return formatted_response


def load_chroma_data():
    embedding_function = SentenceTransformersEmbeddings()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
    return db


if __name__ == "__main__":
    run_user_query()
