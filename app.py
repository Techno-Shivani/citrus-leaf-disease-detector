import streamlit as st
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from PIL import Image
import matplotlib.pyplot as plt
import zipfile
import os

# ==============================
# 1️⃣ SETUP
# ==============================

st.set_page_config(page_title="Citrus Leaf Disease Detection", page_icon="🍋", layout="wide")

st.title("🍃 Citrus Leaf Disease Detection using Deep Learning")
st.markdown("Upload a citrus leaf image to detect the disease type and view prediction confidence.")

# ==============================
# 2️⃣ LOAD MODEL FROM ZIP
# ==============================

if not os.path.exists("citrus_model_retrained.keras"):
    with zipfile.ZipFile("citrus_model_retrained.zip", "r") as zip_ref:
        zip_ref.extractall(".")

model = tf.keras.models.load_model("citrus_model_retrained.keras")

# ==============================
# 3️⃣ DEFINE CLASS LABELS
# ==============================
labels = ["Black spot", "Melanose", "canker", "greening", "healthy"]

# ==============================
# 4️⃣ IMAGE UPLOAD
# ==============================
uploaded_file = st.file_uploader("📂 Upload Leaf Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    img = Image.open(uploaded_file).convert("RGB")
    st.image(img, caption="Uploaded Leaf", use_container_width=True)

    # ==============================
    # 5️⃣ PREPROCESSING
    # ==============================
    img = img.resize((224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = x / 255.0  # ✅ Normalization match with training

    # ==============================
    # 6️⃣ PREDICTION
    # ==============================
    pred = model.predict(x)
    predicted_class = labels[np.argmax(pred)]
    confidence = round(100 * np.max(pred), 2)

    # ==============================
    # 7️⃣ DISPLAY RESULTS
    # ==============================
    st.success(f"✅ Prediction: **{predicted_class} ({confidence}%)**")

    # ==============================
    # 8️⃣ PROBABILITY GRAPH
    # ==============================
    st.subheader("📊 Prediction Probabilities")
    fig, ax = plt.subplots()
    ax.bar(labels, pred[0] * 100)
    ax.set_xlabel("Classes")
    ax.set_ylabel("Confidence (%)")
    ax.set_title("Prediction Probabilities")
    st.pyplot(fig)

    # ==============================
    # 9️⃣ DISEASE INFORMATION PANEL
    # ==============================
    st.sidebar.header("🌿 Disease Information")
    disease_info = {
        "Black spot": ("Fungal infection with black circular spots.", "Use copper-based fungicide and remove infected leaves."),
        "Melanose": ("Fungal infection causing brown scabby spots.", "Prune affected twigs and apply fungicide."),
        "canker": ("Bacterial infection causing raised corky lesions.", "Remove infected leaves and spray bactericide."),
        "greening": ("Viral/bacterial disease leading to yellow mottling.", "Use disease-free plants and control psyllids."),
        "healthy": ("Leaf appears free from visible infections.", "Maintain balanced nutrients and good irrigation.")
    }

    about, solution = disease_info[predicted_class]
    st.sidebar.subheader(f"About {predicted_class}")
    st.sidebar.write(about)
    st.sidebar.subheader("💡 Solution")
    st.sidebar.write(solution)

