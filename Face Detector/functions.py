import cv2
import face_recognition

names = []
faces = []


# User defined functions
def get_percentage(part, whole):
  return 100 * float(part)/float(whole)

def get_part(percent, whole):
  return (percent * whole) / 100.0

def getX(faceX, width=1280, servoDegee=180):
    return (get_part(get_percentage(faceX, width), servoDegee))

def getY(faceY, height=1024, servoDegee=180):
    return (get_part(get_percentage(faceY, height), servoDegee))

def add(name, path):
    if (name and path):
        img = name + "_image"
        enc = name + "_face_encoding"

        img = face_recognition.load_image_file(path)
        enc = face_recognition.face_encodings(img)[0]

        names.append(name)
        faces.append(enc)
    else:
        print("Invalid values!")


add("Amaraa", "img/amaraa.png")
add("Me", "img/me.png")
add("Me", "img/me2.png")
add("Uno", "img/uno.png")