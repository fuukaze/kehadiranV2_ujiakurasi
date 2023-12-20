import os
import shutil

source_folder = 'lfw_funneled'
destination_folder = 'faces/somedata'

# Mengecek apakah folder destinasi sudah ada, jika belum akan membuatnya
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

# Fungsi untuk menyalin file dari satu folder ke folder lain
def copy_files(src, dest):
    for foldername, dest, filenames in os.walk(src):
        for filename in filenames:
            source_path = os.path.join(foldername, filename)
            destination_path = os.path.join(dest, filename)
            shutil.copy(source_path, destination_path)

# Menyalin file dari folder sumber ke folder tujuan
copy_files(source_folder, destination_folder)

print("Files copied successfully.")
