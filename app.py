import streamlit as st
import base64
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image

# ------------------ LOAD MODEL AND LABELS ------------------
model = load_model("citrus_model.keras")
with open("class_labels.txt") as f:
    labels = [line.strip() for line in f]

# ------------------ BACKGROUND IMAGE ------------------
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

    /* Sidebar Heading */
    [data-testid="stSidebar"] h2 {{
        color: #ffff33; 
        font-size: 24px !important;
        text-shadow: 0px 0px 15px #ffff66;
        font-weight: bold;
    }}

    /* Sidebar Radio Buttons */
    [data-testid="stSidebar"] label {{
        color: white !important;
        font-size: 18px !important;
        font-weight: bold !important;
        text-shadow: 0px 0px 6px #39ff14;
    }}

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

    /* Title */
    .title {{
        font-size: 40px;
        font-weight: bold;
        color: #ccff33;
        text-align: center;
        text-shadow: 0px 0px 20px #00ff00, 0px 0px 40px yellow;
        margin-bottom: 20px;
    }}

    /* Upload text bigger */
    .upload-label {{
        font-size: 20px;
        color: #39ff14;
        font-weight: bold;
        text-shadow: 0px 0px 8px black;
    }}

    /* Predict Button */
    .stButton>button {{
        background: linear-gradient(90deg, #39ff14, #ccff33);
        color: black;
        font-size: 18px;
        font-weight: bold;
        border-radius: 12px;
        padding: 12px 25px;
        box-shadow: 0px 0px 20px #39ff14, 0px 0px 40px #ccff33;
        transition: 0.3s;
    }}

    .stButton>button:hover {{
        background: linear-gradient(90deg, yellow, #39ff14);
        transform: scale(1.08);
        box-shadow: 0px 0px 30px yellow, 0px 0px 60px #39ff14;
    }}

    /* Info Cards */
    .card {{
        background: rgba(0, 20, 0, 0.8);
        border-radius: 12px;
        padding: 20px;
        margin-top: 20px;
        box-shadow: 0px 0px 15px #39ff14;
    }}
    .card h3 {{
        color: #ffff33;
        text-shadow: 0px 0px 12px #39ff14;
    }}
    .card p {{
        color: white;
        font-size: 16px;
        line-height: 1.5;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Set background
set_background("bg.jpg")

# ------------------ APP TITLE ------------------
st.markdown("<h1 class='title'>🌿 Citrus Leaf Disease Detector 🌿</h1>", unsafe_allow_html=True)

# ------------------ SIDEBAR MENU ------------------
st.sidebar.markdown("<h2>📌 Disease Information</h2>", unsafe_allow_html=True)

disease = st.sidebar.radio("Select a disease", ["Black spot", "Melanose", "Canker", "Greening", "Healthy"])

disease_images = {
    "Black spot": "black_spot.jpg",
    "Melanose": "melanose.jpg",
    "Canker": "canker.jpg",
    "Greening": "greening.jpg",
    "Healthy": "healthy.jpg"
}

st.sidebar.image(disease_images[disease], use_container_width=True)
st.sidebar.markdown(f"<p class='caption'>{disease} Example</p>", unsafe_allow_html=True)

# ------------------ ABOUT + SOLUTIONS ------------------
disease_info = {
    "Black spot": {
        "about": "Black spot causes dark circular lesions on leaves and fruits, reducing plant health.",
        "solution": "Spray copper-based fungicides and remove infected leaves."
    },
    "Melanose": {
        "about": "Melanose leads to brown raised spots and roughened leaf surface, common in humid climates.",
        "solution": "Apply fungicide sprays and ensure good air circulation in orchards."
    },
    "Canker": {
        "about": "Canker is a bacterial disease that produces raised brown lesions with yellow halos.",
        "solution": "Use resistant varieties and apply copper sprays regularly."
    },
    "Greening": {
        "about": "Greening (HLB) is a deadly bacterial disease spread by psyllids, leading to yellow shoots and misshapen fruits.",
        "solution": "Remove infected plants and control psyllid population with insecticides."
    },
    "Healthy": {
        "about": "This leaf is healthy with no signs of infection.",
        "solution": "Maintain proper nutrition and irrigation for continued health."
    }
}

# ------------------ FILE UPLOAD ------------------
st.markdown("<p class='upload-label'>📤 Upload a Citrus Leaf Image</p>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"])

# ------------------ PREDICTION ------------------
if uploaded_file is not None:
    img = Image.open(uploaded_file).convert("RGB")
    st.image(img, caption="Uploaded Image", use_container_width=True)

    if st.button("🔍 Predict"):
        img_resized = img.resize((224, 224))
        img_array = image.img_to_array(img_resized) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        prediction = model.predict(img_array)
        predicted_class = labels[np.argmax(prediction)]
        confidence = np.max(prediction) * 100

        st.success(f"✅ Prediction: {predicted_class}")
        st.info(f"📊 Confidence: {confidence:.2f}%")

        # Show About + Solution Card
        info = disease_info.get(predicted_class, {})
        if info:
            st.markdown(f"""
            <div class='card'>
                <h3>📖 About</h3>
                <p>{info['about']}</p>
                <h3>💡 Solution</h3>
                <p>{info['solution']}</p>
            </div>
            """, unsafe_allow_html=True)
