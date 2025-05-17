import cv2
import os
import numpy as np

# Path to the dataset folder (make sure you have the images inside folders named after people)
dataset_path = "DataSet"

# Initialize lists for known faces and names
known_face_encodings = []
known_face_names = []

# Load Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load dataset (images of each person)
for person_name in os.listdir(dataset_path):
    person_folder = os.path.join(dataset_path, person_name)
    if not os.path.isdir(person_folder):  # Skip if not a directory
        continue
    for image_name in os.listdir(person_folder):
        image_path = os.path.join(person_folder, image_name)
        image = cv2.imread(image_path)

        # Convert the image to grayscale (required for face detection)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect faces in the image
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        for (x, y, w, h) in faces:
            # Crop the face region
            face_image = image[y:y + h, x:x + w]
            
            # Resize face to a fixed size (100x100)
            face_image_resized = cv2.resize(face_image, (100, 100))

            # Append the resized face and the person's name to the lists
            known_face_encodings.append(face_image_resized)
            known_face_names.append(person_name)

# Initialize video capture (use 0 for the default laptop camera)
video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not video_capture.isOpened():
    print("Failed to grab frame.")
    exit()

while True:
    ret, frame = video_capture.read()
    if not ret:
        print("Failed to grab frame.")
        break

    # Resize frame to 480x480
    frame = cv2.resize(frame, (480, 480))

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the current frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    for (x, y, w, h) in faces:
        # Crop the face from the current frame
        face_image = frame[y:y + h, x:x + w]

        # Resize the detected face to match the size of stored faces
        face_image_resized = cv2.resize(face_image, (100, 100))

        # Compare the detected face with the known faces in the dataset
        best_match_index = -1
        min_distance = float('inf')

        for idx, known_face in enumerate(known_face_encodings):
            # Compare the detected face with the known face using Mean Squared Error (MSE)
            distance = np.sum((face_image_resized - known_face) ** 2)  # Simple difference metric
            if distance < min_distance:
                min_distance = distance
                best_match_index = idx

        # If a match is found, display the name of the person
        if best_match_index != -1 and min_distance < 1000000:  # Threshold for matching
            name = known_face_names[best_match_index]
        else:
            name = "Unknown"

        # Draw a rectangle around the face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # Put the name text below the rectangle
        cv2.putText(frame, name, (x + 2, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # Display the resulting frame
    cv2.imshow('SECURO Camera', frame)

    # Press 'q' to exit the video stream
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close the window
video_capture.release()
cv2.destroyAllWindows()
