import cv2
import face_recognition
import datetime
import os

# Define the path to the directory containing the images of known faces
known_faces_dir = "known_faces"

# Load the images of the known faces
known_face_encodings = []
known_face_names = []
for filename in os.listdir(known_faces_dir):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        image_path = os.path.join(known_faces_dir, filename)
        image = face_recognition.load_image_file(image_path)
        encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(encoding)
        known_face_names.append(os.path.splitext(filename)[0])

# Initialize the video capture object
video_capture = cv2.VideoCapture(0)

# Set the width and height of the video stream
width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Set the dimensions of the live stream window
stream_width = int(width / 4)
stream_height = int(height / 4)

# Set up the face detection model
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    # Capture a single frame from the video stream
    ret, frame = video_capture.read()

    # Resize the frame to make it smaller and faster to process
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known faces
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

            # Use the first match found
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
            else:
                name = "Unknown"

                # Get the distance between the unknown face and all the known faces
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)

                # Get the top 5 closest matches
                closest_matches = face_distances.argsort()[:5]

                # Print the names of the top 5 closest matches
                for i in closest_matches:
                    print("Close match found with", known_face_names[i], "with distance", face_distances[i])

            face_names.append(name)

    process_this_frame = True

    # Display the live stream in the top-left corner of the screen, taking up 25% of the width and height
    stream_frame = cv2.resize(frame, (stream_width, stream_height))
    cv2.imshow('Video', stream_frame)

    # Check for a key press and exit if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all windows
video_capture.release()
cv2.destroyAllWindows()
