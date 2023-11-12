from flask import Flask, request, jsonify, Response
from flask_cors import CORS, cross_origin
from rembg import remove
from PIL import Image
from io import BytesIO
import requests
import os
import base64
import cv2
import numpy as np


def calculate_gamma(image, target_brightness):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    avg_brightness = np.average(gray)

    if avg_brightness == 0:
        return 1

    gamma = np.log(target_brightness / np.log(avg_brightness))

    return gamma


def adjust_gamma(image, gamma=1.0):
    # build a lookup table mapping the pixel values [0, 255] to
    # their adjusted gamma values
    invGamma = 1.0 / gamma
    table = np.array(
        [((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]
    ).astype("uint8")

    # apply gamma correction using the lookup table
    return cv2.LUT(image, table)


output_path = f"masked/masked.jpg"


with open(output_path, "wb") as f:
    # input = open(f"original/imageToSave.jpg", "rb").read()
    input = cv2.imread("original/patryk.jpg")

    gamma_value = calculate_gamma(input, 128)

    gamma_adjusted = adjust_gamma(input, gamma_value)

    cv2.imwrite("gamma_adjusted/gamma_adjusted.jpg", gamma_adjusted)

    ycrcb = cv2.cvtColor(gamma_adjusted, cv2.COLOR_BGR2YCrCb)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))

    ycrcb[:, :, 0] = clahe.apply(ycrcb[:, :, 0])

    clahe_img = cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)

    cv2.imwrite("equalized/equalized.jpg", clahe_img)

    blended_img = cv2.addWeighted(clahe_img, 0.5, input, 0.5, 0)

    cv2.imwrite("blended/blended.jpg", blended_img)

    processed = open("blended/blended.jpg", "rb").read()

    subject = remove(
        processed,
        bgcolor=(255, 255, 255, 255),
        alpha_matting_background_threshold=30,
        alpha_matting_erode_size=0,
    )

    f.write(subject)


# app = Flask(__name__)

# cors = CORS(app)


# @app.route("/api/hello")
# @cross_origin()
# def hello_world():
#     return {"text": "Hello World!"}


# @app.route("/api/process-image", methods=["POST"])
# @cross_origin()
# def process_image():
#     content = request.json
#     image_base64 = content["imageBase64"]
#     image_bytes = base64.b64decode(image_base64)

#     with open("original/imageToSave.jpg", "wb") as f:
#         f.write(image_bytes)

#     img = Image.open("original/imageToSave.jpg")

#     output_path = f"masked/masked.jpg"

#     with open(output_path, "wb") as f:
#         input = open(f"original/imageToSave.jpg", "rb").read()
#         subject = remove(
#             input,
#             bgcolor=(255, 255, 255, 255),
#             alpha_matting_background_threshold=30,
#             alpha_matting_erode_size=0,
#         )
#         f.write(subject)

#     processed_image_base64 = base64.b64encode(open("masked/masked.jpg", "rb").read())

#     return jsonify(
#         {
#             "imageBase64": processed_image_base64.decode("utf-8"),
#             "status": 200,
#         }
#     )


# if __name__ == "__main__":
#     app.run(host="192.168.8.102", debug=True)
