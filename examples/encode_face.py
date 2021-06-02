import face_recognition
import pickle

f = open('names.txt', 'r')
names = f.read().split()
f.close()

all_face_encodings = {}

try:
    img1 = face_recognition.load_image_file(names[0]+".jpg")
    all_face_encodings[names[0]] = face_recognition.face_encodings(img1)[0]
except IndexError: pass

try:
    img2 = face_recognition.load_image_file(names[1]+".jpg")
    all_face_encodings[names[1]] = face_recognition.face_encodings(img2)[0]
except IndexError: pass

try:
    img3 = face_recognition.load_image_file(names[2]+".jpg")
    all_face_encodings[names[2]] = face_recognition.face_encodings(img3)[0]
except IndexError: pass

try:
    img4 = face_recognition.load_image_file(names[3]+".jpg")
    all_face_encodings[names[3]] = face_recognition.face_encodings(img4)[0]
except IndexError: pass

try:
    img5 = face_recognition.load_image_file(names[4]+".jpg")
    all_face_encodings[names[4]] = face_recognition.face_encodings(img5)[0]
except IndexError: pass

# ... etc ...

with open('data/dataset_faces.dat', 'wb') as f:
    pickle.dump(all_face_encodings, f)
