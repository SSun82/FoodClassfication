import os 
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)

from keras.models import load_model 
from keras.backend import set_session
from skimage.transform import resize 
import matplotlib.pyplot as plt 
import tensorflow as tf 
import numpy as np
#import base64

print("Loading model") 
#global sess
#sess = tf.compat.v1.Session()
#set_session(sess)
global model 
model = load_model('CharKwayTeowNasiLemakRGBWorking.h5') 
#global graph
#graph = tf.compat.v1.get_default_graph()

@app.route('/', methods=['GET', 'POST']) 
def main_page():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join('static/uploads', filename))
        return redirect(url_for('prediction', filename=filename))
    return render_template('index.html')

@app.route('/prediction/<filename>') 
def prediction(filename):
    #Step 1
    my_image = plt.imread(os.path.join('static/uploads', filename))
    #Step 2
    my_image_re = resize(my_image, (32,32,3))
    #step 2a
    print(my_image);
    #with open(my_image, "wb") as fh:
    #var vimage64 = fh.write(base64.urlsafe_b64decode('data'))
    
    #Step 3
    #with graph.as_default():
      #set_session(sess)
      #Add
    model.run_eagerly=True  
    probabilities = model.predict(np.array( [my_image_re,] ))[0,:]
    print(probabilities)
    #Step 4
    number_to_class = ['CharKwayTeow', 'NasiLemak']
    index = np.argsort(probabilities)
    predictions = {
      "class1":number_to_class[index[1]],
      "class2":number_to_class[index[0]],
      "prob1":probabilities[index[1]],
      "prob2":probabilities[index[0]],
      "upload_filename":filename,
      #"image64": vimage64,
    }
    #Step 5
    return render_template('predict.html', predictions=predictions, params={})

@app.route('/displaypredict/', methods=['GET']) 
def displaypredict():
    _foodtype = request.args.get('_foodtype')
    _buttondisplay = request.args.get('_buttondisplay')
    #_foodtype='CharKwayTeow'
    #_buttondisplay='both'
    params = {
      "_foodtype":_foodtype,
      "_buttondisplay":_buttondisplay,
    }
    return render_template('predict.html', predictions={},params=params)
  


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
