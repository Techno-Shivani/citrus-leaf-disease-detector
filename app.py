import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

# Load Model
model = tf.keras.models.load_model("citrus_model.keras")

# Load class labels
with open("class_labels.txt") as f:
    class_names = [line.strip() for line in f.readlines()]

# Disease Info
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

h1 {{
    font-family: 'Poppins', sans-serif;
    font-size: 50px;
    text-align: center;
    color: #ccff00;
    text-shadow: 0 0 20px #00ff55, 0 0 40px #00ff55;
}}
.card {{
    background: rgba(0,0,0,0.6);
    padding: 20px;
    border-radius: 20px;
    box-shadow: 0px 0px 20px #00ff55;
    margin: 10px;
}}
img {{
    border-radius: 15px;
    max-height: 250px;
    object-fit: contain;
}}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# --- Heading ---
st.markdown("<h1>🍃 Citrus Leaf Disease Detector 🍃</h1>", unsafe_allow_html=True)

# --- Layout ---
col1, col2 = st.columns([1, 2])

# Left Column (Disease Info)
with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📌 Disease Information")
    selected = st.radio("Select a disease", list(disease_info.keys()))
    st.image(disease_info[selected]["image"], caption=f"{selected} Example", use_container_width=True)

    st.markdown(f"### 🌿 About:\n{disease_info[selected]['about']}")
    st.markdown(f"### 💡 Solution:\n{disease_info[selected]['solution']}")
    st.markdown("</div>", unsafe_allow_html=True)

# Right Column (Prediction)
with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
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
            <div style='padding:15px; border-radius:12px; background:rgba(0,0,0,0.7);
            text-align:center; font-size:22px; font-weight:bold; color:#ccff00;'>
            ✅ Prediction: {predicted_class}<br>
            📊 Confidence: {confidence:.2f}%
            </div>
            """,
            unsafe_allow_html=True
        )
    st.markdown("</div>", unsafe_allow_html=True)
