import face_recognition, cv2, os, pygame, torch
from gtts import gTTS

# Load the known images
directory_path = "ml_model/dataset/face_recognition/"  # Adjust this path to your directory

known_face_encodings = []
known_face_names = []
person = ""

def speak(text):
    """Convert text to speech and play it."""
    tts = gTTS(text=text, lang='en')
    tts.save("temp_audio.mp3")
    pygame.mixer.init()
    pygame.mixer.music.load("temp_audio.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue

for filename in os.listdir(directory_path):
    if filename.endswith(".jpg") or filename.endswith(".png"):  # You can add more file types if needed
        image_path = os.path.join(directory_path, filename)
        image = face_recognition.load_image_file(image_path)
        face_encoding = face_recognition.face_encodings(image)[0]
        
        known_face_encodings.append(face_encoding)
        
        # Get the name from the filename without the extension
        person_name = os.path.splitext(filename)[0]
        known_face_names.append(person_name)

# Start the webcam
video_capture = cv2.VideoCapture(0)

while True:
    # Capture each frame from the webcam
    ret, frame = video_capture.read()

    # Find all face locations and face encodings in the current frame
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):

        distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = distances.argmin()
        confidence_score = 1 - distances[best_match_index]
        
        # Use a threshold (e.g., 0.6) to determine if the match is strong enough
        if confidence_score > 0.5:
            name = f"{known_face_names[best_match_index]} - {confidence_score * 100:.2f}%"
            if person != known_face_names[best_match_index]:
                speak(f"Hello, {known_face_names[best_match_index]}!")
            
            person=known_face_names[best_match_index]
        else:
            person="Unknown"
            name = f"Unknown - {confidence_score * 100:.2f}%"
        # Draw a rectangle around the face and display the name
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

    # Display the frame with the face(s) and name(s)
    cv2.imshow('Video', frame)

    # Press 'q' to quit the video window
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()