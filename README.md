# 📌 Filum AI – AI Engineer Assignments

This repository design a **"Pain Point to Solution Agent."** This agent's primary function will be to take a user's described business pain point (related to customer experience or service) and suggest relevant Filum.ai features or capabilities that can help address that pain point.

---

## 🚀 How to Set Up and Run

### 1. Download Docker Desktop
Go to this link to download: https://www.docker.com/products/docker-desktop/

### 2. Clone the repository and create a virtual environment

```bash
git clone https://github.com/dattrieuK17/filum_ai_assignment.git
cd filum_ai_assignment
python -m venv .venv
source .venv/bin/activate         # On Unix/macOS
# .venv\Scripts\activate          # On Windows

pip install -r requirements.txt
```

### 3. Start Weaviate service
```bash
docker-compose up -d
```

### 4. Run
Run without UI: Run All in `full_pipeline.ipynb `  

Run with UI:
```bash
python app.py
```
and then go to http://127.0.0.1:5000/

## 📂 Project Structure
```
filum_ai_assignment/
├── .venv/
├── data/
│   ├── embedding_data.jsonl    # Stores the pre-computed vector embeddings for each feature.
│   └── knowledge_base.json     # The knowledge base file containing details about Filum.ai features.
├── static/
│   ├── chat.js                 # Handles client-side logic for the chat interface (sending messages, displaying responses).
│   └── style.css               # Provides styling for the web application's user interface.
├── templates/
│   └── index.html              # The main HTML file for the user interface.
├── utils/  
│   ├── create_database.py      # Script to initialize and set up the schema for the Weaviate vector database.
│   ├── embedding_data.py       # Script to generate and load the feature data and embeddings into Weaviate.
│   └── get_relevant_feature.py # Contains the core logic for querying and retrieving relevant features from the database.
├── app.py                      # The main entry point to run the Flask web application.
├── docker-compose.yml          # Configuration file to run Weaviate services using Docker Compose.
├── full_pipeline.ipynb         # A Jupyter Notebook demonstrating the full pipeline with clear input/output examples.
├── README.md
└── requirements.txt            # Lists all Python packages required to run the project.
```

