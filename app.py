import streamlit as st
import base64
import numpy as np
import matplotlib.pyplot as plt
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
        background: linear-gradient(180deg, #001a00, #003300);
        padding: 20px;
    }}

    h1 {{
        color: #ffff33;
        text-align: center;
        font-size: 40px;
        font-family: 'Poppins', sans-serif;
        text-shadow: 0 0 10px #39ff14, 0 0 20px #39ff14, 0 0 40px #39ff14;
    }}

    h2 {{
        color: #fff;
        font-size: 24px;
    }}

    .disease-title {{
        font-size: 28px;
        color: #ffeb3b;
        font-weight: bold;
        text-shadow: 1px 1px 3px black;
    }}

    .about {{
        font-size: 18px;
        color: white;
    }}

    .solution {{
        font-size: 18px;
        color: #a5ffb5;
    }}

    .stButton>button {{
        background: linear-gradient(90deg, #39ff14, #ffff33);
        border-radius: 10px;
        color: black;
        font-size: 18px;
        font-weight: bold;
        padding: 10px 20px;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Call background
set_background("bg.jpg")

# ------------------ PREDICT FUNCTION ------------------
def predict_disease(img):
    img = img.convert("RGB").resize((224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0) / 255.0
    preds = model.predict(x)[0]
    result = {labels[i]: float(preds[i]) for i in range(len(labels))}
    predicted_label = labels[np.argmax(preds)]
    confidence = np.max(preds) * 100
    return predicted_label, confidence, result

# ------------------ SIDEBAR MENU ------------------
menu = st.sidebar.radio("🌿 Disease Information", [
    "🍂 Black Spot",
    "🍁 Melanose",
    "🌱 Canker",
    "🍃 Greening",
    "🌿 Healthy"
])

# Disease Info
disease_info = {
    "🍂 Black Spot": {
        "about": "Black spot is a fungal disease that causes dark circular spots on citrus leaves and fruits.",
        "solution": "Use copper-based fungicides, prune infected leaves, and improve air circulation."
    },
    "🍁 Melanose": {
        "about": "Melanose is a fungal disease common in young citrus leaves, causing small dark lesions.",
        "solution": "Apply protective fungicides like copper sprays and avoid overhead irrigation."
    },
    "🌱 Canker": {
        "about": "Canker is a bacterial disease causing raised corky lesions on leaves, stems, and fruit.",
        "solution": "Remove and burn infected parts, use resistant varieties, and copper sprays for prevention."
    },
    "🍃 Greening": {
        "about": "Greening (HLB) is a serious citrus disease caused by bacteria spread by psyllids.",
        "solution": "Control psyllid population, remove infected trees, and provide balanced nutrition."
    },
    "🌿 Healthy": {
        "about": "Healthy citrus leaves are green, shiny, and free of visible lesions or yellowing.",
        "solution": "Maintain proper irrigation, fertilization, and monitor for early signs of disease."
    }
}

# ------------------ UI MAIN ------------------
st.markdown("<h1>🌿 Citrus Leaf Disease Detector 🌿</h1>", unsafe_allow_html=True)

# Sidebar Info
st.sidebar.markdown(f"<h2 class='disease-title'>{menu}</h2>", unsafe_allow_html=True)
st.sidebar.markdown(f"<p class='about'><b>About:</b> {disease_info[menu]['about']}</p>", unsafe_allow_html=True)
st.sidebar.markdown(f"<p class='solution'><b>Solution:</b> {disease_info[menu]['solution']}</p>", unsafe_allow_html=True)

# Upload Section
st.subheader("📤 Upload a Citrus Leaf Image")
uploaded_file = st.file_uploader("Choose a leaf image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Leaf", use_container_width=True)

    if st.button("🔍 Predict Disease"):
        predicted_label, confidence, result = predict_disease(img)

        st.success(f"🌟 Prediction: **{predicted_label}** ({confidence:.2f}%)")

        # Show probability graph
        st.subheader("📊 Prediction Confidence")
        fig, ax = plt.subplots()
        ax.bar(result.keys(), result.values(), color="green")
        ax.set_ylabel("Confidence")
        ax.set_title("Model Prediction Probability")
        plt.xticks(rotation=45)
        st.pyplot(fig)
