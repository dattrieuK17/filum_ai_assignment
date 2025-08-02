from sentence_transformers import SentenceTransformer
import torch
import json
import uuid
from pathlib import Path

# Select computation device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"[INFO] Using device: {device}")

# Load embedding model
model = SentenceTransformer("Qwen/Qwen3-Embedding-0.6B", device=device)

def load_json(file_path: str) -> list[dict]:
    """
    Load a JSON file and return its content as a list of dictionaries.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        features = json.load(f)
    return features


def get_embedding_text(feature: dict) -> str:
    """
    Concatenate fields from a feature dictionary into a single string for embedding.
    """
    text_parts = [
        feature["feature_name"] + ".",
        " ".join(feature.get("description", [])),
        feature.get("how_it_helps", ""),
        ". ".join(feature.get("use_cases", []))
    ]
    return " ".join(text_parts).strip()


def embedding_data(features: list[dict]) -> list[dict]:
    """
    Generate embedding vectors from a list of features and return enriched objects.
    
    Each output object includes both the original metadata and the computed embedding.
    """
    objects = []
    for i, feature in enumerate(features):
        text = get_embedding_text(feature)
        
        embedding = model.encode(text, convert_to_numpy=True).tolist()

        print(f"[INFO] Processing feature {i + 1}/{len(features)}: {feature.get('feature_name', 'Unnamed Feature')}")
        print(f"[DEBUG] Text for embedding: {text}")  # Print for debugging
        print(f"[DEBUG] Embedding vector length: {len(embedding)}")

        obj = {
            "id": feature.get("feature_id", str(uuid.uuid4())),
            "feature_name": feature["feature_name"],
            "category": feature.get("category", []),
            "description": feature.get("description", []),
            "how_it_helps": feature.get("how_it_helps", ""),
            "use_cases": feature.get("use_cases", []),
            "keywords": feature.get("keywords", []),
            "vector": embedding
        }

        objects.append(obj)
    return objects


def save_json(objects: list[dict], output_file: str):
    """
    Save a list of objects to a file in JSONL format (1 JSON per line).
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        for obj in objects:
            json.dump(obj, f, ensure_ascii=False)
            f.write('\n')

# # Example usage
# if __name__ == "__main__":
#     current_file = Path(__file__)

#     parent_dir = current_file.parent.parent

#     knowledge_base_path = parent_dir / "data" / "knowledge_base.json"

#     embedding_data_path = parent_dir / "data" / "embedding_data.jsonl"

#     # Load features from the knowledge base JSON file
#     features = load_json(knowledge_base_path)
#     print(f"[INFO] Loaded {len(features)} features from {knowledge_base_path}")

#     # Generate embeddings
#     objects = embedding_data(features)

#     # Save to JSONL for Weaviate import
#     save_json(objects, embedding_data_path)
#     print(f"[INFO] JSONL file for Weaviate import saved to {embedding_data_path}.")
