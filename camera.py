import cv2
import os
import numpy as np
import threading

# Configuration
XML_PATH = 'xml/haarcascade_frontalface_default.xml'
DATASET_PATH = 'DataSet'
RTSP_URL = "rtsp://securo:iamsecuro@192.168.1.8:554/stream1"

# Load face cascade
face_cascade = cv2.CascadeClassifier(XML_PATH)

# Load recognizer if dataset exists
recognizer = cv2.face.LBPHFaceRecognizer_create()
label_ids = {}

if os.path.exists(DATASET_PATH):
    def get_dataset(dataset_path):
        faces = []
        labels = []
        label_ids_local = {}
        current_id = 0

        for root, dirs, files in os.walk(dataset_path):
            for file in files:
                if file.endswith("jpg") or file.endswith("png"):
                    path = os.path.join(root, file)
                    label = os.path.basename(root).replace(" ", "-").lower()

                    if label not in label_ids_local:
                        label_ids_local[label] = current_id
                        current_id += 1

                    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                    face = face_cascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=5)
                    for (x, y, w, h) in face:
                        face_img = img[y:y+h, x:x+w]
                        faces.append(face_img)
                        labels.append(label_ids_local[label])

        return faces, labels, label_ids_local

    faces, labels, label_ids = get_dataset(DATASET_PATH)
    recognizer.train(faces, np.array(labels))
    recognizer.save("trained_model.yml")
    print("Training complete!")

else:
    print("Dataset not found. Running only face detection.")

# Threaded video capture
class VideoCaptureThread:
    def __init__(self, src):
        self.cap = cv2.VideoCapture(src)
        self.ret, self.frame = self.cap.read()
        self.running = True
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        while self.running:
            self.ret, self.frame = self.cap.read()

    def read(self):
        return self.ret, self.frame

    def stop(self):
        self.running = False
        self.thread.join()
        self.cap.release()

# Start threaded capture
video = VideoCaptureThread(RTSP_URL)

while True:
    ret, frame = video.read()
    if not ret:
        continue

    frame = cv2.resize(frame, (640, 480))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        if os.path.exists("trained_model.yml"):
            id_, confidence = recognizer.predict(roi_gray)
            if confidence < 100:
                name = list(label_ids.keys())[list(label_ids.values()).index(id_)]
                print(f"Recognized: {name} ({round(100 - confidence)}%)")
            else:
                print("Unknown")

    cv2.imshow("Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.stop()
cv2.destroyAllWindows()
