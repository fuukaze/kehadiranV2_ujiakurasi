from PIL import Image
import os

def resize_images(folder_path, output_folder, new_size=(250, 250)):
    # Membuat folder output jika belum ada
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Melakukan iterasi pada setiap file di dalam folder input
    for filename in os.listdir(folder_path):
        input_path = os.path.join(folder_path, filename)
        output_path = os.path.join(output_folder, filename)

        try:
            # Membuka gambar
            with Image.open(input_path) as img:
                # Mengubah ukuran gambar
                img_resized = img.resize(new_size)
                # Menyimpan gambar yang sudah diubah ukurannya
                img_resized.save(output_path)
        except Exception as e:
            print(f"Gagal mengubah ukuran gambar {filename}: {str(e)}")

if __name__ == "__main__":
    # Ganti folder_path dengan path folder tempat gambar-gambar berada
    folder_path = "faces"
    
    # Ganti output_folder dengan path folder tempat menyimpan gambar yang sudah diubah ukurannya
    output_folder = "faces/test"

    # Panggil fungsi resize_images
    resize_images(folder_path, output_folder)
