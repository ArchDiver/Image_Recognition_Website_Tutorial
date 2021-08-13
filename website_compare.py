#Operations Library
import os

#website libraries
from flask import render_template, Flask, request, flash, redirect, url_for
from keras.saving.hdf5_format import load_model_from_hdf5
from werkzeug.utils import secure_filename

# math libraries
import numpy as np

# Machine_Learing Libraries
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from keras.models import load_model
from keras.backend import set_session

# These are the two categories
X = 'cat'
Y = 'dog'
'''
Two example images for the website, they are in the static directory
in the same directory as this file and match the filenames here
'''
sampleX = 'static/cat.jpg'
sampleY = 'static/dog.jpg'

# Where the user uploaded file is saved
UPLOAD_FOLDER = 'static/uploads'
# ML model filename
ML_MODEL_FILENAME = 'save_model.h5'

# list of allowed file types
ALLOWED_EXTENTIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Creates the website object
app = Flask(__name__)

def load_model_from_file():
  #Sets up the machine learning session
  mySession = tf.Session()
  set_session(mySession)
  myModel = load_model('saved_model.h5')
  myGraph = tf.get_default_graph()
  return (mySession, myModel, myGraph)

# Makes sure that the usable file types are uploaded
def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENTIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
  #Initial webpage load
  if request.method == 'GET':
    return render_template('index.html', myX=X, myY=Y, mySampleX=sampleX, mySample=sampleY)
  else: # This is for request.method == "POST":
    # check if the post request has the file part
    if 'file' not in request.files:
      flash('No file part')
      return redirect(request.url)
    file = request.files['file']
    # if user doesn't select file, browser may also submit an empty part without filename
    if file.filename == '':
      flash("No selected file")
      return redirect(request.url)
    # If is doesn't look like an image file
    if not allowed_file(file.filename):
      flash(str(ALLOWED_EXTENTIONS) + 'Are the only allowed file types.')
      return redirect(request.url)
    #When a proper file is uploaded
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      return redirect(url_for('upload_file', filename=filename))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
  test_image = image.load_img(UPLOAD_FOLDER+"/"+filename, target_size=(150,150))
  test_image = image.img_to_array(test_image)
  test_image = np.expand_dims(test_image, axis=0)

  mySession = app.config['SESSION']
  myModel = app.config['MODEL']
  myGraph = app.config['GRAPH']

  with myGraph.as_default():
    set_session(mySession)
    result = myModel.predict(test_image)
    image_src = "/"+UPLOAD_FOLDER+"/"+filename
    if result[0] < 0.5:
      answer = "<div class='col text-center'><img width='150' height='150' src='"+image_src+"' class='img-thumbnail' /><h4>guess:"+X+" "str(result[0])+"</h4></div><div class='col'></div><div class='w-100'></div>"
    else:
      answer = "<div class='col'></div><div class='col text-center'><img width='150' height='150' src='"+image_src+"' class='img-thumbnail' /><h4>guess:"+Y+" "+str(result[0])+"</h4></div><div class='w-100'></div>"
    results.append(answer)
    return render_template('index.html', myX=X, myY=Y, mySampleX=sampleX, mySampleY=Y, len=len(results), results=results)
    


def main():
  (mySession, myModel, myGraph) = load_model_from_file()

  app.config['SECRET_KEY'] = 'super secret key'

  app.config['SESSION'] = mySession
  app.config['MODEL'] = myModel
  app.config['GRAPH'] = myGraph

  app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
  #This limits the uploads to 16MB
  app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

  app.run() 


#Creates a running list of results
results = []

# Launch the application
main()