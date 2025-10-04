import streamlit as st
from pathlib import Path

st.markdown("""
<style>
/* Clean neon heading */
.neon-title{
  font-family: 'Poppins', sans-serif;
  font-size: 42px;
  font-weight: 800;
  text-align: center;
  background: linear-gradient(90deg, #eaff65, #00ff88);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 0 8px rgba(0,255,136,0.6), 0 0 14px rgba(234,255,101,0.6);
  margin: 25px 0;
}

/* Grid */
.cards-grid{
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 25px;
  padding: 20px 0;
}

/* Flip Card */
.flip-card{
  width: 260px;
  height: 340px;
  perspective: 1000px;
}

.flip-card-inner{
  position: relative;
  width: 100%;
  height: 100%;
  text-align: center;
  transition: transform 0.6s;
  transform-style: preserve-3d;
}
.flip-card:hover .flip-card-inner{
  transform: rotateY(180deg);
}

/* Faces */
.flip-face{
  position: absolute;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 6px 18px rgba(0,0,0,0.2);
}

/* Front */
.flip-front{
  background: #fff;
}
.flip-front img{
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Back */
.flip-back{
  background: linear-gradient(135deg,#00c36f,#eaff65);
  color: #0e261a;
  transform: rotateY(180deg);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 18px;
}
.flip-back h4{
  margin: 6px 0;
  font-size: 20px;
  font-weight: 700;
}
.flip-back p{
  font-size: 14px;
  line-height: 1.4;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="neon-title">🌿 Citrus Leaf Disease — Knowledge Cards</div>', unsafe_allow_html=True)

# Cards data
cards = [
  {"title": "Black Spot", "img": "black_spot.jpg", 
   "about": "Dark circular lesions on citrus leaves and fruits.",
   "solution": "Use copper-based fungicides and prune infected areas."},
  {"title": "Melanose", "img": "melanose.jpg", 
   "about": "Small raised brown lesions, sandpaper-like feel.",
   "solution": "Remove dead twigs and apply copper sprays."},
  {"title": "Canker", "img": "canker.jpg", 
   "about": "Raised corky lesions with yellow halo, bacterial disease.",
   "solution": "Remove infected plants and use bactericides."},
  {"title": "Greening", "img": "greening.jpg", 
   "about": "Blotchy mottling, bitter fruits. Spread by psyllids.",
   "solution": "Remove infected trees and control psyllids."},
  {"title": "Healthy", "img": "healthy.jpg", 
   "about": "Glossy deep-green leaves and healthy fruits.",
   "solution": "Balanced nutrients and proper irrigation."},
]

# Render
st.markdown('<div class="cards-grid">', unsafe_allow_html=True)
for c in cards:
    img_path = str(Path(c["img"]))
    html = f"""
    <div class="flip-card">
      <div class="flip-card-inner">
        <div class="flip-face flip-front">
          <img src="{img_path}" alt="{c['title']} image">
        </div>
        <div class="flip-face flip-back">
          <h4>{c['title']}</h4>
          <p><b>About:</b> {c['about']}</p>
          <p><b>Solution:</b> {c['solution']}</p>
        </div>
      </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
