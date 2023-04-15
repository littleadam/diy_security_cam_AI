# The code is an implementation of a facial recognition system that uses the OpenCV and face_recognition libraries to detect faces in a video stream or file, recognize them by comparing their facial features with a database of known faces, and save their names and timestamps to a database.
# The code first loads the face detection and recognition models and then opens a video stream or file. For each frame in the video, the code detects any faces present and encodes their facial features using the face_recognition library. It then compares the encoded face features with a database of known faces to determine if the face is recognized or unknown.
# If the face is recognized, the code retrieves the name associated with the face from the database and adds the current timestamp to the list of timestamps for that face in the database. If the face is unknown, the code prompts the user to suggest a name for the person and adds the new face and timestamp to the database with the suggested name.
# The code also displays the video stream with the recognized faces labeled with their names and timestamps, and saves the video with the labeled frames to a file.

import cv2
import face_recognition
import numpy as np
import datetime

# Load a sample picture and learn how to recognize it.
known_image = face_recognition.load_image_file("known_image.jpg")
known_encoding = face_recognition.face_encodings(known_image)[0]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
timestamps = []

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame to 50%
    small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    # Get timestamp of current frame
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    for face_encoding, face_location in zip(face_encodings, face_locations):
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces([known_encoding], face_encoding, tolerance=0.5)

        # If a match was found in the known_faces, add the current timestamp to the existing timestamps
        if True in matches:
            first_match_index = matches.index(True)
            name = "Known Person"
            timestamps.append(current_time)

            # If the same face is present in adjacent frames, save only the timestamps of the first frame with the face
            # and the last continuous frame with the face
            if len(timestamps) > 1 and timestamps[-2] == timestamps[-1]:
                prev_faces_time = timestamps.pop()
                while len(timestamps) > 1 and timestamps[-2] == prev_faces_time:
                    timestamps.pop()
                timestamps[-1] = '-' + str(prev_faces_time)

        # If no match was found in the known_faces, ask the user for a name suggestion
        else:
            name = "Unknown Person"
            cv2.imshow('Unknown Face', small_frame)
            suggestion = input("Please provide a name suggestion for the unknown person: ")
            if suggestion:
                name = suggestion

            # Save the facial encoding and name in the database
            known_encoding = np.concatenate((known_encoding, face_encoding), axis=None)
            face_names.append(name)
            timestamps.append(current_time)

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/2 size
        top *= 2
        right *= 2
        bottom *= 2
        left *= 2

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

       # Draw a label with the name below the face
cv2.rectangle(frame, (left, bottom - 25), (right, bottom), (0, 0, 255), cv2.FILLED)
font = cv2.FONT_HERSHEY_DUPLEX
cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

# Check if the face is unknown
if name == 'unknown':
    # Ask the user for a name suggestion
    suggested_name = input("Unknown face detected. Please suggest a name for the person: ")

    # Add the new face and timestamp to the database
    face_encoding = face_recognition.face_encodings(face_image)[0]
    db.append({'name': suggested_name, 'encoding': face_encoding, 'timestamps': [timestamp]})
    print("Face added to database with name:", suggested_name)

else:
    # If the facial image is in the database, add the current timestamp to the existing timestamps
    for i in range(len(db)):
        if face_recognition.compare_faces([db[i]['encoding']], face_encoding, tolerance=0.6)[0]:
            db[i]['timestamps'].append(timestamp)
            print("Timestamp added to existing entry in the database")
            break

    # If the facial image is not in the database, add it to the database with the current timestamp
    else:
        db.append({'name': name, 'encoding': face_encoding, 'timestamps': [timestamp]})
        print("New entry added to database with name:", name)

