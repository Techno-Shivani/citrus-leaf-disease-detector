import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import zipfile
import os

# --------------------------
# 🌿 PAGE CONFIGURATION
# --------------------------
st.set_page_config(
    page_title="Citrus Leaf Disease Detection",
    page_icon="🍋",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# --------------------------
# 🌈 CUSTOM DARK + NEON STYLE
# --------------------------
st.markdown(
    """
    <style>
        body {
            background-color: #0B132B;
            color: #F0F0F0;
        }
        [data-testid="stAppViewContainer"] {
            background: radial-gradient(circle at top left, #0B132B, #1C2541);
        }
        [data-testid="stHeader"] {background: rgba(0,0,0,0);}
        h1 {
            text-align: center;
            color: #00FFFF;
            text-shadow: 0px 0px 10px #00FFFF;
            font-family: 'Trebuchet MS', sans-serif;
        }
        .result-card {
            background: linear-gradient(145deg, #16213E, #0F3460);
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            color: white;
            font-size: 1.3rem;
            box-shadow: 0 0 15px #00FFFF;
            margin-top: 20px;
        }
        .healthy {color: #4EEC8E; text-shadow: 0px 0px 10px #4EEC8E;}
        .diseased {color: #FF4B5C; text-shadow: 0px 0px 10px #FF4B5C;}
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------
# 🍋 TITLE
# --------------------------
st.markdown("<h1>🍋 Citrus Leaf Disease Detection</h1>", unsafe_allow_html=True)
st.write("Upload a citrus leaf image to detect if it’s **Healthy** or **Diseased**.")

# --------------------------
# 🧠 LOAD MODEL FUNCTION
# --------------------------
@st.cache_resource
def load_model_and_labels():
    zip_path = "citrus_model_retrained.zip"
    extract_path = "model_folder"

    # ✅ Extract model if not already extracted
    if not os.path.exists(extract_path):
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)

    model_path = os.path.join(extract_path, "citrus_model_retrained.keras")
    model = tf.keras.models.load_model(model_path, compile=False)

    with open("class_labels.txt", "r") as f:
        labels = [line.strip() for line in f.readlines()]

    return model, labels


# --------------------------
# 🔍 PREDICTION FUNCTION
# --------------------------
def predict_disease(image, model, labels):
    img = image.resize((224, 224))
    img_array = tf.keras.preprocessing.image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    preds = model.predict(img_array)
    pred_idx = np.argmax(preds)
    confidence = np.max(preds) * 100
    return labels[pred_idx], confidence


# --------------------------
# 🚀 MAIN APP
# --------------------------
uploaded_file = st.file_uploader("Upload Citrus Leaf Image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    st.write("🧠 Analyzing image, please wait...")
    model, labels = load_model_and_labels()
    label, confidence = predict_disease(image, model, labels)

    # 🌿 Show Result
    if label.lower() == "healthy":
        st.markdown(
            f"<div class='result-card healthy'>✅ Prediction: <b>{label}</b><br>Confidence: {confidence:.2f}%</div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"<div class='result-card diseased'>⚠️ Prediction: <b>{label}</b><br>Confidence: {confidence:.2f}%</div>",
            unsafe_allow_html=True,
        )

else:
    st.info("Please upload a leaf image to start detection 🌱")
