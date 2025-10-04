import streamlit as st
import base64
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image

# Load model and labels
model = load_model("citrus_model.keras")
with open("class_labels.txt") as f:
    labels = [line.strip() for line in f]

# Function to set background
def get_base64(bin_file):
    with open(bin_file, "rb") as f:
        return base64.b64encode(f.read()).decode()

def set_background(jpg_file):
    bin_str = get_base64(jpg_file)
    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/jpg;base64,{bin_str}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* Sidebar background */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #001a00, #003300);
        padding: 20px;
    }}

    /* Sidebar Title */
    [data-testid="stSidebar"] h2 {{
        color: #ff4dd2;
        font-size: 24px !important;
        text-shadow: 0px 0px 10px #ff66ff, 0px 0px 20px #ff33cc;
    }}

    /* Sidebar radio labels */
    [data-testid="stSidebar"] label {{
        color: #ffff66 !important;   
        font-size: 18px !important;  
        font-weight: bold !important;
        text-shadow: 0px 0px 5px #00ff99;
    }}

    /* Hover effect on radio buttons */
    [data-testid="stSidebar"] label:hover {{
        color: #39ff14 !important;  
        text-shadow: 0px 0px 10px #39ff14, 0px 0px 20px yellow;
        transform: scale(1.05);
    }}

    /* Upload file label */
    .uploadedFileLabel, .css-1djdyxw {{
        font-size: 22px !important;
        color: #ffcc00 !important;
        font-weight: bold !important;
        text-shadow: 0px 0px 10px #39ff14;
    }}

    /* Prediction result */
    .result-box {{
        font-size: 22px;
        font-weight: bold;
        color: #00ffcc;
        text-shadow: 0px 0px 8px #ff33cc;
        padding: 15px;
        border-radius: 12px;
        background: rgba(0, 0, 0, 0.6);
        text-align: center;
        margin-top: 15px;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Set background
set_background("bg.jpg")

# App title
st.markdown(
    "<h1 style='text-align: center; color: #ccff00; text-shadow: 0px 0px 10px #39ff14, 0px 0px 20px yellow;'>🌿 Citrus Leaf Disease Detector 🌿</h1>",
    unsafe_allow_html=True
)

# Sidebar Disease Info
st.sidebar.markdown("## 📌 Disease Information")
disease = st.sidebar.radio("Select a disease", labels)

# Show example image
if disease.lower() == "black spot":
    st.sidebar.image("black_spot.jpg", caption="Black spot Example")
    st.sidebar.markdown("### 🌱 About:\nBlack spot causes dark circular lesions on leaves and fruits.")
    st.sidebar.markdown("### 💡 Solution:\nSpray copper-based fungicides and remove infected leaves.")

elif disease.lower() == "canker":
    st.sidebar.image("canker.jpg", caption="Canker Example")
    st.sidebar.markdown("### 🌱 About:\nCanker produces raised corky lesions on leaves, stems, and fruits.")
    st.sidebar.markdown("### 💡 Solution:\nUse resistant varieties and apply bactericides.")

elif disease.lower() == "melanose":
    st.sidebar.image("melanose.jpg", caption="Melanose Example")
    st.sidebar.markdown("### 🌱 About:\nMelanose causes small dark brown lesions on leaves and fruits.")
    st.sidebar.markdown("### 💡 Solution:\nRemove old twigs and apply fungicides.")

elif disease.lower() == "greening":
    st.sidebar.image("greening.jpg", caption="Greening Example")
    st.sidebar.markdown("### 🌱 About:\nGreening causes yellow shoots and misshapen fruits.")
    st.sidebar.markdown("### 💡 Solution:\nControl psyllid insects and remove infected plants.")

elif disease.lower() == "healthy":
    st.sidebar.image("healthy.jpg", caption="Healthy Leaf")
    st.sidebar.markdown("### 🌱 About:\nThis leaf is healthy and shows no signs of disease.")
    st.sidebar.markdown("### 💡 Solution:\nMaintain proper care for citrus plants.")

# Upload Section
uploaded_file = st.file_uploader("📤 Upload a Citrus Leaf Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    img = Image.open(uploaded_file).convert("RGB")
    st.image(img, caption="Uploaded Image", use_container_width=True)

    # Preprocess
    img_resized = img.resize((128, 128))
    img_array = image.img_to_array(img_resized) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Prediction
    prediction = model.predict(img_array)
    pred_class = labels[np.argmax(prediction)]
    confidence = np.max(prediction) * 100

    st.markdown(
        f"<div class='result-box'>Prediction: {pred_class} <br> Confidence: {confidence:.2f}%</div>",
        unsafe_allow_html=True
    )
