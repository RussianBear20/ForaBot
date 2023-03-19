from keras.applications import resnet50
from keras.applications import vgg16
import os
import numpy as np
from natsort import natsorted # Import for sorting of images
import cv2
import pickle
# The forams images should be in the CWD
data_dir = './NCSU-CUB Foram Images 01/'
img_shape = (224, 224) # 

# build the pretrained models
vgg16_model = vgg16.VGG16(include_top=False, pooling='avg')
resnet50_model = resnet50.ResNet50(include_top=False, pooling='avg')
print('Pre-trained Model loaded.')

forams_features = []
forams_labels = []
label2class = {}
class_count = {}
# The above initializes the variables for the features, labels, class_count, and the label2class mapping
class_list = natsorted([os.path.join(data_dir, folder) for folder in \
                            os.listdir(data_dir) if not folder.endswith('.txt')])
# The above gets the list of class folders sorted in natural order excluding any .txt folders
for class_id, class_folder in enumerate(class_list): # Loop through each class folder assigning an ID to each one
    sample_list = natsorted([os.path.join(class_folder, folder) \
                                    for folder in os.listdir(class_folder)])
    # Get a sorted listed of sample folders in current class folder
    class_count[class_id] = len(sample_list) / 1000 # Store the number of samples in the current class folder
    for sample_folder in sample_list: # Loop through each sample folder in the current class folder
        img_filenames = natsorted([os.path.join(sample_folder, file) for file in \
                            os.listdir(sample_folder) if file.endswith('.png')])
        # The above gets the list of each sample folder in every class folder in natural order
        group_images = np.zeros(img_shape + (len(img_filenames),))
        # The above creates a numpy array to store the current image data
        for i, img_file in enumerate(img_filenames): 
            img = cv2.imread(img_file, 0) # Read current image and convert to grayscale
            img = cv2.resize(img, img_shape, interpolation=cv2.INTER_CUBIC) # Resize the current image shape to 224,224
            group_images[:, :, i] = img # Add the image data to the numpy array
        img90 = np.expand_dims(np.percentile(group_images, 90, axis=-1), axis=-1)
        img50 = np.expand_dims(np.percentile(group_images, 50, axis=-1), axis=-1)
        img10 = np.expand_dims(np.percentile(group_images, 10, axis=-1), axis=-1)
        # The above finds the 10, 50, and 90th percentile of images across all images
        img = np.concatenate((img10, img50, img90), axis=-1) # Concatenate all of the percentiles above 
        img = np.expand_dims(img, axis=0) # Add new axis/ dimension for the batch dim

        fea_vgg16 = vgg16_model.predict_on_batch(vgg16.preprocess_input(img.copy())) 
        # The above preprocesses the image and extracts the features for vgg16
        fea_resnet50 = resnet50_model.predict_on_batch(resnet50.preprocess_input(img.copy()))
        # The above preprocesses the image and extracts the features for resnet50
        fea = np.concatenate((fea_vgg16, fea_resnet50), axis=1) # Concatenate the features from vgg16 and resnet50
        forams_features.append(fea) # Add the concatenated features to the list of features
        forams_labels.append(class_id) # Add current class ID to the list of labels
        label2class[class_id] = class_folder.split('/')[-1] # Store the mapping between class IDs and class folder names

forams_features = np.array(forams_features)
forams_labels = np.array(forams_labels)
# The above converts the features and labels to numpy arrays
print(forams_features.shape)
print(forams_labels.shape)

with open('./forams_features.p', 'wb') as f:
    pickle.dump({'features':forams_features, 'labels':forams_labels, \
                    'label2class':label2class, 'class_count':class_count}, f)
# The above saves the numpy arrays of the features and labels, and label-class mapping/ class_count to a pickle file