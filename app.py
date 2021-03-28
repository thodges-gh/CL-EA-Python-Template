import cv2
import numpy as np

from flask import Flask, request, jsonify
from image_checker import ImageChecker

from PIL import Image

app = Flask(__name__)
image_checker = ImageChecker()


@app.before_request
def log_request_info():
    app.logger.debug('Headers: %s', request.headers)
    app.logger.debug('Body: %s', request.get_data())


def load_image(data):
    nparr = np.fromstring(data, np.uint8)
    # decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img = Image.fromarray(img)
    return img


@app.route('/register_image', methods=['POST'])
def register_image():
    img = load_image(request.data)
    image_checker.register_new_image(img, 'None')

    # build a response dict to send back to client
    response = {'message': 'image received.'}
    # encode response using jsonpickle
    response = jsonify(response)
    return response


@app.route('/image_score', methods=['POST'])
def image_score():
    img = load_image(request.data)
    score = image_checker.get_image_score(img)

    # build a response dict to send back to client
    response = {'score': str(score)}
    # encode response using jsonpickle
    response = jsonify(response)
    return response


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='8080', threaded=True)
