import streamlit as st
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt

# -----------------------------
# Page setup
# -----------------------------
st.set_page_config(page_title="🍋 Citrus Leaf Disease Detector", page_icon="🌿", layout="wide")

# subtle background + typography
st.markdown("""
<style>
[data-testid="stAppViewContainer"]{background:linear-gradient(180deg,#dbf7d6, #c9f1c2);}
[data-testid="stHeader"]{background:rgba(0,0,0,0);}
h1,h2,h3{color:#064b2f !important;}
.block-container{padding-top:1.2rem;}
.sidebar .sidebar-content{background:transparent;}
.stSuccess{border-left:0.35rem solid #2e8b57;}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;'>🍃 Citrus Leaf Disease Detection using Deep Learning</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Upload a citrus leaf image to get the predicted disease and suggested remedy.</p>", unsafe_allow_html=True)
st.divider()

# -----------------------------
# Load model + labels (cached)
# -----------------------------
@st.cache_resource
def load_citrus_model_and_labels():
    model = load_model("citrus_model.keras")
    with open("class_labels.txt", "r") as f:
        labels = [ln.strip() for ln in f if ln.strip()]
    return model, labels

model, labels = load_citrus_model_and_labels()

# -----------------------------
# Disease info (keys EXACTLY labels ke jaisi)
# Make sure these names match class_labels.txt
# -----------------------------
disease_info = {
    "Black spot": {
        "image": "black_spot.jpg",
        "about": "A fungal disease causing dark lesions on leaves and fruits.",
        "solution": "Use copper-based fungicides and maintain orchard sanitation."
    },
    "Melanose": {
        "image": "melanose.jpg",
        "about": "Caused by Diaporthe citri; appears as small rough brown specks.",
        "solution": "Prune infected twigs; avoid overhead irrigation."
    },
    "canker": {
        "image": "canker.jpg",
        "about": "Bacterial infection leading to raised corky lesions on leaves & stems.",
        "solution": "Spray copper-based bactericides; remove severely infected parts."
    },
    "greening": {
        "image": "greening.jpg",
        "about": "Serious bacterial disease (HLB) spread by psyllids; causes yellowing & deformation.",
        "solution": "Control psyllids; rogue infected trees promptly."
    },
    "healthy": {
        "image": "healthy.jpg",
        "about": "Leaf appears free from visible infections.",
        "solution": "Continue monitoring and follow balanced nutrient schedule."
    }
}

# -----------------------------
# Upload UI
# -----------------------------
left, right = st.columns([1.1, 1.2])
with left:
    uploaded = st.file_uploader("📤 Upload a Leaf Image", type=["jpg", "jpeg", "png"])
with right:
    st.write(" ")

# -----------------------------
# Prediction helper
# -----------------------------
def predict(img: Image.Image):
    img = img.convert("RGB").resize((224, 224))         # match model input
    arr = np.expand_dims(np.array(img), axis=0)          # (1,224,224,3)
    # NOTE: do NOT divide by 255 (Rescaling layer is inside the model)
    probs = model.predict(arr, verbose=0)[0]             # shape (num_classes,)
    idx = int(np.argmax(probs))
    return labels[idx], float(probs[idx]*100), probs

# -----------------------------
# Main
# -----------------------------
if uploaded:
    # layout: image | results
    img_col, res_col = st.columns([1, 1.2], vertical_alignment="top")

    with img_col:
        img = Image.open(uploaded)
        st.image(img, caption="🖼️ Uploaded Leaf", use_container_width=True)

    with res_col:
        st.subheader("🔎 Analyzing image…")
        pred_class, conf, probs = predict(img)

        # Result box
        st.success(f"✅ Prediction: **{pred_class} ({conf:.2f}%)**")

        # Probability chart (tidy size)
        fig = plt.figure(figsize=(6.5, 3.6))
        plt.bar(labels, probs * 100)
        plt.ylabel("Confidence (%)")
        plt.title("Prediction Probabilities")
        plt.xticks(rotation=10)
        plt.grid(axis="y", alpha=0.25)
        plt.tight_layout()
        st.pyplot(fig)

    # -------------------------
    # Sidebar content (safe-get to avoid KeyError)
    # -------------------------
    info = disease_info.get(pred_class)
    st.sidebar.title("🌿 Disease Information")

    if info:
        try:
            st.sidebar.image(info["image"], use_container_width=True)
        except Exception:
            pass  # image optional; avoid crashing if missing
        st.sidebar.markdown(f"### About {pred_class}")
        st.sidebar.write(info["about"])
        st.sidebar.markdown("### 💡 Solution")
        st.sidebar.write(info["solution"])
    else:
        st.sidebar.info("No extra information available for this class.")

    # Optional: low-confidence notice
    if conf < 40:
        st.warning("Result confidence is low. Try another photo with better focus & lighting.")
else:
    st.info("📂 Please upload a citrus leaf image to begin.")
