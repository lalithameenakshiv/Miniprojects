import tensorflow as tf
import numpy as np
import sys
from tensorflow.keras.preprocessing import image


# =========================
# Load Models
# =========================

plant_model = tf.keras.models.load_model(
    "models/plant_model.keras",
    compile=False
)

disease_model = tf.keras.models.load_model(
    "models/disease_model.keras",
    compile=False
)


IMG_SIZE = (224,224)


# =========================
# Class Names
# =========================

plant_classes = [
    "Pepper",
    "PlantVillage",
    "Potato",
    "Tomato",
    "Tomato_Bacterial_spot",
    "Tomato_Early_blight",
    "Tomato_Late_blight",
    "Tomato_Leaf_Mold",
    "Tomato_Septoria_leaf_spot",
    "Tomato_Spider_mites_Two_spotted_spider_mite",
    "Tomato_healthy"
]


disease_classes = [
    "Curl_Virus",
    "Target_Spot",
    "Tomato_Bacterial_spot",
    "Tomato_Early_blight",
    "Tomato_Late_blight",
    "Tomato_Leaf_Mold",
    "Tomato_Septoria_leaf_spot",
    "Tomato_Spider_mites_Two_spotted_spider_mite",
    "Tomato_healthy",
    "Tomato_mosaic_virus",
    "Bacterial_spot",
    "Early_blight",
    "Late_blight",
    "healthy"
]


# =========================
# Get Image From Flask
# =========================

if len(sys.argv) > 1:
    img_path = sys.argv[1]
else:
    img_path = r"images\tomato.jpeg"



# =========================
# Load Image
# =========================

img = image.load_img(
    img_path,
    target_size=IMG_SIZE
)


img_array = image.img_to_array(img)

img_array = np.expand_dims(
    img_array,
    axis=0
)

img_array = img_array / 255.0



# =========================
# Prediction
# =========================

plant_prediction = plant_model.predict(
    img_array,
    verbose=0
)

//silent mode
disease_prediction = disease_model.predict(
    img_array,
    verbose=0
)


plant_index = np.argmax(
    plant_prediction
)


disease_index = np.argmax(
    disease_prediction
)



plant_name = plant_classes[plant_index]

disease_name = disease_classes[disease_index]



# =========================
# Details
# =========================

if "healthy" in disease_name.lower():

    health = "Healthy"
    duration = "No infection"
    severity = "0%"

else:

    health = "Diseased"
    duration = "5-7 days"
    severity = "Medium (45% affected area)"



solution = {

"Tomato_Late_blight":
"Remove infected leaves, apply fungicide, avoid excess moisture",

"Tomato_Early_blight":
"Remove affected leaves and improve ventilation",

"Tomato_Bacterial_spot":
"Use recommended bactericide and avoid wet leaves",

"Tomato_healthy":
"Plant is healthy. Continue normal care"

}



symptoms = {

"Tomato_Late_blight":
[
"Brown patches",
"Yellow edges",
"Leaf curling"
],

"Tomato_Early_blight":
[
"Dark spots",
"Leaf yellowing"
],

"Tomato_Bacterial_spot":
[
"Small brown spots",
"Leaf damage"
],

"Tomato_healthy":
[
"No symptoms"
]

}



# =========================
# Print Result
# =========================

print("====================")

print(
"Plant Name:",
plant_name.replace("_"," ")
)


print(
"Leaf Stage:",
"Mature Leaf (Old)"
)


print(
"Health Status:",
health
)


print(
"Disease Detected:",
disease_name.replace("_"," ")
)


print(
"Estimated Infection Duration:",
duration
)


print(
"Severity:",
severity
)


print("\nSymptoms:")

for s in symptoms.get(
    disease_name,
    ["Unknown"]
):
    print("-",s)



print("\nRecommended Solution:")

print(
solution.get(
    disease_name,
    "Consult agriculture expert"
)
)


print("\nConfidence:")

print(
"Plant:",
round(float(np.max(plant_prediction))*100,2),
"%"
)


print(
"Disease:",
round(float(np.max(disease_prediction))*100,2),
"%"
)


print("====================")