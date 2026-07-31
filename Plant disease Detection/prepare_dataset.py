import os
import shutil


source = "dataset/raw"

plant_folder = "dataset/plant"
disease_folder = "dataset/disease"


os.makedirs(plant_folder, exist_ok=True)
os.makedirs(disease_folder, exist_ok=True)


for folder in os.listdir(source):

    folder_path = os.path.join(source, folder)

    # skip folders inside raw
    if not os.path.isdir(folder_path):
        continue

    # if PlantVillage folder exists, go inside it
    if folder == "PlantVillage":

        for subfolder in os.listdir(folder_path):

            folder_path2 = os.path.join(folder_path, subfolder)

            if os.path.isdir(folder_path2):

                process_folder = subfolder
                image_path = folder_path2

                parts = process_folder.split("__")

                plant = parts[0]
                disease = parts[-1]


                plant_path = os.path.join(
                    plant_folder, plant
                )

                disease_path = os.path.join(
                    disease_folder, disease
                )

                os.makedirs(plant_path, exist_ok=True)
                os.makedirs(disease_path, exist_ok=True)


                for image in os.listdir(image_path):

                    img = os.path.join(
                        image_path,
                        image
                    )

                    shutil.copy(img, plant_path)
                    shutil.copy(img, disease_path)



print("Dataset preparation completed")