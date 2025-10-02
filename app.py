import streamlit as st
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image

# ================== PAGE CONFIG ==================
st.set_page_config(page_title="Citrus Leaf Disease Detector", layout="wide")

# ================== BACKGROUND ==================
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://raw.githubusercontent.com/Techno-Shivani/citrus-leaf-disease-detector/main/bg.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    .title {
        font-size: 42px;
        font-weight: bold;
        color: #006400;
        text-align: center;
        text-shadow: 2px 2px 6px #99ff99;
    }
    .subtitle {
        font-size: 24px;
        font-weight: bold;
        color: #2E8B57;
    }
    .solution {
        font-size: 22px;
        font-weight: bold;
        color: #FF8C00;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ================== TITLE ==================
st.markdown("<h1 class='title'>🍃 Citrus Leaf Disease Detector 🍃</h1>", unsafe_allow_html=True)

# ================== LOAD MODEL ==================
@st.cache_resource
def load_my_model():
    return load_model("citrus_model.keras")

model = load_my_model()

# Labels
labels = ["Black spot", "Melanose", "Canker", "Greening", "Healthy"]

# ================== SIDEBAR MENU ==================
st.sidebar.header("📌 Disease Information")
menu = ["Black spot", "Canker", "Melanose", "Greening", "Healthy"]
choice = st.sidebar.radio("Select a disease", menu)

# Disease Info
disease_data = {
    "Black spot": {
        "image": "black_spot.jpg",
        "about": "Black spot causes dark circular lesions on citrus leaves and fruits.",
        "solution": "Spray copper-based fungicides and remove infected leaves immediately."
    },
    "Canker": {
        "image": "canker.jpg",
        "about": "Canker disease produces raised, corky lesions on leaves, stems, and fruits.",
        "solution": "Apply copper sprays, prune infected twigs, and use resistant rootstocks."
    },
    "Melanose": {
        "image": "melanose.jpg",
        "about": "Melanose is a fungal disease that creates small, dark, raised spots on leaves and fruits.",
        "solution": "Remove old twigs, improve air circulation, and apply fungicides."
    },
    "Greening": {
        "image": "greening.jpg",
        "about": "Greening (HLB) is a bacterial disease spread by psyllid insects, causing yellow shoots and misshaped fruits.",
        "solution": "Remove infected plants, control psyllid insects, and use resistant varieties."
    },
    "Healthy": {
        "image": "healthy.jpg",
        "about": "Healthy citrus leaves are shiny, green, and free from disease symptoms.",
        "solution": "Maintain proper irrigation, balanced fertilization, and regular monitoring."
    }
}

# Show sidebar disease info
st.sidebar.image(disease_data[choice]["image"], caption=f"{choice} Example", use_column_width=True)
st.sidebar.markdown(f"<p class='subtitle'>🌿 About:</p>", unsafe_allow_html=True)
st.sidebar.write(disease_data[choice]["about"])
st.sidebar.markdown(f"<p class='solution'>💡 Solution:</p>", unsafe_allow_html=True)
st.sidebar.write(disease_data[choice]["solution"])

# ================== MAIN APP - UPLOAD + PREDICTION ==================
st.markdown("### 📤 Upload a Citrus Leaf Image for Prediction")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    img = Image.open(uploaded_file).convert("RGB")
    st.image(img, caption="Uploaded Image", use_column_width=True)

    # Preprocess
    img_resized = img.resize((224, 224))  # same size as model training
    img_array = image.img_to_array(img_resized) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Predict
    preds = model.predict(img_array)[0]
    pred_class = labels[np.argmax(preds)]
    confidence = np.max(preds) * 100

    st.success(f"✅ Prediction: **{pred_class}** ({confidence:.2f}%)")

    # Show bar chart of all probabilities
    st.markdown("### 📊 Prediction Confidence")
    st.bar_chart(dict(zip(labels, preds)))
