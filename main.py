from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)

cors = CORS(app)

app.config["CORS_HEADERS"] = "Content-Type"


@app.route("/api/hello")
@cross_origin()
def hello_world():
    return {"text": "Hello World!"}


if __name__ == "__main__":
    app.run(host="192.168.8.102", debug=True)
