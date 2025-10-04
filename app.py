import streamlit as st
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image

# Load trained model
model = load_model("citrus_model.keras")

# Class labels
with open("class_labels.txt", "r") as f:
    labels = [line.strip() for line in f.readlines()]

# Custom CSS for styling
st.markdown("""
    <style>
    body {
        background: url('bg.jpg') no-repeat center center fixed;
        background-size: cover;
        font-family: 'Poppins', sans-serif;
    }
    h1 {
        font-size: 40px !important;
        text-align: center;
        color: #28a745;
        text-shadow: 0px 0px 10px #00ff88, 0px 0px 20px #00ff88;
        font-weight: bold;
    }
    .about-text {
        font-size: 20px;
        color: #222;
        padding: 10px;
        border-left: 5px solid #28a745;
        background: rgba(255,255,255,0.7);
        border-radius: 10px;
        margin-top: 15px;
    }
    .neon-button {
        display: inline-block;
        padding: 15px 30px;
        font-size: 22px;
        font-weight: bold;
        color: #fff;
        background: #00ff88;
        border: none;
        border-radius: 15px;
        text-shadow: 0 0 5px #00ff88, 0 0 15px #00ff88, 0 0 30px #00ff88;
        box-shadow: 0 0 10px #00ff88, 0 0 20px #00ff88, 0 0 40px #00ff88;
        transition: 0.3s;
    }
    .neon-button:hover {
        background: #ffcc00;
        color: black;
        text-shadow: 0 0 5px #ffcc00, 0 0 15px #ffcc00, 0 0 30px #ffcc00;
        box-shadow: 0 0 20px #ffcc00, 0 0 40px #ffcc00, 0 0 60px #ffcc00;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1>🌿 Citrus Leaf Disease Detector 🌿</h1>", unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader("Upload a Citrus Leaf Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    img = Image.open(uploaded_file).convert("RGB")
    st.image(img, caption="Uploaded Leaf", use_column_width=True)  # Image auto-resize

    # Preprocess image
    img_resized = img.resize((128, 128))
    img_array = image.img_to_array(img_resized) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Prediction
    predictions = model.predict(img_array)
    predicted_class = labels[np.argmax(predictions)]
    confidence = float(np.max(predictions) * 100)

    # Show result as Neon Button
    st.markdown(
        f'<button class="neon-button">Prediction: {predicted_class} ({confidence:.2f}%)</button>',
        unsafe_allow_html=True
    )

    # Disease Info
    if predicted_class == "Black spot":
        st.markdown(
            "<div class='about-text'><b>🍂 About:</b> Black spot causes dark circular lesions on leaves and fruits.</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<div class='about-text'><b>💡 Solution:</b> Spray copper-based fungicides and remove infected leaves.</div>",
            unsafe_allow_html=True,
        )
    elif predicted_class == "Canker":
        st.markdown(
            "<div class='about-text'><b>🍂 About:</b> Canker leads to raised lesions on leaves, stems, and fruits.</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<div class='about-text'><b>💡 Solution:</b> Remove infected plants and use antibiotics or copper sprays.</div>",
            unsafe_allow_html=True,
        )
    elif predicted_class == "Melanose":
        st.markdown(
            "<div class='about-text'><b>🍂 About:</b> Melanose causes small brown spots on older leaves.</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<div class='about-text'><b>💡 Solution:</b> Prune old twigs and apply fungicide sprays.</div>",
            unsafe_allow_html=True,
        )
    elif predicted_class == "Greening":
        st.markdown(
            "<div class='about-text'><b>🍂 About:</b> Greening results in yellow shoots and bitter fruits.</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<div class='about-text'><b>💡 Solution:</b> Remove infected trees and control psyllid insect carriers.</div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            "<div class='about-text'><b>🍂 About:</b> This leaf looks healthy and free from diseases.</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<div class='about-text'><b>💡 Tip:</b> Maintain proper watering and use organic fertilizers.</div>",
            unsafe_allow_html=True,
        )
