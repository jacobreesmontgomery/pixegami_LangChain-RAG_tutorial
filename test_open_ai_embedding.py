import openai 
from dotenv import load_dotenv
import os

load_dotenv()

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_USER_KEY")

# Example text to embed
text = "OpenAI provides powerful AI tools."

# Generate embeddings
response = openai.embeddings.create(
    model="text-embedding-ada-002",
    input=text
)

# Extract the embedding vector
embedding = response.data

print(embedding)
