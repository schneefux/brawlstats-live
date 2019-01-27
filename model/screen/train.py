from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.callbacks import ModelCheckpoint
from keras.layers import Conv2D, MaxPooling2D, \
    Activation, BatchNormalization, Dropout, Flatten, Dense
from keras.backend import image_data_format

from config import shape, feature_map

SAMPLES = 5000
VALIDATION_RATIO = 0.2
N_SCREENS = 26
IMAGE_SHAPE = shape
BATCH_SIZE = 16
EPOCHS = 10

channels_first = image_data_format() == "channels_first"
channel_dim = 1 if channels_first else -1
input_shape = (3, ) + IMAGE_SHAPE if channels_first \
    else IMAGE_SHAPE + (3, )

model = Sequential()

model.add(Conv2D(32, (3, 3), input_shape=input_shape))
model.add(BatchNormalization(axis=channel_dim))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(128))
model.add(Activation("relu"))
model.add(BatchNormalization(axis=channel_dim))
model.add(Dropout(0.5))

model.add(Dense(N_SCREENS))
model.add(Activation("softmax"))

model.compile(
    loss="categorical_crossentropy",
    optimizer="rmsprop",
    metrics=["accuracy"])

train_datagen = ImageDataGenerator(
    width_shift_range=0.2,
    height_shift_range=0.2,
    rescale=1.0/255, # 0-255 to 0.0-1.0
    zoom_range=0.2,
    fill_mode="nearest")

validation_datagen = ImageDataGenerator(rescale=1.0/255)

train_generator = train_datagen.flow_from_directory(
    "dataset/train",
    target_size=IMAGE_SHAPE,
    batch_size=BATCH_SIZE,
    shuffle=True,
    class_mode="categorical")

validation_generator = validation_datagen.flow_from_directory(
    "dataset/validation",
    target_size=IMAGE_SHAPE,
    batch_size=BATCH_SIZE,
    shuffle=True,
    class_mode="categorical")

print("indices: " + str(train_generator.class_indices))

checkpoint = ModelCheckpoint("model_checkpoint.h5",
    monitor="val_acc", verbose=1, save_best_only=True, mode="max")

model.fit_generator(
    train_generator,
    steps_per_epoch=(1.0-VALIDATION_RATIO) * SAMPLES // BATCH_SIZE,
    epochs=EPOCHS,
    validation_data=validation_generator,
    validation_steps=VALIDATION_RATIO * SAMPLES // BATCH_SIZE,
    callbacks=[checkpoint],
    verbose=1)
