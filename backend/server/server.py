from classes.Model import Model
from flask import Flask, request, jsonify

# What is CORS doing here
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

model = Model()

@app.route("/get_response", methods=["POST"])
def get_response():

    if request.method != "POST":
        # Return HTTP Error later
        return -1
    
    user_input_json = request.get_json()
    user_input = user_input_json.get("input")

    return jsonify(model.get_chat_response(user_input))