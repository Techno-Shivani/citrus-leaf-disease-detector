import streamlit as st
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image

# Load model
model = load_model("citrus_model.keras")

# Labels
labels = ["Black spot", "Melanose", "Canker", "Greening", "Healthy"]

# UI Title
st.markdown("<h1 style='text-align: center; color: green;'>🍃 Citrus Leaf Disease Detector 🍃</h1>", unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader("Upload a Citrus Leaf Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    img = Image.open(uploaded_file).convert("RGB")
    st.image(img, caption="Uploaded Leaf", use_column_width=True)

    img = img.resize((224,224))
    x = np.array(img)/255.0
    x = np.expand_dims(x, axis=0)

    prediction = model.predict(x)[0]
    result = labels[np.argmax(prediction)]
    confidence = np.max(prediction)*100

    st.success(f"Prediction: **{result}** ({confidence:.2f}%)")
