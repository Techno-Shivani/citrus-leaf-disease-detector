import streamlit as st
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import matplotlib.pyplot as plt

# --------------------------
# Basic App Configuration
# --------------------------
st.set_page_config(
    page_title="Citrus Leaf Disease Detector 🌿",
    layout="wide",
    page_icon="🌱"
)

# --------------------------
# Custom CSS for Neon Theme
# --------------------------
st.markdown("""
    <style>
    body {
        background-color: #0b0c10;
        color: #66fcf1;
    }
    .stApp {
        background: linear-gradient(135deg, #0b0c10, #1f2833);
        color: #c5c6c7;
    }
    .title {
        font-size: 40px;
        color: #45A29E;
        text-align: center;
        font-weight: bold;
    }
    .prediction-box {
        border: 2px solid #66fcf1;
        border-radius: 15px;
        padding: 20px;
        background-color: rgba(31, 40, 51, 0.8);
        color: #c5c6c7;
    }
    .footer {
        text-align: center;
        color: #45A29E;
        font-size: 14px;
        margin-top: 50px;
    }
    </style>
""", unsafe_allow_html=True)

# --------------------------
# Model & Labels Load
# --------------------------
@st.cache_resource
def load_model_and_labels():
model = tf.keras.models.load_model("citrus_model_retrained.keras", compile=False)
    with open("class_labels.txt", "r") as f:
        labels = [line.strip() for line in f.readlines()]
    return model, labels

model, labels = load_model_and_labels()

# --------------------------
# Sidebar
# --------------------------
st.sidebar.image("bg.jpg", use_container_width=True)
st.sidebar.title("🍃 Disease Information")
st.sidebar.markdown("""
Upload a **Citrus Leaf Image** and let the model detect the disease using Deep Learning.
""")
st.sidebar.divider()
st.sidebar.write("Developed with ❤️ by Shivani using TensorFlow & Streamlit.")

# --------------------------
# Title
# --------------------------
st.markdown('<p class="title">🌿 Citrus Leaf Disease Detection (AI Model)</p>', unsafe_allow_html=True)

# --------------------------
# File Upload
# --------------------------
uploaded_file = st.file_uploader("📤 Upload a Citrus Leaf Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    img = image.load_img(uploaded_file, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = x / 255.0

    pred = model.predict(x)
    predicted_class = labels[np.argmax(pred)]
    confidence = round(np.max(pred) * 100, 2)

    # Display uploaded image
    col1, col2 = st.columns(2)
    with col1:
        st.image(uploaded_file, caption="Uploaded Leaf", use_container_width=True)
    with col2:
        st.markdown(f"<div class='prediction-box'><h3>Prediction: {predicted_class}</h3>", unsafe_allow_html=True)
        st.markdown(f"<h4>Confidence: {confidence}%</h4></div>", unsafe_allow_html=True)

    # Bar chart for probabilities
    fig, ax = plt.subplots()
    ax.bar(labels, pred[0] * 100, color="#66fcf1")
    ax.set_title("Prediction Probabilities", color="#66fcf1")
    ax.set_xlabel("Diseases", color="#c5c6c7")
    ax.set_ylabel("Confidence (%)", color="#c5c6c7")
    st.pyplot(fig)

# --------------------------
# Footer
# --------------------------
st.markdown('<p class="footer">© 2025 Shivani | Citrus Leaf Disease AI Model 🌱</p>', unsafe_allow_html=True)
