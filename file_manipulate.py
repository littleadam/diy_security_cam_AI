import os
import face_recognition
import datetime
import string
import random
import cv2

def load_known_faces():
    known_faces_dir = "known_faces"
    known_faces = []
    known_face_names = []

    if os.path.exists(known_faces_dir):
        for file in os.listdir(known_faces_dir):
            image_path = os.path.join(known_faces_dir, file)
            image = face_recognition.load_image_file(image_path)
            face_encoding = face_recognition.face_encodings(image)[0]
            known_faces.append(face_encoding)
            known_face_names.append(os.path.splitext(file)[0])

    return known_faces, known_face_names

def load_unknown_faces():
    unknown_faces_dir = "unknown_faces"
    unknown_faces = []
    unknown_face_names = []

    if os.path.exists(unknown_faces_dir):
        for file in os.listdir(unknown_faces_dir):
            image_path = os.path.join(unknown_faces_dir, file)
            image = face_recognition.load_image_file(image_path)
            face_encoding = face_recognition.face_encodings(image)[0]
            unknown_faces.append(face_encoding)
            unknown_face_names.append(os.path.splitext(file)[0])

    return unknown_faces, unknown_face_names

def save_unknown_face(frame):
    unknown_faces_dir = "unknown_faces"

    if not os.path.exists(unknown_faces_dir):
        os.makedirs(unknown_faces_dir)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    rand_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    file_name = f"{timestamp}_{rand_id}.jpg"
    file_path = os.path.join(unknown_faces_dir, file_name)
    cv2.imwrite(file_path, frame)
