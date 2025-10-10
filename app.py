import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import zipfile
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image

# -------------------------------------------------------------
# ✅ Step 1: Page setup
# -------------------------------------------------------------
st.set_page_config(page_title="🍃 Citrus Leaf Disease Detector", layout="wide")
st.title("🍃 Citrus Leaf Disease Detection using Deep Learning")
st.markdown("Upload a citrus leaf image to detect disease and view analysis results.")

# -------------------------------------------------------------
# ✅ Step 2: Load model (from ZIP if needed)
# -------------------------------------------------------------
MODEL_FILE = "citrus_model_retrained.keras"
ZIP_FILE = "citrus_model_retrained.zip"

if not os.path.exists(MODEL_FILE):
    with zipfile.ZipFile(ZIP_FILE, "r") as zip_ref:
        zip_ref.extractall(".")

model = load_model(MODEL_FILE)

# -------------------------------------------------------------
# ✅ Step 3: Load class labels
# -------------------------------------------------------------
with open("class_labels.txt", "r") as f:
    labels = [line.strip() for line in f.readlines()]

# -------------------------------------------------------------
# ✅ Step 4: UI layout (sidebar + upload)
# -------------------------------------------------------------
st.sidebar.image("bg.jpg", use_container_width=True)
st.sidebar.header("🌿 Disease Information")

uploaded_file = st.file_uploader("📤 Upload a Leaf Image", type=["jpg", "jpeg", "png"])

# -------------------------------------------------------------
# ✅ Step 5: Process and predict
# -------------------------------------------------------------
if uploaded_file is not None:
    # Show uploaded image
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Leaf", use_container_width=True)

    # Preprocess image
    img = img.convert("RGB")
    img = img.resize((224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = x / 255.0

    # Predict
    st.info("🔍 Analyzing image...")
    pred = model.predict(x)
    predicted_class = labels[np.argmax(pred)]
    confidence = round(np.max(pred) * 100, 2)

    # ---------------------------------------------------------
    # ✅ Step 6: Show prediction results
    # ---------------------------------------------------------
    st.success(f"✅ Prediction: **{predicted_class}** ({confidence}%)")

    # Show probability chart
    st.subheader("📊 Prediction Probabilities")
    fig, ax = plt.subplots()
    ax.bar(labels, pred[0] * 100)
    ax.set_ylabel("Confidence (%)")
    ax.set_xlabel("Classes")
    ax.set_title("Prediction Probabilities")
    st.pyplot(fig)

    # ---------------------------------------------------------
    # ✅ Step 7: Sidebar information (disease info + solutions)
    # ---------------------------------------------------------
    disease_info = {
        "Black spot": {
            "desc": "Fungal disease causing black lesions on leaves.",
            "solution": "Use copper-based fungicide and avoid overhead irrigation.",
            "img": "black_spot.jpg",
        },
        "Melanose": {
            "desc": "Fungal disease forming small dark brown spots.",
            "solution": "Prune dead wood and apply suitable fungicide.",
            "img": "melanose.jpg",
        },
        "canker": {
            "desc": "Bacterial infection causing raised corky lesions.",
            "solution": "Remove infected leaves and use copper spray.",
            "img": "canker.jpg",
        },
        "greening": {
            "desc": "Serious bacterial disease spread by psyllids.",
            "solution": "Remove infected trees and control insect vectors.",
            "img": "greening.jpg",
        },
        "healthy": {
            "desc": "Leaf appears free from visible infections.",
            "solution": "Maintain balanced nutrients and regular monitoring.",
            "img": "healthy.jpg",
        },
    }

    if predicted_class in disease_info:
        info = disease_info[predicted_class]
        st.sidebar.subheader(f"🌱 About {predicted_class}")
        st.sidebar.image(info["img"], use_container_width=True)
        st.sidebar.write(f"**Description:** {info['desc']}")
        st.sidebar.write(f"💡 **Solution:** {info['solution']}")
else:
    st.warning("👆 Upload an image to start the prediction process.")
