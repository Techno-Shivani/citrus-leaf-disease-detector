import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
from pathlib import Path

# Load Model & Labels
model = tf.keras.models.load_model("citrus_model.keras")
labels = [l.strip() for l in open("class_labels.txt")]

# CSS
st.markdown("""
<style>
body {
    background: linear-gradient(120deg, #d9fdd3, #f0fff0);
    font-family: 'Poppins', sans-serif;
}
.neon-title {
    font-size: 48px;
    font-weight: 800;
    text-align: center;
    color: #eaff65;
    text-shadow: 0px 0px 6px #00ff88, 0px 0px 12px #00ff88, 0px 0px 18px #00ff88;
    margin-bottom: 15px;
}
.upload-box {
    background: rgba(255,255,255,0.8);
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 6px 18px rgba(0,0,0,0.1);
    text-align: center;
}
.result-box {
    background: #1b1b1b;
    color: white;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    margin-top: 15px;
}
.neon-btn {
    display: inline-block;
    padding: 12px 25px;
    background: linear-gradient(90deg,#00ff88,#eaff65);
    color: black;
    font-weight: 600;
    border-radius: 25px;
    text-decoration: none;
    transition: 0.3s;
    margin-top: 15px;
}
.neon-btn:hover {
    box-shadow: 0 0 10px #00ff88, 0 0 20px #eaff65;
    transform: scale(1.05);
}
.cards-grid {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 25px;
    margin-top: 40px;
}
.card {
    width: 260px;
    border-radius: 16px;
    overflow: hidden;
    background: white;
    box-shadow: 0px 6px 15px rgba(0,0,0,0.15);
    transition: 0.3s;
}
.card:hover {
    transform: translateY(-6px);
    box-shadow: 0px 10px 25px rgba(0,0,0,0.2);
}
.card img {
    width: 100%;
    height: 180px;
    object-fit: cover;
}
.card-body {
    padding: 15px;
    text-align: center;
}
.card-body h4 {
    color: #00994d;
    margin-bottom: 10px;
}
.card-body p {
    font-size: 14px;
    color: #444;
}
</style>
""", unsafe_allow_html=True)

# Heading
st.markdown('<div class="neon-title">🌿 Citrus Leaf Disease Detector</div>', unsafe_allow_html=True)

# Upload Section
col1, col2 = st.columns([1,1])
with col1:
    st.markdown('<div class="upload-box">', unsafe_allow_html=True)
    file = st.file_uploader("📂 Upload a Citrus Leaf Image", type=["jpg","jpeg","png"])
    if file:
        img = Image.open(file).convert("RGB").resize((224,224))
        st.image(img, caption="Uploaded Leaf", use_container_width=True)
        arr = np.expand_dims(np.array(img)/255.0, axis=0)
        preds = model.predict(arr)[0]
        top = np.argmax(preds)
        conf = preds[top]*100
        st.markdown(f'<div class="result-box">Prediction: <b>{labels[top]}</b> ({conf:.2f}%)</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Knowledge Cards
st.subheader("📘 Disease Knowledge Cards")
cards = [
  {"title": "Black Spot", "img": "black_spot.jpg", "about": "Dark circular lesions on leaves & fruits.", "solution": "Use copper fungicides & prune infected leaves."},
  {"title": "Melanose", "img": "melanose.jpg", "about": "Brown raised lesions with sandpaper texture.", "solution": "Remove dead twigs, apply copper sprays."},
  {"title": "Canker", "img": "canker.jpg", "about": "Raised corky lesions with yellow halo.", "solution": "Remove infected plants, use bactericides."},
  {"title": "Greening", "img": "greening.jpg", "about": "Blotchy mottling & bitter fruits.", "solution": "Control psyllids, remove infected trees."},
  {"title": "Healthy", "img": "healthy.jpg", "about": "Glossy green leaves & healthy fruits.", "solution": "Maintain nutrition & irrigation."},
]

st.markdown('<div class="cards-grid">', unsafe_allow_html=True)
for c in cards:
    html = f"""
    <div class="card">
      <img src="{c['img']}" alt="{c['title']}">
      <div class="card-body">
        <h4>{c['title']}</h4>
        <p><b>About:</b> {c['about']}</p>
        <p><b>Solution:</b> {c['solution']}</p>
      </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
