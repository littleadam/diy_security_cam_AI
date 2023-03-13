def main(video_file_path):
    # Load known faces
    known_faces, known_names = load_known_faces(KNOWN_FACES_DIR)

    # Load unknown faces
    unknown_faces, unknown_times = load_unknown_faces(UNKNOWN_FACES_DIR)

    # Initialize face recognition model
    model = load_face_model()

    # Process video file
    process_video_file(video_file_path, known_faces, known_names, unknown_faces, unknown_times, model)

    # Save unknown faces
    save_unknown_faces(UNKNOWN_FACES_DIR, unknown_faces, unknown_times)


if __name__ == '__main__':
    # Replace the VIDEO_FILE_PATH with the absolute file path of the video file
    VIDEO_FILE_PATH = "/path/to/video.mp4"
    main(VIDEO_FILE_PATH)
