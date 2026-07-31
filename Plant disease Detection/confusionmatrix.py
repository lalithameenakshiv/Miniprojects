import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import confusion_matrix
import seaborn as sns


# Load model
model = tf.keras.models.load_model(
    "models/disease_model.keras",
    compile=False
)


IMG_SIZE = (224,224)
BATCH = 32


# Dataset path
test_path = "dataset/disease"


# Load test images
datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2
)


test_data = datagen.flow_from_directory(
    test_path,
    target_size=IMG_SIZE,
    batch_size=BATCH,
    class_mode="categorical",
    shuffle=False,
    subset="validation"
)



# Prediction
pred = model.predict(test_data)


y_pred = np.argmax(pred, axis=1)

y_true = test_data.classes



# Confusion matrix

cm = confusion_matrix(
    y_true,
    y_pred
)



labels = list(test_data.class_indices.keys())



plt.figure(figsize=(12,10))


sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    xticklabels=labels,
    yticklabels=labels
)


plt.xlabel("Predicted")

plt.ylabel("Actual")

plt.title("Plant Disease Confusion Matrix")


plt.savefig(
    "confusion_matrix.png"
)


plt.show()


print("Confusion matrix saved successfully")