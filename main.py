from flask import Flask, request, jsonify, Response
from flask_cors import CORS, cross_origin
import base64
import cv2

app = Flask(__name__)

cors = CORS(app)


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

    with open("imageToSave.jpg", "wb") as f:
        f.write(image_bytes)

    img = cv2.imread("imageToSave.jpg")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    cv2.imwrite("imageToSave.jpg", gray)

    processed_image_base64 = base64.b64encode(open("imageToSave.jpg", "rb").read())

    return jsonify(
        {
            "imageBase64": processed_image_base64.decode("utf-8"),
            "status": 200,
        }
    )


if __name__ == "__main__":
    app.run(host="192.168.8.102", debug=True)
