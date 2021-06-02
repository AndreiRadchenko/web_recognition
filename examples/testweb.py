# This is a _very simple_ example of a web service that recognizes faces in uploaded images.
# Upload an image file and it will check if the image contains a picture of Barack Andrii.
# The result is returned as json. For example:
#
# $ curl -XPOST -F "file=@Andrii2.jpg" http://127.0.0.1:5001
#
# Returns:
#
# {
#  "face_found_in_image": true,
#  "is_picture_of_Andrii": true
# }
#
# This example is based on the Flask file upload example: http://flask.pocoo.org/docs/0.12/patterns/fileuploads/

# NOTE: This example requires flask to be installed! You can install it with pip:
# $ pip3 install flask

import face_recognition
from flask import Flask, jsonify, request, redirect
import pickle
import os
import werkzeug
import numpy as np

# You can change this to any folder on your system
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_image():
    # Check if a valid image file was uploaded
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # The image file seems valid! Detect faces and return the result.
            return detect_faces_in_image(file)

    # If no valid image file was uploaded, show the file upload form:
    return '''
    <!doctype html>
    <title>Is this a picture of our family?</title>
    <h1>Upload a picture and see if it's a picture of our family!</h1>
    <form method="POST" enctype="multipart/form-data">
      <input type="file" name="file">
      <input type="submit" value="Upload">
    </form>
    <p></p>
    <a href='/add_samples'> Or add some samples here</a>
    '''


def detect_faces_in_image (file_stream):

    # Load face encodings
    with open('data/dataset_faces.dat', 'rb') as f:
	        all_face_encodings = pickle.load(f)

    # Grab the list of names and the list of encodings
    face_names = list(all_face_encodings.keys())
    known_face_encodings = np.array(list(all_face_encodings.values()))

    # Load the uploaded image file
    img = face_recognition.load_image_file(file_stream)
    # Get face encodings for any faces in the uploaded image
    unknown_face_encodings = face_recognition.face_encodings(img)


    # создаём кортеж из двух элементов
    # для индексов от 0 до len(s) - 1
    finded_faces = ""
    faces_list = []
        #((face_names[i], False) 
        #   for i in range(len(face_names)))
    #}
    face_found = 0

    if len(unknown_face_encodings) > 0:
        face_found = len(unknown_face_encodings)
        for face_encoding in unknown_face_encodings: 
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)     

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                #print("best_match_index: ", best_match_index)
                #print("face_names[best_match_index]: ", face_names[best_match_index])
                face_name = ''.join(map(str, face_names[best_match_index]))
                #face_name = face_names[best_match_index]
                # Print the result as a list of names with True/False
                #face_name = ""
                finded_faces += face_name                 
                finded_faces += ", "
                faces_list += [face_name]
            #names_with_result = list(zip(face_names, result))
            #print(names_with_result)
        print(finded_faces)
        #if match_results[0]:
        #    is_Andrii = True

    # Return the result as json
    result = {
        "faces_found": face_found,
        "faces_list": faces_list,   
    }
    return jsonify(result)

def encode_face():
    #os.system("python3 ../fr/encode_face.py")
    os.system("python3 encode_face.py")
    return '''<p>completed</p>
    <a href='/'>Return to the main page</a>
    '''

@app.route('/add_samples', methods=['GET', 'POST'])
def add_samples():

    if request.method == 'POST':
        names = []

        file = request.files['name1']
        name = request.form['name11']
        if file.filename == '':
                pass
        elif name != '':
            names.append(name)
            file.save(os.path.join('', name+'.jpg'))
        
        file = request.files['name2']
        name = request.form['name22']
        if file.filename == '':
                pass
        elif name != '':
            names.append(name)
            file.save(os.path.join('', name+'.jpg'))

        file = request.files['name3']
        name = request.form['name33']
        if file.filename == '':
                pass
        elif name != '':
            names.append(name)
            file.save(os.path.join('', name+'.jpg'))

        file = request.files['name4']
        name = request.form['name44']
        if file.filename == '':
                pass
        elif name != '':
            names.append(name)
            file.save(os.path.join('', name+'.jpg'))

        file = request.files['name5']
        name = request.form['name55']
        if file.filename == '':
                pass
        elif name != '':
            names.append(name)
            file.save(os.path.join('', name+'.jpg'))

        with open('names.txt', 'w') as f:
            for i in range(len(names)):
                f.write(str(names[i])+' ')

        return encode_face()

    return '''
    <form method="POST" enctype="multipart/form-data">
    <p>Add a photo №1 and a name:</p>
        <input type="file" name="name1"> 
        <input type="text" name="name11">
    <p>Add a photo №2 and a name (or leave this field empty):</p>
        <input type="file" name="name2"> 
        <input type="text" name="name22">
    <p>Add a photo №3 and a name (or leave this field empty):</p>
        <input type="file" name="name3"> 
        <input type="text" name="name33">
    <p>Add a photo №4 and a name (or leave this field empty):</p>
        <input type="file" name="name4">
        <input type="text" name="name44">
    <p>Add a photo №5 and a name (or leave this field empty):</p>
        <input type="file" name="name5">
        <input type="text" name="name55">

        <input type="submit" value="Upload">
    </form>

    <a href='/'>Main page</a>'''

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
