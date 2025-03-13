import subprocess
import json
import flask
from flask import request, jsonify

app = flask.Flask(__name__)

# Path to your compiled llama.cpp binary and model
LLAMA_CPP_PATH = "/home/pi/llama.cpp/main"
MODEL_PATH = "/home/pi/llama.cpp/models/mymodel.gguf"

@app.route("/query", methods=["POST"])
def query_model():
    data = request.json
    prompt = data.get("prompt", "")
    
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    
    try:
        result = subprocess.run(
            [LLAMA_CPP_PATH, "-m", MODEL_PATH, "-p", prompt, "--n", "100"],
            capture_output=True,
            text=True
        )
        response = result.stdout.strip()
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
