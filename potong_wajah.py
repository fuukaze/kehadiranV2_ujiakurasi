import cv2
import time

def potong_wajah():
    # Input path gambar
    input_path = "faces/real_face/sigit.jpg"

    # Muat cascade classifier untuk deteksi wajah
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Baca gambar
    img = cv2.imread(input_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Deteksi wajah
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    for i, (x, y, w, h) in enumerate(faces):
        # Potong wajah
        face = img[y:y+h, x:x+w]

        # Nama file otomatis dengan timestamp
        timestamp = int(time.time())
        output_path = f"faces/real_face/widi_face_{i}_{timestamp}.jpg"

        # Simpan wajah
        cv2.imwrite(output_path, face)

        print(f"Wajah {i+1} berhasil dipotong dan disimpan di {output_path}")

if __name__ == "__main__":
    potong_wajah()
