#https://circuitdigest.com/microcontroller-projects/driver-drowsiness-detector-using-raspberry-pi-and-opencv
import face_recognition
import cv2
import numpy as np
import time
import cv2
import eye_game
import RPi.GPIO as GPIO
import sys

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
BUZZER= 23
GPIO.setup(BUZZER, GPIO.OUT)
previous ="Unknown"
count=0
video_capture = cv2.VideoCapture(0)
#frame = (video_capture, file)
file = 'laks1.jpg'
# Load a sample picture and learn how to recognize it.
img_image = face_recognition.load_image_file('laks.jpg')

try:
    img_face_encoding = face_recognition.face_encodings(img_image)[0]
except IndexError as e:
    print(e)
    sys.exit(1) # stops code execution in my case you could handle it differently
    

#img_face_encoding = face_recognition.face_encodings(img_image)[0]
# Create arrays of known face encodings and their names
known_face_encodings = [
    img_face_encoding   
]

known_face_names = [
    "Laks"
]


# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
while True:
    # Grab a single frame of video    
    ret, frame = video_capture.read()    
    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)   
    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]
    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        cv2.imwrite(file, small_frame)
        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"            
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]                
                result= image_preprocessing(file)
                print(result)
                #direction = eye_game.api.get_eyeball_direction(cv_image_array)
                direction = eye_game.interpret_result_direction(result)
                if previous != direction:
                    previous=direction                  
                else:
                    print("old same")
                    count=1+count
                    print(count)
                    if (count>=10):
                       #GPIO.output(BUZZER, GPIO.HIGH)
                       print("Driver is asleep")
                       time.sleep(2)
                       #GPIO.output(BUZZER, GPIO.LOW)
                       print("Alert!! Alert!! Driver Drowsiness Detected")
                       cv2.putText(frame, "DROWSINESS ALERT!", (10, 30),

cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            face_names.append(name)         
    process_this_frame = not process_this_frame
    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (0, 0, 255), 1)
        #cv2.putText(frame, frame_string, (left + 10, top - 10), font, 1.0, (255, 255, 255), 1)
    # Display the resulting image
    cv2.imshow('Video', frame)
    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()