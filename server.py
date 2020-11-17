from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from PIL import Image
from pycoral.adapters import classify, common
from pycoral.utils.dataset import read_label_file
from pycoral.utils.edgetpu import make_interpreter
import platform
import base64
import numpy as np
import io
import cv2
import argparse

parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-m', '--model', required=True,
                    help='File path of edgetpu .tflite file.')
parser.add_argument('-l', '--labels', required=True,
                    help='File path of labels .txt file.')
parser.add_argument('-c', '--haar', required=True,
                    help='File path of haarcascade .xml file.')
args = parser.parse_args()

app = Flask(__name__)
socketio = SocketIO(app)
face_cascade = cv2.CascadeClassifier(args.haar)

def detectface(img):
    image = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
    faces = face_cascade.detectMultiScale(image, 1.1, 4)
    x, y, w, h = faces[0]
    image = img[y:y+h, x:x+w]
    return image


labels = read_label_file(args.labels)
interpreter = make_interpreter(args.model)
interpreter.allocate_tensors()
size = common.input_size(interpreter)


@app.route('/')
def homeroute():
    return render_template('index.html')


@socketio.on('imgdata')
def getimagedata(message):
    message = bytes(message, encoding='utf-8')
    message = message[message.find(b'/9'):]
    pimage = Image.open(io.BytesIO(base64.b64decode(message)))
    pimage = cv2.cvtColor(np.array(pimage), cv2.COLOR_RGB2BGR)
    pimage = detectface(pimage)
    pimage = cv2.resize(pimage, (224, 224))
    pimage = cv2.flip(pimage, 1)
    common.set_input(interpreter, pimage)
    interpreter.invoke()
    classes = classify.get_classes(interpreter, 1, 0.0)
    for class1 in classes:
        pred = str(labels.get(class1.id, class1.id)) + " " + str(class1.score)
        print(pred)
        emit('predresult', pred)


if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000, ssl_context='adhoc')
    print('Server started')
