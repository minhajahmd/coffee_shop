# 🤖 Python Code for Coffee Shop Chatbot

This folder contains the Python code and notebooks necessary for building and deploying the chatbot system for the coffee shop app. The code is organized into several components, each serving a specific function within the overall project.

---

## 📂 Directory Structure

```
python_code/
├── API/                         # Chatbot API for agent-based system
├── dataset/                     # Dataset for training recommendation engine    
├── products/                    # Product data (names, prices, descriptions, images)   
├── build_vector_database.ipynb  # Builds vector database for RAG model   
├── firebase_uploader.ipynb      # Uploads products to Firebase    
├── recommendation_engine_training.ipynb  # Trains recommendation engine 
```

---

## 📚 Components Overview

### 🔌 API
Handles requests to the chatbot agent system. Acts as the bridge between the React Native frontend and the backend functionality.

### 🗃️ Dataset
Contains the Kaggle dataset used to train the recommendation engine for personalized product suggestions.

### 🛍️ Products
Includes product information (name, price, description, image) used both in the app and for generating chatbot responses.

### 📓 Notebooks

- **`build_vector_database.ipynb`**: Builds the Pinecone vector DB for the RAG model.
- **`firebase_uploader.ipynb`**: Uploads product data to Firebase for real-time access in the app.
- **`recommendation_engine_training.ipynb`**: Trains the recommendation engine using market basket analysis.

---

## 🚀 Getting Started

Follow these steps to configure and run the chatbot system.

### 1️⃣ Install Requirements
```bash
pip install -r requirements.txt
```

### 2️⃣ Set Up Hugging Face
- Create a Hugging Face account
- Choose a model (e.g., LLama 3) and accept its terms if needed
- Create a token
- Add to `.env` file inside `python_code/`:
```
MODEL_NAME=<your_huggingface_model>
```

### 3️⃣ Set Up RunPod
- Sign up at [RunPod](https://www.runpod.io/)
- Create a chatbot endpoint and an embedding endpoint
- In `.env`, add:
```
RUNPOD_TOKEN=<your_runpod_token>
RUNPOD_CHATBOT_URL=<your_chatbot_endpoint>
RUNPOD_EMBEDDING_URL=<your_embedding_endpoint>
```

### 4️⃣ Set Up Pinecone
- Create a [Pinecone](https://www.pinecone.io/) account
- Add to `.env`:
```
PINECONE_API_KEY=<your_pinecone_api_key>
PINECONE_INDEX_NAME=<your_index_name>
```

### 5️⃣ Set Up Firebase
- Create a Firebase project
- Download JSON credentials
- Extract necessary fields and paste into `.env`

### 6️⃣ Run the Notebooks
You’re now ready to run the notebooks. Open each `.ipynb` file in Jupyter or VS Code and execute the cells.

