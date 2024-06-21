from flask import Flask, request, jsonify
from flask_cors import CORS
import sys

sys.path.insert(1, "C:/Users/17178/Desktop/GITHUB_PROJECTS/pixegami_LangChain-RAG_tutorial")
import query_data as qd

app = Flask(__name__)
# Enabling requests from our front-end React client
CORS(app, resources={r"/*": {"origins": "*"}, })


@app.route("/")
def index():
    return "Chroma Data Retrieval API"


@app.route('/new_query', methods=['POST'])
def new_query():
    """
        Runs the incoming query and returns the results.
    """
    query = request.json.get('input', '')
    response = qd.run_user_query(query=query) if query else "Invalid input."
    return jsonify({"response": response})


if __name__ == '__main__':
    app.run(debug=True)