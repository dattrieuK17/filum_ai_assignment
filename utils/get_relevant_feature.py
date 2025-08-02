import weaviate
import weaviate.classes as wvc
from sentence_transformers import SentenceTransformer
import torch

# Initialize embedding model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"[INFO] Using device: {device}")
model = SentenceTransformer("Qwen/Qwen3-Embedding-0.6B", device=device)

def query(query_text: str, collection_name: str = "Filum_AI_Features", top_k: int = 1):
    """
    Perform semantic search in Weaviate using a SentenceTransformer embedding.

    Args:
        query_text (str): The natural language query to search for.
        collection_name (str): The name of the Weaviate collection to search in.
        top_k (int): Number of top similar results to return.

    Returns:
        None
    """

    # Encode query
    try:
        query_vector = model.encode(query_text, convert_to_numpy=True).tolist()
    except Exception as e:
        print(f"[ERROR] Failed to encode query: {e}")
        return

    # Connect to Weaviate
    try:
        client = weaviate.connect_to_local(host="localhost", port=8080)
    except Exception as e:
        print(f"[ERROR] Failed to connect to Weaviate: {e}")
        return

    try:
        # Retrieve collection
        collection = client.collections.get(collection_name)

        # Perform semantic search
        results = collection.query.near_vector(
            near_vector=query_vector,
            limit=top_k,
            return_metadata=["distance"]
        )

    except Exception as e:
        print(f"[ERROR] Query failed: {e}")
    finally:
        client.close()
        return results.objects

def get_output(result):
    feature_name = result.properties.get('feature_name', 'N/A')
    categories = ', '.join(result.properties.get('category', ['N/A']))
    how_it_helps = result.properties.get('how_it_helps', 'N/A')
    return f"{feature_name} ({categories}) – How it helps: {how_it_helps}"


# # Example usage
# if __name__ == "__main__":
#     example_query = (
#         "Manually analyzing thousands of open-ended survey responses for common themes is too time-consuming."
#     )
#     result = query(example_query, collection_name="Filum_AI_Features", top_k=1)

#     # Print results
#     for obj in result:
#         print("Feature ID    :", obj.properties.get("feature_id", "N/A"))
#         print("Feature Name  :", obj.properties.get("feature_name", "N/A"))
#         print("Category      :", obj.properties.get("category", []))
#         print("Description   :", obj.properties.get("description", []))
#         print("How it helps  :", obj.properties.get("how_it_helps", ""))
#         print("Distance:", obj.metadata.distance)
        
#         print("-" * 60)