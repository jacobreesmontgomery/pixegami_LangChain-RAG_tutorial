from langchain.evaluation import load_evaluator
from create_database import SentenceTransformersEmbeddings

def main():
    # Initialize embedding function
    embedding_model = SentenceTransformersEmbeddings()

    # Prompt user for two sentences
    sentence1 = input("Enter the first sentence: ")
    sentence2 = input("Enter the second sentence: ")
    
    # Compare embeddings using the evaluator
    evaluator = load_evaluator(evaluator="pairwise_embedding_distance", embeddings=embedding_model)
    x = evaluator.evaluate_string_pairs(
        prediction=sentence1, 
        prediction_b=sentence2
    )
    print(f"Comparing ({sentence1}, {sentence2}): {x}")


if __name__ == "__main__":
    main()
