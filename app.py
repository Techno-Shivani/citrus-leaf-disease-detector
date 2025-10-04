import streamlit as st
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import base64

# ----------------- BACKGROUND IMAGE -----------------
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
        background-color: rgba(0,0,0,0.6);
        color: white;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Call background
set_background("bg.jpg")

# ----------------- LOAD MODEL -----------------
model = load_model("citrus_model.keras")

# Class labels
with open("class_labels.txt") as f:
    labels = [line.strip() for line in f]

# ----------------- TITLE -----------------
st.markdown(
    """
    <h1 style='text-align: center; color: #eaff00;
    text-shadow: 0 0 10px #39ff14, 0 0 20px #39ff14, 0 0 40px #39ff14;'>
    🍃 Citrus Leaf Disease Detector 🍃
    </h1>
    """,
    unsafe_allow_html=True,
)

# ----------------- UPLOAD IMAGE -----------------
uploaded_file = st.file_uploader("📤 Upload a Citrus Leaf Image", type=["jpg","jpeg","png"])

if uploaded_file is not None:
    img = image.load_img(uploaded_file, target_size=(224, 224))
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=False, width=350)

    # Preprocess
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = x / 255.0

    # Predict
    preds = model.predict(x)
    pred_class = labels[np.argmax(preds)]
    confidence = round(100 * np.max(preds), 2)

    # Result Card
    st.markdown(
        f"""
        <div style="background:rgba(0,0,0,0.7); padding:20px; border-radius:15px; 
        text-align:center; margin-top:20px; color:white;">
            <h2 style="color:#39ff14; text-shadow:0px 0px 10px yellow;">
            Prediction: {pred_class}</h2>
            <h3 style="color:#eaff00;">Confidence: {confidence}%</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # About + Solution
    st.markdown("---")
    st.markdown("### 🌱 About")
    if pred_class == "Black spot":
        st.write("Black spot causes dark circular lesions on leaves and fruits.")
        st.markdown("### 💡 Solution")
        st.write("Spray copper-based fungicides and remove infected leaves.")
    elif pred_class == "Canker":
        st.write("Canker causes raised brown lesions on leaves, stems, and fruit.")
        st.markdown("### 💡 Solution")
        st.write("Remove infected parts and use preventive sprays.")
    elif pred_class == "Melanose":
        st.write("Melanose causes small brown spots mainly on older leaves.")
        st.markdown("### 💡 Solution")
        st.write("Use fungicides and remove fallen debris.")
    elif pred_class == "Greening":
        st.write("Greening causes yellow shoots, misshaped fruits, and leaf mottling.")
        st.markdown("### 💡 Solution")
        st.write("Control psyllid insect vectors and remove infected trees.")
    else:
        st.write("Healthy leaf with no visible disease symptoms. 🌿")

