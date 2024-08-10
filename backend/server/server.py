from flask import Flask, request, jsonify
from pinecone import Pinecone
import tiktoken
from openai import OpenAI
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()

oai = OpenAI()
encoder = tiktoken.get_encoding("cl100k_base")

pc = Pinecone(api_key=os.environ.get("PINECONE_KEY"))
pc_index = pc.Index("dune-gpt")

@app.route("/get_response", methods=["POST"])
def get_response():

    if request.method != "POST":
        # Return HTTP Error later
        return -1
    
    user_input_json = request.get_json()
    user_input = user_input_json.get("input")

    print(user_input)

    # Refactor to return proper error depending on OAI server error or too long input (make map for each error value)
    user_input_vector = get_embedding(user_input)

    pinecone_results = pc_index.query(vector=user_input_vector, top_k=10, include_values=True)
    print([x["id"] for x in pinecone_results["matches"]])
    
    return jsonify()

def get_embedding(text, model="text-embedding-3-large"):
    retries,MAX_RETRIES = 0,50
    embedding = []
    while not embedding and retries < MAX_RETRIES:
        try:
            if len(encoder.encode(text)) <= 8191:
                embedding = oai.embeddings.create(input = [text], model=model).data[0].embedding
            else:
                return -1
        except Exception as e:
            retries += 1
            if retries == MAX_RETRIES: return -1
    
    return embedding