import streamlit as st
import base64
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image

# ------------------ LOAD MODEL ------------------
@st.cache_resource
def load_citrus_model():
    model = load_model("citrus_model.keras")
    labels = ["Black spot", "Melanose", "Canker", "Greening", "Healthy"]
    return model, labels

model, class_labels = load_citrus_model()

# ------------------ BACKGROUND IMAGE ------------------
def add_bg_from_local(bg_file):
    with open(bg_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_from_local("bg.jpg")

# ------------------ CSS ------------------
st.markdown("""
    <style>
    h1 {
        font-size: 48px !important;
        text-align: center;
        color: #fff200;
        text-shadow: 2px 2px 8px #00ff00;
    }
    h2 {
        color: white;
    }
    .upload-text {
        font-size: 22px;
        font-weight: bold;
        color: white;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------ TITLE ------------------
st.markdown("<h1>🌿 Citrus Leaf Disease Detector 🌿</h1>", unsafe_allow_html=True)

# ------------------ SIDEBAR MENU ------------------
menu = st.sidebar.selectbox(
    "📘 Disease Information",
    ["Black spot", "Melanose", "Canker", "Greening", "Healthy Leaf"]
)

disease_info = {
    "Black spot": {
        "img": "black_spot.jpg",
        "about": "Black spot is a fungal disease causing dark lesions on leaves and fruits.",
        "solution": "Use copper-based fungicides and ensure proper sanitation in orchards."
    },
    "Melanose": {
        "img": "melanose.jpg",
        "about": "Melanose is caused by Diaporthe citri fungus, producing brown spots on young leaves.",
        "solution": "Apply fungicide sprays and remove infected twigs."
    },
    "Canker": {
        "img": "canker.jpg",
        "about": "Canker causes raised brown lesions with yellow halos on citrus leaves and fruits.",
        "solution": "Remove infected trees, use windbreaks, and copper sprays."
    },
    "Greening": {
        "img": "greening.jpg",
        "about": "Citrus greening is a bacterial disease spread by psyllids, causing yellow shoots and misshapen fruits.",
        "solution": "Control psyllid vectors, remove diseased trees, and use resistant rootstocks."
    },
    "Healthy Leaf": {
        "img": "healthy.jpg",
        "about": "Healthy citrus leaves are green, smooth, and free from lesions or spots.",
        "solution": "Maintain good soil health, regular irrigation, and balanced nutrients."
    }
}

# Sidebar display
info = disease_info[menu]
st.sidebar.image(info["img"], caption=menu, use_container_width=True)
st.sidebar.markdown(f"### 📝 About\n{info['about']}")
st.sidebar.markdown(f"### 💡 Solution\n{info['solution']}")

# ------------------ IMAGE UPLOAD ------------------
st.markdown("<p class='upload-text'>📤 Upload a Citrus Leaf Image</p>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"])

def predict_leaf(img):
    img = img.convert("RGB").resize((224,224))
    arr = image.img_to_array(img) / 255.0
    arr = np.expand_dims(arr, axis=0)
    preds = model.predict(arr)[0]
    return preds

# ------------------ PREDICTION ------------------
if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Leaf", width=300)

    preds = predict_leaf(img)
    pred_idx = np.argmax(preds)
    pred_label = class_labels[pred_idx]
    confidence = preds[pred_idx] * 100

    st.success(f"✅ Prediction: **{pred_label}** ({confidence:.2f}%)")

    # Bar graph
    fig, ax = plt.subplots()
    ax.bar(class_labels, preds*100, color="limegreen")
    ax.set_ylabel("Confidence (%)")
    ax.set_title("Prediction Probabilities")
    st.pyplot(fig)
