import os
import random
import numpy as np
import cv2
from imutils import paths
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import RMSprop
from keras.applications.inception_v3 import InceptionV3
import tensorflow.keras.layers as layers
from keras.models import Model
from matplotlib import pyplot as plt
import tensorflow as tf

# Check GPU availability
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
if len(tf.config.list_physical_devices('GPU')) == 0:
    raise SystemError('GPU device not found')

# Define path to data and list of cat breeds
data_path = "dataset"
breeds = ["Abyssinian", "Bengal", "Birman", "Bombay",
          "British_Shorthair", "Egyptian_Mau", "Maine_Coon",
          "Persian", "Ragdoll", "Russian_Blue", "Siamese", "Sphynx"]

# Initialize lists for storing images and labels
data = []
labels = []

# Collect all image paths and shuffle them
image_paths = sorted(list(paths.list_images(data_path)))
if not image_paths:
    raise ValueError(f"No images found in the directory: {data_path}")
random.shuffle(image_paths)

# Load images, resize them, and add to data and labels lists
for image_path in image_paths:
    image = cv2.imread(image_path)
    if image is None:
        print(f"Warning: Failed to load image: {image_path}")
        continue
    image = cv2.resize(image, (150, 150))
    data.append(image)
    label = image_path.split(os.path.sep)[-2]
    labels.append(label)

# Check if any images were loaded
if len(data) == 0 or len(labels) == 0:
    raise ValueError("No images were loaded. Please check the image paths and formats.")

# Convert lists to NumPy arrays and normalize the images
data = np.array(data, dtype="float32") / 255.0
labels = np.array(labels)

# Split data into training and test sets
(trainX, testX, trainY, testY) = train_test_split(data, labels, test_size=0.25, random_state=52)

# Display examples of images from the training set
num_images_to_show = min(len(trainX), 16)
plt.figure(figsize=(12, 12))
for i in range(num_images_to_show):
    plt.subplot(4, 4, i + 1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(trainX[i], cmap=plt.cm.binary)
    plt.xlabel(f'Breed: {trainY[i]}')
plt.show()

# Encode labels using One-Hot Encoding
enc = OneHotEncoder()
trainY = enc.fit_transform(trainY.reshape(-1, 1)).toarray()
testY = enc.transform(testY.reshape(-1, 1)).toarray()

# Create a data generator for data augmentation
train_datagen = ImageDataGenerator(
    rotation_range=30, width_shift_range=0.1, height_shift_range=0.1,
    shear_range=0.2, zoom_range=0.2, horizontal_flip=True,
    fill_mode="nearest"
)

# Function to display accuracy and loss graphs
def show_accuracy_and_loss(history):
    # Display the graph of model loss
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.title('Model Loss')
    plt.legend()
    plt.show()

    # Display the graph of model accuracy
    plt.plot(history.history['accuracy'], label='Training Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.title('Model Accuracy')
    plt.legend()
    plt.show()

# Function to train the model
def train_model():
    # Load pre-trained InceptionV3 model without the top layers
    pretrained_model = InceptionV3(input_shape=trainX[0].shape, include_top=False, weights='imagenet')
    for layer in pretrained_model.layers:
        layer.trainable = False

    # Add custom layers on top of the pre-trained model
    x = layers.Flatten()(pretrained_model.output)
    x = layers.Dense(1024, activation='relu')(x)
    x = layers.Dropout(0.2)(x)
    x = layers.Dense(trainY.shape[1], activation='sigmoid')(x)

    # Create and compile the model
    inception_model = Model(inputs=pretrained_model.input, outputs=x)
    inception_model.compile(optimizer=RMSprop(learning_rate=0.001), loss="categorical_crossentropy", metrics=["accuracy"])

    # Train the model
    history = inception_model.fit(train_datagen.flow(trainX, trainY), validation_data=(testX, testY), epochs=20)

    # Display accuracy and loss graphs
    show_accuracy_and_loss(history)

    # Save the model
    inception_model.save('InceptionV3.h5')
    return inception_model

# Train the model and evaluate its accuracy
model = train_model()
# model = tf.keras.models.load_model('InceptionV3.h5') # Uncomment if you want to load the model instead of training

test_loss, test_acc = model.evaluate(testX, testY)  # Evaluate the model on the test set

# Generate predictions on the test images
predictions = model.predict(testX)

print(f'Test accuracy: {test_acc}')
print(f'Test loss: {test_loss}')

# Display predictions on test images
num_images_to_show = min(len(testX), 16)
plt.figure(figsize=(12, 12))
for i in range(num_images_to_show):
    plt.subplot(4, 4, i + 1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(testX[i], cmap=plt.cm.binary)
    plt.xlabel(f"Breed: Predicted - {breeds[np.argmax(predictions[i])]} \nActual - {breeds[np.argmax(testY[i])]}")
plt.show()
