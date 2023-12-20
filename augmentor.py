# import os
# import cv2
# import numpy as np

# # Path ke folder yang berisi foto-foto wajah asli
# input_folder = 'faces/real_face'  # Ganti dengan path folder Anda

# # Path ke folder tempat menyimpan hasil augmentasi
# output_folder = 'faces/real_face_augmented'  # Ganti dengan path folder output yang diinginkan
# os.makedirs(output_folder, exist_ok=True)

# def augment_image(image, label, output_folder, num_augmentations=10):
#     augmented_images = []

#     for i in range(num_augmentations):
#         augmented_image = image.copy()

#         # Flip horizontal with a 50% probability
#         if np.random.rand() < 0.5:
#             augmented_image = cv2.flip(augmented_image, 1)

#         # Rotate with a random angle between -10 and 10 degrees
#         angle = np.random.uniform(-10, 10)
#         rotation_matrix = cv2.getRotationMatrix2D((augmented_image.shape[1] // 2, augmented_image.shape[0] // 2), angle, 1.0)
#         augmented_image = cv2.warpAffine(augmented_image, rotation_matrix, (augmented_image.shape[1], augmented_image.shape[0]))

#         # Save the augmented image
#         output_file_name = f"{label}_{i + 1}.jpg"
#         output_file_path = os.path.join(output_folder, output_file_name)
#         cv2.imwrite(output_file_path, augmented_image)
#         augmented_images.append(output_file_path)

#     return augmented_images

# # Loop through each file in the input folder
# for root, dirs, files in os.walk(input_folder):
#     for file in files:
#         file_path = os.path.join(root, file)
#         label = os.path.splitext(os.path.basename(file))[0]

#         # Read the image
#         image = cv2.imread(file_path)

#         # Perform augmentation
#         augment_image(image, label, output_folder, num_augmentations=10)

# print(f"Aktivitas augmentasi selesai. Hasil disimpan di: {output_folder}")

import os
import cv2
import numpy as np
import face_recognition

# Path ke folder yang berisi foto-foto wajah asli
input_folder = 'faces/real_face'  # Ganti dengan path folder Anda

# Path ke folder tempat menyimpan hasil augmentasi
output_folder = 'faces/real_face_augmented'  # Ganti dengan path folder output yang diinginkan
os.makedirs(output_folder, exist_ok=True)

def change_image_quality(image, target_quality=95):
    # Ubah kualitas gambar ke nilai target_quality (biasanya antara 0 dan 100)
    _, img_encoded = cv2.imencode('.jpg', image, [int(cv2.IMWRITE_JPEG_QUALITY), target_quality])
    img_decoded = cv2.imdecode(img_encoded, cv2.IMREAD_COLOR)
    return img_decoded

def augment_image(image, label, output_folder, num_augmentations=10, target_quality=95):
    augmented_images = []

    # Mengubah kualitas gambar menjadi target_quality
    image = change_image_quality(image, target_quality)

    # Deteksi wajah menggunakan face_recognition
    face_locations = face_recognition.face_locations(image)

    for i in range(num_augmentations):
        # Hanya melanjutkan jika ada wajah yang terdeteksi
        if len(face_locations) > 0:
            # Memilih wajah secara acak dari wajah yang terdeteksi
            top, right, bottom, left = face_locations[np.random.choice(len(face_locations))]

            # Menambahkan beberapa ruang antara batas kotak
            padding = 20
            top -= padding
            right += padding
            bottom += padding
            left -= padding

            # Memastikan kotak pembatas tetap dalam batas gambar
            top = max(0, top)
            right = min(image.shape[1], right)
            bottom = min(image.shape[0], bottom)
            left = max(0, left)

            # Membuat salinan gambar yang akan di-augmentasi
            augmented_image = image.copy()

            # Menjalankan augmentasi lain seperti flip dan rotasi
            # ...

            # Simpan gambar hasil augmentasi
            output_file_name = f"{label}_{i + 1}.jpg"
            output_file_path = os.path.join(output_folder, output_file_name)
            cv2.imwrite(output_file_path, augmented_image[top:bottom, left:right])
            augmented_images.append(output_file_path)

    return augmented_images

# Loop through each file in the input folder
for root, dirs, files in os.walk(input_folder):
    for file in files:
        file_path = os.path.join(root, file)
        label = os.path.splitext(os.path.basename(file))[0]

        # Read the image
        image = cv2.imread(file_path)

        # Perform augmentation with quality adjustment and face detection
        augment_image(image, label, output_folder, num_augmentations=10, target_quality=95)

print(f"Aktivitas augmentasi selesai. Hasil disimpan di: {output_folder}")
