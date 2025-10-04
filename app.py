import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import os

# Load Model
model = tf.keras.models.load_model("citrus_model.keras")

# Load class labels
with open("class_labels.txt") as f:
    class_names = [line.strip() for line in f.readlines()]

# Disease info
disease_info = {
    "Black spot": {
        "image": "black_spot.jpg",
        "about": "Black spot causes dark circular lesions on leaves and fruits.",
        "solution": "Spray copper-based fungicides and remove infected leaves."
    },
    "Canker": {
        "image": "canker.jpg",
        "about": "Canker causes lesions with a water-soaked margin and yellow halo.",
        "solution": "Use copper sprays and resistant varieties."
    },
    "Melanose": {
        "image": "melanose.jpg",
        "about": "Melanose produces small dark brown spots on leaves and fruits.",
        "solution": "Prune dead branches and apply fungicide sprays."
    },
    "Greening": {
        "image": "greening.jpg",
        "about": "Greening makes leaves yellow with green veins.",
        "solution": "Remove infected plants and control psyllid insect."
    },
    "Healthy": {
        "image": "healthy.jpg",
        "about": "Healthy citrus leaf with no signs of disease.",
        "solution": "Maintain proper watering and nutrient management."
    }
}

# --- Page Config ---
st.set_page_config(page_title="Citrus Leaf Disease Detector", page_icon="🍋", layout="wide")

# --- Background Image ---
page_bg = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background: url("bg.jpg");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# --- Heading ---
st.markdown(
    """
    <h1 style='text-align: center; color: #ccff00; font-family: Poppins; 
    text-shadow: 0 0 20px #00ff55, 0 0 40px #00ff55;'>
    🍃 Citrus Leaf Disease Detector 🍃
    </h1>
    """,
    unsafe_allow_html=True
)

st.write("")

# --- Layout ---
col1, col2 = st.columns([1, 2])

# Disease Information Section
with col1:
    st.subheader("📌 Disease Information")
    selected = st.radio("Select a disease", list(disease_info.keys()))

    st.image(disease_info[selected]["image"], caption=f"{selected} Example", use_container_width=True)

    st.markdown(f"### 🌿 About:\n{disease_info[selected]['about']}")
    st.markdown(f"### 💡 Solution:\n{disease_info[selected]['solution']}")

# Prediction Section
with col2:
    st.subheader("🔍 Upload a Citrus Leaf Image")
    uploaded_file = st.file_uploader("Upload leaf image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        img = Image.open(uploaded_file).convert("RGB")
        st.image(img, caption="Uploaded Leaf", use_container_width=True)

        # Preprocess
        img_resized = img.resize((224, 224))
        img_array = np.array(img_resized) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # Predict
        predictions = model.predict(img_array)
        confidence = np.max(predictions) * 100
        predicted_class = class_names[np.argmax(predictions)]

        st.markdown(
            f"""
            <div style='text-align:center; padding:20px; 
            border-radius:15px; background:rgba(0,0,0,0.6); 
            color:#ccff00; font-size:22px; font-weight:bold;
            text-shadow: 0 0 10px #00ff55;'>
            ✅ Prediction: {predicted_class} <br>
            📊 Confidence: {confidence:.2f}%
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <style>
            div.stButton > button {
                background-color: #00cc44;
                color: white;
                font-size: 20px;
                border-radius: 10px;
                box-shadow: 0px 0px 15px #00ff55;
                transition: 0.3s;
            }
            div.stButton > button:hover {
                background-color: #00ff55;
                color: black;
                transform: scale(1.1);
                box-shadow: 0px 0px 30px #ccff00;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        st.button("🔮 Predict Again")

