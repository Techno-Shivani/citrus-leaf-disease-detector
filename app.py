import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import base64

# ==============================
# 🌙 CUSTOM DARK-NEON UI DESIGN
# ==============================
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(145deg, #0f2027, #203a43, #2c5364);
    color: white;
}
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #141e30, #243b55);
    color: white;
}
h1, h2, h3, h4 {
    color: #00FFFF;
    text-shadow: 0 0 10px #00FFFF;
}
.stButton>button {
    background-color: #00FFFF;
    color: black;
    font-weight: bold;
    border-radius: 10px;
    box-shadow: 0 0 10px #00FFFF;
}
.stButton>button:hover {
    background-color: #008B8B;
    color: white;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ==============================
# 🌿 PAGE SETUP
# ==============================
st.title("🍋 Citrus Leaf Disease Detection")
st.write("Upload a citrus leaf image to detect if it’s **Healthy** or **Diseased**.")

# ==============================
# 🧠 LOAD MODEL & LABELS
# ==============================
@st.cache_resource
def load_model_and_labels():
    model = tf.keras.models.load_model("citrus_model_retrained.keras", compile=False)
    with open("class_labels.txt", "r") as f:
        labels = [line.strip() for line in f.readlines()]
    return model, labels

model, labels = load_model_and_labels()

# ==============================
# 🖼️ IMAGE UPLOAD SECTION
# ==============================
uploaded_image = st.file_uploader("Upload Leaf Image", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    image = Image.open(uploaded_image).convert("RGB")
    st.image(image, caption="Uploaded Leaf", use_column_width=True)

    # Preprocess the image
    img = image.resize((224, 224))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Make prediction
    pred = model.predict(img_array)
    predicted_class = labels[np.argmax(pred)]
    confidence = round(np.max(pred) * 100, 2)

    # Display result
    st.subheader("🩺 Prediction Result:")
    st.success(f"**{predicted_class.upper()}** leaf detected with **{confidence}%** confidence.")

    # Confidence chart
    st.write("### 📊 Class Probabilities:")
    for i, label in enumerate(labels):
        st.write(f"• {label}: {round(pred[0][i]*100, 2)} %")

else:
    st.info("⬆️ Upload a citrus leaf image to start detection.")

# ==============================
# 🧾 FOOTER
# ==============================
st.markdown("---")
st.markdown("Developed by **Shivani Chauhan** | Citrus Disease Detection 🌱")
