from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, \
    Activation, Dropout, Flatten, Dense

N_SCREENS = 15
IMAGE_SHAPE = (100, 100)

model = Sequential()
model.add(Conv2D(32, (3, 3), input_shape=(3, ) + IMAGE_SHAPE))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(32, (3, 3)))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(32, (3, 3)))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(64))
model.add(Activation("relu"))
model.add(Dropout(0.5))
model.add(Dense(N_SCREENS))
model.add(Activation("softmax"))

model.compile(
    loss="categorical_crossentropy",
    optimizer="rmsprop",
    metrics=["accuracy"])

batch_size = 16

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
    batch_size=batch_size,
    class_mode="categorical")

validation_generator = validation_datagen.flow_from_directory(
    "dataset/validation",
    target_size=IMAGE_SHAPE,
    batch_size=batch_size,
    class_mode="categorical")

print("indices: " + str(train_generator.class_indices))

model.fit_generator(
    train_generator,
    steps_per_epoch=1000 // batch_size,
    epochs=10,
    validation_data=validation_generator,
    validation_steps=500 // batch_size,
    verbose=1)

model.save("model.h5")
