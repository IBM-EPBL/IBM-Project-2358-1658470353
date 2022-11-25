from flask import Flask, render_template, request
from keras.models import load_model
from keras.preprocessing import image
import pickle
import cv2
from skimage import feature
import os.path

app = Flask(__name__)
def predict_label(img_path):
        model = pickle.loads(open('parkinson.pkl', "rb").read())
        #img_path="F:/Pradhicsha/IBM/test1/templates/static/V55HO08.png"
        # Pre-process the image in the same manner we did earlier
        image = cv2.imread(img_path)
        output = image.copy()

        # Load the input image, convert it to grayscale, and resize
        output = cv2.resize(output, (128, 128))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.resize(image, (200, 200))
        image = cv2.threshold(image, 0, 255,
    	cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    	# Quantify the image and make predictions based on the extracted features using the last trained Random Forest
        features = feature.hog(image, orientations=9,
		pixels_per_cell=(10, 10), cells_per_block=(2, 2),
		transform_sqrt=True, block_norm="L1")
        preds = model.predict([features])
        print(preds)
        ls=["healthy","parkinson"]
        return(ls[preds[0]]) 
# routes
@app.route("/", methods=['GET', 'POST'])
def main():
	return render_template("index.html")

@app.route("/about")
def about_page():
	return "Please subscribe  Artificial Intelligence Hub..!!!"

@app.route("/submit", methods = ['GET', 'POST'])
def get_output():
        if request.method == 'POST':
            # img = request.files['my_image']
            # img_path = "..static/" + img.filename
            # img.save(img_path)
            img = request.files['my_image']

            img_path = "static/" + img.filename	
            img.save(img_path)
            p=predict_label(img_path)
        return render_template("index.html", prediction = p, img_path = img_path)


if __name__ =='__main__':
	#app.debug = True
	app.run(debug = True)