from keras.models import Sequential
from keras.layers import Dropout, Dense
from keras.utils import to_categorical
import numpy as np
from keras.callbacks import LearningRateScheduler
import math
import pickle
from sklearn.utils import shuffle

foram_fc_model_path = './foram_fc.h5'
# Trained model will be saved at this location
batch_size = 32 # The number of samples trained on in a batch
epochs = 60 # Number of times to iterate over total dataset

data = pickle.load(open('forams_features.p', "rb")) # Load the pickle file of the features, labels, class to label mapping, and class ids
features = np.squeeze(data['features']) # Get the features array and remove the extra dimensions
labels = data['labels'] # Extract the labels array
class_count = data['class_count'] # Extract the class_count array
features, labels = shuffle(features, labels)  # Shuffle the features and labels in unison
one_hot_labels = to_categorical(labels) # One-hot encode the labels 
label2class = data['label2class'] # Extract the label2class mapping array
feature_shape = features.shape # Get features array shape

print(feature_shape)
print(one_hot_labels.shape)
print(label2class)

foram_fc_model = Sequential() # Define a sequential model for fully connected layers
foram_fc_model.add(Dropout(0.05, input_shape=feature_shape[1:])) # Add a dropout layer with 0.05 dropout rate and set the input shape
foram_fc_model.add(Dense(512, activation='relu')) # Add a fully connected layer with 512 units and ReLu activation
foram_fc_model.add(Dropout(0.15)) # Add another dropout layer with dropout rate of 0.15
foram_fc_model.add(Dense(512, activation='relu')) # Add a fully connected layer with 512 units and ReLu activation
foram_fc_model.add(Dense(7, activation='softmax')) # This is the output layer with 7 classes and softmax activation
# The above is the model definition/ building
foram_fc_model.compile(loss='categorical_crossentropy',
                      optimizer='adam',
                      metrics=['accuracy'])
# Compile the model for training with categorical crossentropy as the loss function
initial_lrate = 1e-3 # Set learning rate 
def step_decay(epoch): # Function for lowering learning rate by 5% each epoch
  drop = 0.95
  epochs_drop = 1
  lrate = initial_lrate * math.pow(drop, math.floor((1 + epoch) / epochs_drop))
  return lrate

# learning schedule callback
lrate = LearningRateScheduler(step_decay)
foram_fc_model.fit(features, one_hot_labels,
          epochs=epochs,
          batch_size=batch_size,
          shuffle=True,
          validation_split=0.2,
          class_weight={key:1000 / class_count[key] for key in class_count},
          callbacks=[lrate])
# The above trains the model with class_weights added in 