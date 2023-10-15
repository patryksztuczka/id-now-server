from flask import Flask, request, jsonify, Response
from flask_cors import CORS, cross_origin
import base64

app = Flask(__name__)

cors = CORS(app)

# app.config["CORS_HEADERS"] = "Content-Type"


@app.route("/api/hello")
@cross_origin()
def hello_world():
    return {"text": "Hello World!"}


@app.route("/api/process-image", methods=["POST"])
@cross_origin()
def process_image():
    content = request.json

    image_base64 = content["imageBase64"]
    image_bytes = base64.b64decode(image_base64)
    with open("imageToSave.png", "wb") as f:
        f.write(image_bytes)
    return {"status": "success"}


if __name__ == "__main__":
    app.run(host="192.168.8.102", debug=True)
