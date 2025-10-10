import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import base64

# ---------- Page Configuration ----------
st.set_page_config(page_title="Citrus Leaf Disease Detection", layout="centered")

# ---------- Background Style ----------
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
    background-image: url("https://raw.githubusercontent.com/Techno-Shivani/citrus-leaf-disease-detector/main/bg.jpg");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    color: white;
}}
[data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
}}
h1, h2, h3, h4, h5 {{
    color: #00FFFF;
    text-shadow: 0 0 15px #00FFFF;
    font-weight: bold;
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# ---------- Title ----------
st.markdown("<h1 style='text-align:center;'>🍋 Citrus Leaf Disease Detection</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Upload a citrus leaf image to detect if it’s <b>Healthy</b> or <b>Diseased</b>.</p>", unsafe_allow_html=True)

# ---------- Load Model & Labels ----------
@st.cache_resource
def load_model_and_labels():
    model = tf.keras.models.load_model("citrus_model_retrained.keras", compile=False)
    with open("class_labels.txt", "r") as f:
        labels = [line.strip() for line in f.readlines()]
    return model, labels

model, labels = load_model_and_labels()

# ---------- Upload Section ----------
st.subheader("Upload Citrus Leaf Image")
uploaded_file = st.file_uploader("Upload an image (JPG, PNG)", type=["jpg", "jpeg", "png"])

# ---------- Prediction Function ----------
def predict_image(img):
    img = img.resize((224, 224))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    pred = model.predict(img_array)
    return pred

# ---------- When Image Uploaded ----------
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    with st.spinner("🔮 Analyzing image, please wait..."):
        pred = predict_image(image)
        pred_class = labels[np.argmax(pred)]
        confidence = round(np.max(pred) * 100, 2)

    # ---------- Result Display ----------
    color = "#00FFAA" if pred_class.lower() == "healthy" else "#FF5C5C"
    glow = "0 0 20px " + color

    st.markdown(
        f"""
        <div style='text-align:center; padding:25px; border-radius:20px; background:rgba(0,0,0,0.4);
                    box-shadow:inset {glow}; margin-top:30px;'>
            <h2 style='color:{color}; text-shadow:{glow};'>
            ⚡ Prediction: {pred_class.capitalize()} <br> 
            Confidence: {confidence}%
            </h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---------- Graph Display ----------
    fig, ax = plt.subplots()
    ax.barh(labels, pred[0]*100, color="cyan")
    ax.set_xlabel("Confidence (%)", color="white")
    ax.set_title("Prediction Probabilities", color="white")
    ax.tick_params(colors="white")
    st.pyplot(fig)
