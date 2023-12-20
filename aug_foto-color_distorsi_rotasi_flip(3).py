import os
from tqdm import tqdm
import cv2
import numpy as np

def load_image(file_path):
    return cv2.imread(file_path)

def save_image(image, output_dir, prefix, index):
    filename = f"{prefix}_{index + 1}.jpg"
    output_path = os.path.join(output_dir, filename)
    cv2.imwrite(output_path, image)

def elastic_distortion(image, alpha=20, sigma=5):
    shape = image.shape[:2]
    grid_x, grid_y = np.meshgrid(np.arange(shape[1]), np.arange(shape[0]))
    dx = alpha * cv2.GaussianBlur((np.random.rand(*shape) * 2 - 1).astype(np.float32), (sigma, sigma), 0)
    dy = alpha * cv2.GaussianBlur((np.random.rand(*shape) * 2 - 1).astype(np.float32), (sigma, sigma), 0)
    new_x, new_y = grid_x + dx, grid_y + dy
    new_x, new_y = np.clip(new_x, 0, shape[1] - 1), np.clip(new_y, 0, shape[0] - 1)
    distorted_image = cv2.remap(image, new_x.astype(np.float32), new_y.astype(np.float32), interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    return distorted_image

def change_color(image):
    # Create a random color transformation matrix
    color_matrix = np.random.rand(3, 3)
    # Apply the color transformation to the image
    colored_image = cv2.transform(image, color_matrix)
    return colored_image

def rotate_image(image, angle):
    rows, cols = image.shape[:2]
    rotation_matrix = cv2.getRotationMatrix2D((cols/2, rows/2), angle, 1)
    return cv2.warpAffine(image, rotation_matrix, (cols, rows))

def flip_image(image, flip_direction):
    return cv2.flip(image, flip_direction)

def augment_and_save(input_image, output_directory, output_prefix):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for i in tqdm(range(60), desc='Augmenting images', unit='image'):
        # Acak apakah akan di-transpose atau tidak
        transpose_prob = np.random.uniform(0, 1)
        if transpose_prob > 0.5:
            input_image = cv2.transpose(input_image)

        # Variasi warna saja, distorsi elastis saja, atau keduanya
        color_prob = np.random.uniform(0, 1)
        elastic_prob = np.random.uniform(0, 1)

        if color_prob < 0.33:
            augmented_image = change_color(input_image)
        elif elastic_prob < 0.5:
            augmented_image = elastic_distortion(input_image)
        else:
            color_augmented = change_color(input_image)
            augmented_image = elastic_distortion(color_augmented)

        # Rotasi gambar
        rotation_angle = np.random.uniform(-20, 20)
        rotated_image = rotate_image(augmented_image, rotation_angle)

        # Kemungkinan flipping setelah rotasi
        flip_prob = np.random.uniform(0, 1)
        if flip_prob > 0.5:
            flip_direction = np.random.choice([-1, 1])  # -1 untuk horizontal, 1 untuk vertikal
            rotated_image = flip_image(rotated_image, flip_direction)

        # Simpan gambar hasil augmentasi
        save_image(rotated_image.astype(np.uint8), output_directory, output_prefix, i)

if __name__ == "__main__":
    input_image_path = "faces/real_face/aziz.jpg"
    output_directory = "faces/augmented/aziz"
    output_prefix = "augmented"

    input_image = load_image(input_image_path)
    augment_and_save(input_image, output_directory, output_prefix)
