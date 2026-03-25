from flask import Flask, request, render_template
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.xception import preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import load_img
import numpy as np
import os
import cv2
from werkzeug.utils import secure_filename

model = load_model("xcep_yoga.h5")

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/home")
def homeagain():
    return render_template("index.html")

@app.route("/iinput")
def predict():
    return render_template("input.html")

@app.route("/ioutput", methods=['POST','GET'])
def output():
    if request.method == 'POST':
        img = request.files["file"]
        filepath = "static/assets/uploaded_image.png"
        img.save(filepath)
        img = load_img(filepath, target_size=(224,224))
        img = image.img_to_array(img)
        img.shape
        x = np.expand_dims (img, axis=0)
        img_data=preprocess_input(x)
        pred = model.predict(img_data)
        p = np.argmax(pred)
        columns = ['Downdog', 'Goddess', 'Plank', 'Tree', 'Warrior2']
        result = str(columns[p])
        return render_template("input.html", prediction = result, img_path="assets/uploaded_image.png")

@app.route("/vinput")
def videoinput():
    return render_template("output.html")

@app.route("/voutput", methods=['POST', 'GET'])
def video():
    # Get a reference to webcam #0 (the default one)
        print("[INFO] starting video stream...")
        vs = cv2.VideoCapture(0)
        #writer = None
        (W, H) = (None, None)
#loop over frames from the video file stream
        while True:
            # read the next frame from the file
            (grabbed, frame) = vs.read()

            #if the frame was not grabbed, then we have reached the end
            # of the stream
            if not grabbed:
                break

            #if the frame dimensions are empty, grab them
            if W is None or H is None:
                (H, W) = frame.shape[:2]
            # clone the output frame, then convert it from BGR to RGB
            # ordering and resize the frame to a fixed 64x64
            output = frame.copy()
            #print("apple")
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (224, 224))
            #frame frame.astype("float32")
            x=np.expand_dims (frame, axis=0)
            result = np.argmax(model.predict(x), axis=-1)
            index=['Downdog', 'Goddess', 'Plank', 'Tree', 'Warrior2']
            result=str(index[result[0]])
            cv2.putText(output, "Detected Yoga Pose: {}".format(result), (30, 80), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
            #playaudio("Emergency it is a disaster")
            cv2.imshow("Output", output)
            key = cv2.waitKey(1) & 0xFF

            # if the q key was pressed, break from the loop
            if key == ord("q"):
                break

        # release the file pointers
        print("[INFO] cleaning up...")
        vs.release()
        cv2.destroyAllWindows()
        return render_template("output.html")

""" Running our application """
if __name__ == "__main__":
    app.run(debug = False)