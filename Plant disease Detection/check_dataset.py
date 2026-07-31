import os

path = "dataset/raw"

for folder in os.listdir(path):

    folder_path = os.path.join(path, folder)

    if os.path.isdir(folder_path):
        print(folder, ":", len(os.listdir(folder_path)), "images")