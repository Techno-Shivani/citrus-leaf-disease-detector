import streamlit as st
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt

# -----------------------------
# 1️⃣ Page Setup
# -----------------------------
st.set_page_config(
    page_title="🍋 Citrus Leaf Disease Detector",
    page_icon="🌿",
    layout="wide"
)

# Custom background color
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(to right, #c9f7c1, #a4e3a2);
}
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}
h1, h2, h3, h4 {
    color: #054a29 !important;
}
.stButton>button {
    background-color: #39b37e;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 0.6em 1.2em;
}
.stButton>button:hover {
    background-color: #2e8b57;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# -----------------------------
# 2️⃣ Title and Description
# -----------------------------
st.markdown("<h1 style='text-align:center;'>🍃 Citrus Leaf Disease Detection using Deep Learning</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Upload a citrus leaf image to detect the disease and view suggested remedies.</p>", unsafe_allow_html=True)
st.markdown("---")

# -----------------------------
# 3️⃣ Sidebar with Info
# -----------------------------
st.sidebar.image("bg.jpg", use_container_width=True)
st.sidebar.title("🌿 Disease Information")

disease_info = {
    "Black spot": {
        "About": "A fungal disease causing dark lesions on leaves and fruits.",
        "Solution": "Use copper-based fungicides and ensure proper sanitation in orchards."
    },
    "Melanose": {
        "About": "Caused by *Diaporthe citri* fungus; results in small brown specks on leaves.",
        "Solution": "Prune infected twigs and avoid overhead irrigation."
    },
    "Canker": {
        "About": "Bacterial infection leading to raised corky lesions on leaves and stems.",
        "Solution": "Spray copper-based bactericides and remove infected plant parts."
    },
    "Greening": {
        "About": "Serious bacterial disease transmitted by psyllid insects; causes yellowing and deformation.",
        "Solution": "Control psyllids and remove infected trees promptly."
    },
    "Healthy": {
        "About": "No infection detected — the leaf appears healthy.",
        "Solution": "Maintain regular monitoring and balanced nutrient supply."
    }
}

# -----------------------------
# 4️⃣ Load Model and Labels
# -----------------------------
@st.cache_resource
def load_citrus_model():
    model = load_model("citrus_model.keras")
    with open("class_labels.txt", "r") as f:
        labels = [line.strip() for line in f.readlines()]
    return model, labels

model, labels = load_citrus_model()

# -----------------------------
# 5️⃣ Upload and Predict
# -----------------------------
uploaded_file = st.file_uploader("📤 Upload a Leaf Image", type=["jpg", "jpeg", "png"])

def predict_disease(img):
    img = img.convert("RGB")
    img = img.resize((224, 224))
    img_array = np.expand_dims(np.array(img), axis=0)
    prediction = model.predict(img_array)
    predicted_class = labels[np.argmax(prediction)]
    confidence = float(np.max(prediction) * 100)
    return predicted_class, confidence, prediction[0]

# -----------------------------
# 6️⃣ Main Prediction UI
# -----------------------------
if uploaded_file is not None:
    col1, col2 = st.columns([1, 2])

    with col1:
        image = Image.open(uploaded_file)
        st.image(image, caption="📸 Uploaded Leaf", use_container_width=True)

    with col2:
        st.subheader("🔍 Analyzing Image...")
        predicted_class, confidence, prediction_values = predict_disease(image)
        st.success(f"✅ Prediction: **{predicted_class} ({confidence:.2f}%)**")

        # Display probability chart
        fig, ax = plt.subplots()
        ax.bar(labels, prediction_values * 100, color="#2e8b57")
        ax.set_ylabel("Confidence (%)")
        ax.set_title("Prediction Probabilities")
        st.pyplot(fig)

        # Sidebar Info Update
        st.sidebar.markdown(f"### 🩺 About {predicted_class}")
        st.sidebar.write(disease_info[predicted_class]["About"])
        st.sidebar.markdown("### 💡 Recommended Solution")
        st.sidebar.write(disease_info[predicted_class]["Solution"])

else:
    st.info("📂 Please upload a citrus leaf image to begin.")
