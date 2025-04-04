import os
import json
from PIL import Image

import numpy as np
import tensorflow as tf
import streamlit as st


working_dir=os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(working_dir, "plant_disease_prediction_model.h5")

##load pretrained model
model=tf.keras.models.load_model(model_path)

##loading classes names 
class_indices=json.load(open(f"{working_dir}/class_indices.json"))


##function to load and preprocess image using pillow
def load_and_preprocess_image(image_path,target_size=(224,224)):
    ##load image
    img=Image.open(image_path)
    ##resize image
    img=img.resize(target_size)
    ##convert image to a numpy array
    img_array=np.array(img)
    ##add batch dimension
    img_array=np.expand_dims(img_array,axis=0)
    ###scale image values to[0,1]
    
    img_array=img_array.astype('float32')/255
    return img_array 



# Function to Predict the Class of an Image
def predict_image_class(model, image, class_indices):
    preprocessed_img = load_and_preprocess_image(image)
    predictions = model.predict(preprocessed_img)
    predicted_class_index = np.argmax(predictions, axis=1)[0]
    predicted_class_name = class_indices[str(predicted_class_index)]
    return predicted_class_name



# Streamlit App
st.title('Plant Disease Classifier')

uploaded_image = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    image = Image.open(uploaded_image)
    col1, col2 = st.columns(2)

    with col1:
        resized_img = image.resize((150, 150))
        st.image(resized_img, caption="Uploaded Image",use_column_width=True)

    with col2:
        if st.button('Classify'):
            # Preprocess the uploaded image and predict the class
            with st.spinner("Classifying..."):
                prediction = predict_image_class(model, image, class_indices)
                st.success(f'Prediction: {prediction}')
           