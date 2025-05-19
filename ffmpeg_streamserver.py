from flask import Flask, Response
import cv2

app = Flask(__name__)

# Use FFmpeg backend to capture the RTSP stream
RTSP_URL = "rtsp://securo:iamsecuro@192.168.1.8:554/stream1"
cap = cv2.VideoCapture(RTSP_URL, cv2.CAP_FFMPEG)

def generate_frames():
    while True:
        success, frame = cap.read()
        if not success:
            continue

        frame = cv2.resize(frame, (640, 480))
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return """
    <html>
        <head><title>SECURO Cam</title></head>
        <body>
            <h2>Live Feed</h2>
            <iframe src="/video_feed" width="640" height="480" frameborder="0"></iframe>
        </body>
    </html>
    """

if __name__ == '__main__':
    # Replace 0.0.0.0 with your local IP if needed
    app.run(host='0.0.0.0', port=5000, debug=False)
