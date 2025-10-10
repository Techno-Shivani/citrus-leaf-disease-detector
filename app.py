import streamlit as st
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt

# -----------------------------
# 1️⃣ Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Citrus Leaf Disease Detection 🍋",
    page_icon="🌿",
    layout="wide"
)

st.title("🌿 Citrus Leaf Disease Detection using Deep Learning")
st.markdown("Upload a citrus leaf image to detect possible disease type.")

# -----------------------------
# 2️⃣ Load Model and Labels
# -----------------------------
@st.cache_resource
def load_citrus_model():
    model = load_model("citrus_model.keras")
    with open("class_labels.txt", "r") as f:
        labels = [line.strip() for line in f.readlines()]
    return model, labels

model, labels = load_citrus_model()

# -----------------------------
# 3️⃣ Image Upload Section
# -----------------------------
uploaded_file = st.file_uploader("📤 Upload Leaf Image", type=["jpg", "jpeg", "png"])

# -----------------------------
# 4️⃣ Prediction Function
# -----------------------------
def predict_disease(img):
    img = img.convert("RGB")
    img = img.resize((224, 224))                 # ✅ same as model input
    img_array = np.expand_dims(np.array(img), axis=0)
    # ⚠️ DO NOT divide by 255 (already handled inside model via Rescaling layer)
    prediction = model.predict(img_array)
    predicted_class = labels[np.argmax(prediction)]
    confidence = float(np.max(prediction) * 100)
    return predicted_class, confidence, prediction[0]

# -----------------------------
# 5️⃣ Display Prediction Result
# -----------------------------
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="🖼️ Uploaded Leaf", use_container_width=True)
    
    st.write("🔍 **Analyzing...**")
    predicted_class, confidence, prediction_values = predict_disease(image)

    st.success(f"✅ Prediction: **{predicted_class} ({confidence:.2f}%)**")

    # 📊 Plot prediction probabilities
    fig, ax = plt.subplots()
    ax.bar(labels, prediction_values * 100)
    ax.set_ylabel("Confidence (%)")
    ax.set_title("Prediction Probabilities")
    st.pyplot(fig)
