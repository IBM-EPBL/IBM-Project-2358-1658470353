from flask import Flask,redirect, request, url_for, render_template
import sqlite3 as sql

app=Flask(__name__)

class DB:
    def _init_(self, name = 0):
         self._name = name
         self._lid = 0
         self._tot=0

    # getter method
    def get_name(self):
        return self._name

    # setter method
    def set_name(self, x):
        self._name = x
    def get_lid(self):
        return self._lid

    # setter method
    def set_lid(self, x):
        self._lid = x

    def get_tot(self):
        return self._tot

    # setter method
    def set_tot(self, x):
        self._tot = x
obj=DB()
@app.route('/')
def home():
    try:
        lid=obj.get_lid()
        print(lid)
        return render_template('login.html',data=lid)
    except Exception as e:
        return render_template('login.html')


@app.route('/login')
def login():
    # obj._lid=0
    return render_template('login.html')
@app.route("/login", methods = ["GET","POST"])
def Login():

    l_id = request.form["logname"]
    l_pass  = request.form["logpass"]

    tab=l_id+l_pass
    #print("name")
    if request.method == 'POST':
        print("name")
        l_id = request.form["logname"]
        l_pass  = request.form["logpass"]

        tab=l_id+l_pass
        print(tab)
        obj.set_name(tab)
        obj.set_lid(l_id)
        return redirect(f"/check")

    return render_template('invalid.html',invalid='Please enter a valid data')

@app.route('/sign')
def sign():
    return render_template('signup.html')

@app.route("/regis",methods=["GET","POST"])
def regis():
    u_id = request.values.get("signu_id")
    s_pass  = request.values.get("sign_pass")
    print(u_id)
    print(s_pass)
    table_name=u_id+s_pass
    print(table_name)
    try:
        conn=sql.connect('main.db')

        print("Opened database successfully")
        create="CREATE TABLE "+table_name+" (detail TEXT, cred TEXT)"
        conn.execute(create)
        #conn.execute("select * from credential")

        print("Table created successfully")
        conn.close()
        return render_template("success.html")
    except:
        # print("dsa")
        return render_template("invalid.html", a="Username and password are already taken. Try another.")
@app.route("/check",methods = ["GET","POST"])
def cart():
    tab=obj.get_name()
    lid=obj.get_lid()
    print(lid)
    if request.method == 'GET':
        print(f"Your name is {tab}")
        try:
            con = sql.connect("main.db")
            con.row_factory = sql.Row
            cur = con.cursor()
            a=f"select * from {tab}"
            print(a)
            cur.execute(a)
            return render_template('index.html',data=lid)
        except :
            return render_template('invalid.html',a='Please enter a valid data')


from flask import Flask, render_template, request
from keras.models import load_model
from keras.preprocessing import image
import pickle
import cv2
from skimage import feature
import os.path

# app = Flask(__name__)
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

     
# if __name__=="__main__":
#     app.run(debug=True)