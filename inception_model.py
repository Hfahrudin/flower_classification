from keras.applications.inception_v3 import InceptionV3
from keras.preprocessing.image import ImageDataGenerator
from keras.layers import Input, Flatten, Dense, Dropout
from keras.models import Model
from keras import optimizers
train_data_dir = 'dataset/training_set'
validation_data_dir = 'dataset/test_set'
## other
img_width, img_height = 200, 200
nb_train_samples = 200
nb_validation_samples = 200
top_epochs = 50
fit_epochs = 50
batch_size = 24
nb_classes = 5
nb_epoch = 10

#build CNN

model_InceptionV3_conv = InceptionV3(weights='imagenet', include_top=False)

input = Input(shape=(img_width,img_height, 3),name = 'image_input')

output_vgg16_conv = model_InceptionV3_conv(input)

for layer in model_InceptionV3_conv.layers[:15]:
    layer.trainable = False
model_InceptionV3_conv.summary()

x = Flatten(name='flatten')(output_vgg16_conv)
x = Dense(256, activation='relu')(x)
x = Dropout(0.5)(x)
x = Dense(5, activation='softmax', name='predictis')(x)

inception_model = Model(inputs=input, outputs=x)

inception_model.summary()


inception_model.compile(loss='categorical_crossentropy',
              optimizer=optimizers.SGD(lr=1e-3, momentum=0.9),
              metrics=['accuracy']
)

# Setting learning data
train_datagen = ImageDataGenerator(rescale = 1./255,
                                   shear_range = 0.2,
                                   zoom_range = 0.2,
                                   horizontal_flip = True)

test_datagen = ImageDataGenerator(rescale = 1./255)

training_set = train_datagen.flow_from_directory(train_data_dir,
                                                 target_size = (img_width,img_height),
                                                 batch_size = 32,
                                                 class_mode = 'categorical')

test_set = test_datagen.flow_from_directory(validation_data_dir,
                                            target_size = (img_width,img_height),
                                            batch_size = 32,
                                            class_mode = 'categorical')

y_true_labels = training_set.class_indices

inception_model.fit_generator(
        training_set,
        steps_per_epoch=nb_train_samples,
        epochs=nb_epoch,
        validation_data=test_set,
        validation_steps=nb_validation_samples
)

#Save the model
# serialize model to JSON
my_model_json = inception_model.to_json()
with open("model_inception.json", "w") as json_file:
    json_file.write(my_model_json)
# serialize weights to HDF5
inception_model.save_weights("model_inception.h5")
print("Saved model to disk")

