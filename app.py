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

    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #001a00, #002200);
        padding: 20px;
    }}

    [data-testid="stSidebar"] h2 {{
        color: #ff4dd2;
        font-size: 24px !important;
        text-shadow: 0px 0px 15px #ff33cc;
        font-weight: bold;
    }}

    /* Sidebar labels - white with glow */
    [data-testid="stSidebar"] label {{
        color: white !important;   
        font-size: 18px !important;  
        font-weight: bold !important;
        text-shadow: 0px 0px 6px #39ff14;
    }}

    /* Hover effect */
    [data-testid="stSidebar"] label:hover {{
        color: #ffff66 !important;  
        text-shadow: 0px 0px 10px yellow, 0px 0px 20px #39ff14;
        transform: scale(1.05);
    }}

    /* Caption under images */
    .caption {{
        color: white;
        font-weight: bold;
        font-size: 16px;
        text-align: center;
        text-shadow: 0px 0px 5px black;
    }}

    /* Upload section */
    .uploadedFileLabel, .css-1djdyxw {{
        font-size: 22px !important;
        color: #ffcc00 !important;
        font-weight: bold !important;
        text-shadow: 0px 0px 10px #39ff14;
    }}

    /* Title styling */
    .main-title {{
        text-align: center; 
        color: #ccff00; 
        font-size: 42px; 
        text-shadow: 2px 2px 4px black, 0px 0px 15px #39ff14, 0px 0px 30px yellow;
        font-weight: bold;
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

# App title with outline
st.markdown("<h1 class='main-title'>🌿 Citrus Leaf Disease Detector 🌿</h1>", unsafe_allow_html=True)

# Sidebar Disease Info
st.sidebar.markdown("## 📌 Disease Information")
disease = st.sidebar.radio("Select a disease", labels)

# Show example images + captions
if disease.lower() == "black spot":
    st.sidebar.image("black_spot.jpg")
    st.sidebar.markdown("<p class='caption'>Black spot Example</p>", unsafe_allow_html=True)
    st.sidebar.markdown("### 🌱 About:\nBlack spot causes dark circular lesions on leaves and fruits.")
    st.sidebar.markdown("### 💡 Solution:\nSpray copper-based fungicides and remove infected leaves.")

elif disease.lower() == "canker":
    st.sidebar.image("canker.jpg")
    st.sidebar.markdown("<p class='caption'>Canker Example</p>", unsafe_allow_html=True)
    st.sidebar.markdown("### 🌱 About:\nCanker produces raised corky lesions on leaves, stems, and fruits.")
    st.sidebar.markdown("### 💡 Solution:\nUse resistant varieties and apply bactericides.")

elif disease.lower() == "melanose":
    st.sidebar.image("melanose.jpg")
    st.sidebar.markdown("<p class='caption'>Melanose Example</p>", unsafe_allow_html=True)
    st.sidebar.markdown("### 🌱 About:\nMelanose causes small dark brown lesions on leaves and fruits.")
    st.sidebar.markdown("### 💡 Solution:\nRemove old twigs and apply fungicides.")

elif disease.lower() == "greening":
    st.sidebar.image("greening.jpg")
    st.sidebar.markdown("<p class='caption'>Greening Example</p>", unsafe_allow_html=True)
    st.sidebar.markdown("### 🌱 About:\nGreening causes yellow shoots and misshapen fruits.")
    st.sidebar.markdown("### 💡 Solution:\nControl psyllid insects and remove infected plants.")

elif disease.lower() == "healthy":
    st.sidebar.image("healthy.jpg")
    st.sidebar.markdown("<p class='caption'>Healthy Leaf</p>", unsafe_allow_html=True)
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
