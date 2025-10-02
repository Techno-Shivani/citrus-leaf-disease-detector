import streamlit as st
from PIL import Image

# ================== PAGE CONFIG ==================
st.set_page_config(page_title="Citrus Leaf Disease Detector", layout="wide")

# ================== BACKGROUND IMAGE ==================
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://raw.githubusercontent.com/Techno-Shivani/citrus-leaf-disease-detector/main/bg.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    .big-font {
        font-size:22px !important;
        font-weight: bold;
        color: #2E8B57;
    }
    .solution-font {
        font-size:20px !important;
        color: #FF8C00;
        font-weight: bold;
    }
    .menu-title {
        font-size:30px !important;
        font-weight: bold;
        color: #006400;
        text-align: center;
        text-shadow: 2px 2px 4px #cce;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ================== TITLE ==================
st.markdown("<h1 class='menu-title'>🍃 Citrus Leaf Disease Detector 🍃</h1>", unsafe_allow_html=True)

# ================== MENU ==================
menu = ["Black Spot", "Canker", "Melanose", "Greening", "Healthy"]
choice = st.sidebar.radio("📌 Select a Disease", menu)

# ================== DISEASE DATA ==================
disease_data = {
    "Black Spot": {
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

# ================== DISPLAY DATA ==================
data = disease_data[choice]

col1, col2 = st.columns([1, 2])

with col1:
    st.image(Image.open(data["image"]), caption=f"{choice} Example", width=350)

with col2:
    st.markdown(f"<p class='big-font'>🌿 About:</p>", unsafe_allow_html=True)
    st.write(data["about"])
    st.markdown(f"<p class='solution-font'>💡 Solution:</p>", unsafe_allow_html=True)
    st.write(data["solution"])
