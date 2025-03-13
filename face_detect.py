# STARTING POINT FOR PROJECT
# Import necessary libraries
import cv2
import face_recognition
import sqlite3

# Connect to the database
conn = sqlite3.connect('face_recognition.db')
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY, name TEXT, encoding BLOB)''')

# Initialize the camera
video_capture = cv2.VideoCapture(0)

def get_face_encodings(frame):
    rgb_frame = frame[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    return face_encodings

def register_user(name, encoding):
    c.execute("INSERT INTO users (name, encoding) VALUES (?, ?)", (name, encoding))
    conn.commit()

def recognize_faces(frame):
    encodings = get_face_encodings(frame)
    for encoding in encodings:
        c.execute("SELECT name, encoding FROM users")
        users = c.fetchall()
        for user in users:
            name, db_encoding = user
            matches = face_recognition.compare_faces([db_encoding], encoding)
            if True in matches:
                print(f"Recognized {name}")

while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    # Display the resulting frame
    cv2.imshow('Video', frame)

    # Recognize faces in the frame
    recognize_faces(frame)

    # Register a new user (this should be done through some user interface)
    # Example: register_user('John Doe', get_face_encodings(frame)[0])

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the connection
video_capture.release()
cv2.destroyAllWindows()
conn.close()
