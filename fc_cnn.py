import face_recognition
import dlib
import cv2
import os

path = 'iamge'
images = []
classNames = []
myList = os.listdir(path)
print(myList)

# Set up dlib to use CUDA for GPU acceleration if available
dlib.DLIB_USE_CUDA = True

# Load your test data and ground truth
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)

correct_predictions = 0

for i, images in enumerate(images):
    # Find face locations using the CNN model
    face_locations = face_recognition.face_locations(images, model="cnn")

    if len(face_locations) > 0:
        # Assume only one face per image for simplicity
        face_location = face_locations[0]
        face_encoding = face_recognition.face_encodings(images, [face_location])[0]

        # Perform face recognition (compare with known faces)
        results = face_recognition.compare_faces(known_face_encodings, face_encoding)

        # Check if the prediction matches ground truth
        if True in results and known_names[results.index(True)] == classNames[i]:
            correct_predictions += 1

# Calculate accuracy
accuracy = correct_predictions / len(images)
print(f"Accuracy: {accuracy * 100:.2f}%")
