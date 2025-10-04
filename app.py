import streamlit as st
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import base64

# ---------------- BACKGROUND IMAGE ----------------
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
        background-color: rgba(0,0,0,0.65);
        color: white;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_background("bg.jpg")

# ---------------- LOAD MODEL ----------------
model = load_model("citrus_model.keras")

with open("class_labels.txt") as f:
    labels = [line.strip() for line in f]

# ---------------- TITLE ----------------
st.markdown(
    """
    <h1 style='text-align: center; color: #eaff00;
    text-shadow: 0 0 15px #39ff14, 0 0 25px #39ff14, 0 0 45px yellow;'>
    🍃 Citrus Leaf Disease Detector 🍃
    </h1>
    """,
    unsafe_allow_html=True,
)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------- SIDEBAR - KNOWLEDGE CARDS ----------------
st.sidebar.markdown(
    "<h2 style='color:#39ff14;text-shadow:0 0 10px yellow;'>📌 Disease Information</h2>",
    unsafe_allow_html=True,
)

disease = st.sidebar.radio("Select a disease", labels)

disease_info = {
    "Black spot": {
        "image": "black_spot.jpg",
        "about": "Black spot is a fungal disease that creates dark circular lesions on citrus leaves, stems, and fruits. It reduces photosynthesis, weakens the plant, and makes fruits less marketable.",
        "solution": "Apply copper-based fungicides at early stages. Remove and destroy infected leaves and fruits. Improve air circulation by pruning dense foliage."
    },
    "Canker": {
        "image": "canker.jpg",
        "about": "Citrus canker is a bacterial disease causing raised, corky lesions surrounded by yellow halos. It spreads rapidly via wind, rain, and contaminated tools.",
        "solution": "Remove and destroy infected plant material. Spray preventive copper-based bactericides. Ensure strict sanitation of tools and equipment."
    },
    "Melanose": {
        "image": "melanose.jpg",
        "about": "Melanose is a fungal disease mostly affecting older leaves and twigs. It causes small, brown, raised spots that reduce fruit quality.",
        "solution": "Remove dead twigs where the fungus survives. Use fungicidal sprays during wet seasons. Keep orchards clean from fallen leaves and debris."
    },
    "Greening": {
        "image": "greening.jpg",
        "about": "Citrus greening (HLB) is one of the most serious citrus diseases. It causes yellow shoots, mottled leaves, green but bitter fruits, and tree decline.",
        "solution": "Control psyllid insects that transmit HLB using insecticides. Remove infected trees immediately. Use certified disease-free planting material."
    },
    "Healthy": {
        "image": "healthy.jpg",
        "about": "The leaf shows no visible signs of disease, maintaining normal shape, size, and color. Photosynthesis and plant growth are optimal.",
        "solution": "Maintain good orchard hygiene, ensure balanced fertilization, and monitor regularly for any early signs of disease."
    }
}

# Show disease image + info
if disease in disease_info:
    st.sidebar.image(disease_info[disease]["image"], caption=f"{disease} Example", use_column_width=True)
    st.sidebar.markdown(f"### 🌱 About:\n{disease_info[disease]['about']}")
    st.sidebar.markdown(f"### 💡 Solution:\n{disease_info[disease]['solution']}")

# ---------------- UPLOAD + PREDICTION ----------------
uploaded_file = st.file_uploader("📤 Upload a Citrus Leaf Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    img = image.load_img(uploaded_file, target_size=(224, 224))
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=False, width=350)

    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = x / 255.0

   
