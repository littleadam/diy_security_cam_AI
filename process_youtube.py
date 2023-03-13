def main():
    # Download YouTube video
    download_youtube_video(YOUTUBE_URL, 'video.mp4')

    # Load known faces
    known_faces, known_names = load_known_faces(KNOWN_FACES_DIR)

    # Load unknown faces
    unknown_faces, unknown_times = load_unknown_faces(UNKNOWN_FACES_DIR)

    # Initialize face recognition model
    model = load_face_model()

    # Process video file
    process_video_file('video.mp4', known_faces, known_names, unknown_faces, unknown_times, model)

    # Save unknown faces
    save_unknown_faces(UNKNOWN_FACES_DIR, unknown_faces, unknown_times)


if __name__ == '__main__':
    main()
