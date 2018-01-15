import cv2
import face_recognition as fr
import serial
import simpleaudio as sa
from functions import names, faces, get_part, get_percentage

# Webcam variables
webcamPort = 1
width = 640
height = 480

# Variables for keeping track of the current servo positions.
servoTiltPosition = 90
servoPanPosition = 90

port = serial.Serial('/dev/ttyUSB0', 57600)
# port = False

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(webcamPort)

# Setting the webcam resolution
video_capture.set(3, width)
video_capture.set(4, height)

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

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = fr.face_locations(small_frame)
        face_encodings = fr.face_encodings(small_frame, face_locations, 1)
        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            match = fr.compare_faces(faces, face_encoding, 0.4)
        
            name = "Anonymous"

            # Getting the name of a person in the frame 
            for index in range(0, len(match)):
                if match[index]:
                    name = names[index]
                
            face_names.append(name)
    process_this_frame = not process_this_frame

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):

        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Finding the coordinates of the center of the face
        midFaceX = int(((right - left)/2 + left))
        midFaceY = int(((bottom - top)/2 + top))
        
        # print("{}:{}".format(midFaceX, midFaceY))

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.circle(frame, (midFaceX, midFaceY), 5, (0, 255, 0), 5)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Putting the coordinates into an array
        faceXY = [midFaceX, midFaceY]

        if (faceXY):
            # Getting the degrees of the two servo motors to track the face in the frame
            unitX = get_percentage(faceXY[0], width)
            unitY = get_percentage(faceXY[1], height)

            servoPanPosition = get_part(unitX, 180)
            servoTiltPosition = get_part(unitY, 180) 

            # servoPanPosition = getX(faceXY[0], 180)
            # servoTiltPosition = getY(faceXY[1], 180) 
            
            # Checking if there's an unidentified personnel detected
            # If it's then fire else don't
            if (name == "Anonymous"):
                panPosition = str("p%3d" % (int(servoPanPosition))).encode()
                tiltPosition = str("t%3d" % (int(servoTiltPosition))).encode()
            else:   
                panPosition = str("p0%3d" % (int(servoPanPosition))).encode()
                tiltPosition = str("t0%3d" % (int(servoTiltPosition))).encode()    

            # Sending the commands to the port via serial
            port.write(panPosition)
            port.write(tiltPosition)

            # For debugging purpose
            print("Tilt || {} || Position: {}".format(tiltPosition, servoTiltPosition))
            print("Pan  || {} || Position: {}".format(panPosition, servoPanPosition))

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()

# Close the serial port
port.close()
