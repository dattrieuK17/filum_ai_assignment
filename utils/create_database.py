import json
import weaviate
import weaviate.classes as wvc
from weaviate.classes.config import Configure, Property, DataType, VectorDistances
from pathlib import Path

# Connect to local Weaviate instance
try:
    client = weaviate.connect_to_local(host="localhost", port=8080)
except Exception as e:
    print(f"[ERROR] Failed to connect to Weaviate: {e}")
    exit(1)


def create_database(collection_name: str = "Filum_AI_Features"):
    """
    Delete the existing collection if it exists and create a new one 
    with the specified schema and indexing configuration.
    """
    # Remove old collection if exists
    client.collections.delete(collection_name)

    # Define schema and create collection
    client.collections.create(
        name=collection_name,
        inverted_index_config=Configure.inverted_index(bm25_b=0.75, bm25_k1=1.2),
        vectorizer_config=Configure.Vectorizer.none(),
        vector_index_config=Configure.VectorIndex.flat(distance_metric=VectorDistances.COSINE),
        properties=[
            Property(name="feature_id", data_type=DataType.TEXT, is_indexed=True, is_primary_key=True),
            Property(name="feature_name", data_type=DataType.TEXT, is_indexed=True),
            Property(name="category", data_type=DataType.TEXT_ARRAY, is_indexed=True),
            Property(name="description", data_type=DataType.TEXT_ARRAY, is_indexed=True),
            Property(name="how_it_helps", data_type=DataType.TEXT, is_indexed=True),
            Property(name="use_cases", data_type=DataType.TEXT_ARRAY, is_indexed=True),
            Property(name="keywords", data_type=DataType.TEXT_ARRAY, is_indexed=True)
        ]
    )
    print(f"[INFO] Collection '{collection_name}' created successfully.")


def insert_data_to_db(embedding_data_path: str, collection_name: str = "Filum_AI_Features"):
    """
    Load data from a JSONL file and insert it into the specified Weaviate collection.
    Each line must include an 'id' and 'vector' field.
    """
    try:
        collection = client.collections.get(collection_name)
    except Exception as e:
        print(f"[ERROR] Failed to get collection '{collection_name}': {e}")
        return

    try:
        with open(embedding_data_path, 'r', encoding='utf-8') as f:
            for line_number, line in enumerate(f, start=1):
                try:
                    obj = json.loads(line.strip())

                    # Validate required fields
                    if "id" not in obj or "vector" not in obj:
                        print(f"[WARNING] Line {line_number}: missing 'id' or 'vector'")
                        continue
                    if not isinstance(obj["vector"], list) or not all(isinstance(v, (int, float)) for v in obj["vector"]):
                        print(f"[WARNING] Line {line_number}: invalid vector format")
                        continue

                    # Prepare metadata object
                    metadata = {
                        "feature_id": obj["id"],
                        "feature_name": obj.get("feature_name", ""),
                        "category": obj.get("category", []),
                        "description": obj.get("description", []),
                        "how_it_helps": obj.get("how_it_helps", ""),
                        "use_cases": obj.get("use_cases", []),
                        "keywords": obj.get("keywords", [])
                    }

                    # Insert into Weaviate
                    collection.data.insert(
                        properties=metadata,
                        vector=obj["vector"]
                    )

                except json.JSONDecodeError as e:
                    print(f"[ERROR] Line {line_number}: JSON parse error - {e}")
                except Exception as e:
                    print(f"[ERROR] Line {line_number}: Unexpected error - {e}")

    except FileNotFoundError:
        print(f"[ERROR] File not found: {embedding_data_path}")
        return

    print(f"[INFO] Data from '{embedding_data_path}' inserted successfully.")

# # Example usage
# if __name__ == "__main__":
#         current_file = Path(__file__)

#         parent_dir = current_file.parent.parent


#         embedding_data_path = parent_dir / "data" / "embedding_data.jsonl"

#         create_database()

#         insert_data_to_db(embedding_data_path)

#         print("[INFO] Done.")

#         client.close() 
