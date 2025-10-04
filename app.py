import streamlit as st
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import base64

# ---------------- BACKGROUND IMAGE ----------------
def get_base64(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

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
        background: linear-gradient(180deg, #003300, #004d00);
        color: #ffffff;
    }}
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] span {{
        color: #00ff99 !important;
        font-weight: 600;
        font-size: 16px;
    }}
    .disease-text {{
        color: #ffcc00;
        font-size: 14px;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_background("bg.jpg")

# ---------------- LOAD MODEL ----------------
model = load_model("citrus_model.keras")

with open("class_labels.txt") as f:
    labels = [line.strip() for line in f]

# ---------------- TITLE ----------------
st.markdown(
    """
    <h1 style='text-align: center; color: #eaff00;
    text-shadow: 0 0 15px #39ff14, 0 0 25px #39ff14, 0 0 45px yellow;'>
    🍃 Citrus Leaf Disease Detector 🍃
    </h1>
    """,
    unsafe_allow_html=True,
)

# ---------------- SIDEBAR ----------------
st.sidebar.markdown(
    "<h2 style='color:#39ff14;text-shadow:0 0 10px yellow;'>📌 Disease Information</h2>",
    unsafe_allow_html=True,
)

disease = st.sidebar.radio("Select a disease", labels)

disease_info = {
    "Black spot": {
        "image": "black_spot.jpg",
        "about": "Black spot causes dark circular lesions on leaves and fruits.",
        "solution": "Spray copper-based fungicides and remove infected leaves."
    },
    "Canker": {
        "image": "canker.jpg",
        "about": "Citrus canker creates raised corky lesions with yellow halos.",
        "solution": "Use copper sprays and remove infected plant parts."
    },
    "Melanose": {
        "image": "melanose.jpg",
        "about": "Melanose causes small dark spots, mostly on old leaves.",
        "solution": "Remove dead branches and apply fungicide if needed."
    },
    "Greening": {
        "image": "greening.jpg",
        "about": "Greening leads to mottled leaves, bitter fruit, and decline.",
        "solution": "Remove infected trees and control psyllid vectors."
    },
    "Healthy": {
        "image": "healthy.jpg",
        "about": "Leaf is disease-free with optimal growth.",
        "solution": "Maintain hygiene and proper fertilization."
    }
}

if disease in disease_info:
    st.sidebar.image(disease_info[disease]["image"], caption=f"{disease} Example", use_container_width=True)
    st.sidebar.markdown(f"<p class='disease-text'><b>🌱 About:</b> {disease_info[disease]['about']}</p>", unsafe_allow_html=True)
    st.sidebar.markdown(f"<p class='disease-text'><b>💡 Solution:</b> {disease_info[disease]['solution']}</p>", unsafe_allow_html=True)

# ---------------- UPLOAD + PREDICT ----------------
uploaded_file = st.file_uploader("📤 Upload a Citrus Leaf Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    img = image.load_img(uploaded_file, target_size=(224, 224))
    st.image(uploaded_file, caption="Uploaded Image", width=300)   # FIXED: use_container_width removed

    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = x / 255.0

    prediction = model.predict(x)
    class_index = np.argmax(prediction)
    confidence = round(np.max(prediction) * 100, 2)

    st.markdown(
        f"""
        <div style="background:rgba(0,0,0,0.6); padding:15px; border-radius:10px; 
        text-align:center; color:#00ffcc; font-size:20px; font-weight:bold;
        text-shadow: 0 0 10px #39ff14;">
        ✅ Prediction: {labels[class_index]} <br>
        🔥 Confidence: {confidence}%
        </div>
        """,
        unsafe_allow_html=True,
    )
