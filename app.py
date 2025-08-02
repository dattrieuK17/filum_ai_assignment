from flask import Flask, request, jsonify, render_template
from utils.get_relevant_feature import query, get_output
from utils.embedding_data import load_json, embedding_data, save_json
from utils.create_database import create_database, insert_data_to_db
import torch

# Constants
KNOWLEDGE_BASE_PATH = "data/knowledge_base.json"
EMBEDDING_DATA_PATH = "data/embedding_data.jsonl"

print("[INFO] Loading knowledge base...")
features = load_json(KNOWLEDGE_BASE_PATH)

print("[INFO] Generating embeddings...")
objects = embedding_data(features)

print("[INFO] Saving embedded data to JSONL...")
save_json(objects, EMBEDDING_DATA_PATH)

print("[INFO] Creating Weaviate database...")
create_database()

print("[INFO] Inserting data into Weaviate...")
insert_data_to_db(EMBEDDING_DATA_PATH)

torch.cuda.empty_cache()
print("[INFO] Initialization complete.")


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    query_text = data.get("query", "")

    try:
        results = query(query_text)

        if not results:
            return jsonify({"results": []})

        output = get_output(results[0]) 

        return jsonify({"results": output})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
