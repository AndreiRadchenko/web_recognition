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
from flask import Flask, jsonify, request, redirect, render_template
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


@app.route('/test', methods=['GET', 'POST'])
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
    return render_template("TestPage.html")


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
    return '''
    <head>
        <title>Completed</title>
        <meta name="viewport" content="width=device-width, initial-scale=1"/>
    </head>
    <body style="background-color: #111;
    font-family: Tahoma, sans-serif;">

        <p style="
        font-size: 50px;
        background-color:#222;
        text-align: center;
        color:#fff;
        padding: 8px;
        margin: 4px;">Completed</p>

        <div style="text-align: center;">
            <button style="
            background-color: #555;
            border: none;
            color: #fff;
            padding: 15px 0px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;" type="submit">
                <a style="
                text-decoration: none;
                color: #fff;
                padding-left: 32px;
                padding-right: 32px;
                padding-top: 15px;
                padding-bottom: 15px;" href='/'>
                    Return to the main page
                </a>
            </button>
        </div>
    </body>
    '''

picPath = os.path.join("static")
app.config["UPLOAD_FOLDER"] = picPath

@app.route('/', methods=['GET', 'POST'])
def add_samples():

    if request.method == 'POST':
        names = []
        with open('names.txt', 'r') as f:
            oldNames = f.read().split()

        file = request.files['filename1']
        name = request.form['name1']
        try:
            if name != oldNames[0] and file.filename == '': #changing name leaving photo
                names.append(name)
            elif name == oldNames[0] and file.filename == '': #changing nothing
                names.append(oldNames[0])
            elif name == oldNames[0] and file.filename != '': #changing photo leaving name
                names.append(oldNames[0])
                file.save(os.path.join('static', name+'.jpg'))
            elif name != oldNames[0] and file.filename != '': #changing photo changing name
                names.append(name)
                file.save(os.path.join('static', name+'.jpg'))
        except IndexError:
            if name != '':
                names.append(name)
                file.save(os.path.join('static', name+'.jpg'))

        file = request.files['filename2']
        name = request.form['name2']
        try:
            if name != oldNames[1] and file.filename == '': #changing name leaving photo
                names.append(name)
            elif name == oldNames[1] and file.filename == '': #changing nothing
                names.append(oldNames[1])
            elif name == oldNames[1] and file.filename != '': #changing photo leaving name
                names.append(oldNames[1])
                file.save(os.path.join('static', name+'.jpg'))
            elif name != oldNames[1] and file.filename != '': #changing photo changing name
                names.append(name)
                file.save(os.path.join('static', name+'.jpg'))
        except IndexError:
            if name != '':
                names.append(name)
                file.save(os.path.join('static', name+'.jpg'))

        file = request.files['filename3']
        name = request.form['name3']
        try:
            if name != oldNames[2] and file.filename == '': #changing name leaving photo
                names.append(name)
            elif name == oldNames[2] and file.filename == '': #changing nothing
                names.append(oldNames[2])
            elif name == oldNames[2] and file.filename != '': #changing photo leaving name
                names.append(oldNames[2])
                file.save(os.path.join('static', name+'.jpg'))
            elif name != oldNames[2] and file.filename != '': #changing photo changing name
                names.append(name)
                file.save(os.path.join('static', name+'.jpg'))
        except IndexError:
            if name != '':
                names.append(name)
                file.save(os.path.join('static', name+'.jpg'))

        file = request.files['filename4']
        name = request.form['name4']
        try:
            if name != oldNames[3] and file.filename == '': #changing name leaving photo
                names.append(name)
            elif name == oldNames[3] and file.filename == '': #changing nothing
                names.append(oldNames[3])
            elif name == oldNames[3] and file.filename != '': #changing photo leaving name
                names.append(oldNames[3])
                file.save(os.path.join('static', name+'.jpg'))
            elif name != oldNames[3] and file.filename != '': #changing photo changing name
                names.append(name)
                file.save(os.path.join('static', name+'.jpg'))
        except IndexError:
            if name != '':
                names.append(name)
                file.save(os.path.join('static', name+'.jpg'))

        file = request.files['filename5']
        name = request.form['name5']
        try:
            if name != oldNames[4] and file.filename == '': #changing name leaving photo
                names.append(name)
            elif name == oldNames[4] and file.filename == '': #changing nothing
                names.append(oldNames[4])
            elif name == oldNames[4] and file.filename != '': #changing photo leaving name
                names.append(oldNames[4])
                file.save(os.path.join('static', name+'.jpg'))
            elif name != oldNames[4] and file.filename != '': #changing photo changing name
                names.append(name)
                file.save(os.path.join('static', name+'.jpg'))
        except IndexError:
            if name != '':
                names.append(name)
                file.save(os.path.join('static', name+'.jpg'))

        with open('names.txt', 'w') as f:
            for i in range(len(names)):
                f.write(str(names[i])+' ')

        return encode_face()
    
    with open('names.txt', 'r') as f:
        oldNames = f.read().split()

    pic = []
    prevNames = []
    for i in range(len(oldNames)):
        pic.append(os.path.join(app.config["UPLOAD_FOLDER"], oldNames[i]+".jpg"))
        prevNames.append(oldNames[i])
    for i in range(5 - len(pic)):
        pic.append(os.path.join(app.config["UPLOAD_FOLDER"], "empty.png"))
        prevNames.append("")

    return render_template("AddSamples.html", usr_img1 = pic[0], usr_img2 = pic[1], usr_img3 = pic[2],
     usr_img4 = pic[3], usr_img5 = pic[4], text1 = prevNames[0], text2 = prevNames[1],
     text3 = prevNames[2], text4 = prevNames[3], text5 = prevNames[4])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True, use_reloader=True)
