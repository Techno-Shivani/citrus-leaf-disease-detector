import streamlit as st
from pathlib import Path

st.markdown("""
<style>
/* ---------- THEME ---------- */
:root{
  --card-w: 280px;
  --card-h: 360px;
  --radius: 20px;
  --grad1: #d8ff6b;         /* yellow-green glow */
  --grad2: #00b86b;         /* deep green */
  --text: #0e271a;
  --heading: #eaff87;       /* neon yellow */
}

/* Page heading neon */
.neon-title{
  font-family: 'Poppins', system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
  font-weight: 800;
  font-size: clamp(28px, 3.8vw, 44px);
  letter-spacing: .5px;
  text-align: center;
  color: var(--heading);
  text-shadow:
    0 0 6px rgba(234,255,135,.9),
    0 0 18px rgba(0,255,140,.6),
    0 0 36px rgba(0,180,100,.35);
  margin: 8px 0 22px 0;
  display: block;
}

/* ---------- GRID CONTAINER ---------- */
.cards-grid{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(var(--card-w), 1fr));
  gap: 22px;
  justify-items: center;
}

/* ---------- FLIP CARD ---------- */
.flip-card{
  width: var(--card-w);
  height: var(--card-h);
  perspective: 1200px; /* depth */
}

.flip-card-inner{
  position: relative;
  width: 100%;
  height: 100%;
  transform-style: preserve-3d;
  transition: transform .7s cubic-bezier(.2,.85,.2,1);
  border-radius: var(--radius);
  box-shadow: 0 14px 38px rgba(0, 80, 45, .18), inset 0 0 0 1px rgba(255,255,255,.04);
  background: linear-gradient(135deg, rgba(216,255,107,.18), rgba(0,184,107,.18));
  backdrop-filter: blur(4px);
}
.flip-card:hover .flip-card-inner{
  transform: rotateY(180deg);
}

/* Faces */
.flip-face{
  position: absolute;
  inset: 0;
  backface-visibility: hidden;
  border-radius: var(--radius);
  overflow: hidden;
}

/* Front face (image) */
.flip-front{
  display: grid;
  grid-template-rows: 1fr auto;
  background: #0f291c;
}
.flip-front img{
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: saturate(1.05) contrast(1.05);
}
.badge{
  place-self: end center;
  margin: 10px;
  background: linear-gradient(135deg, var(--grad1), var(--grad2));
  color: #0e261a;
  font-weight: 700;
  padding: 8px 14px;
  border-radius: 999px;
  box-shadow: 0 8px 18px rgba(0,184,107,.35);
  border: 1px solid rgba(255,255,255,.25);
}

/* Back face (text) */
.flip-back{
  transform: rotateY(180deg);
  background:
    radial-gradient(1200px 420px at -10% -20%, rgba(216,255,107,.18), transparent 55%),
    radial-gradient(1000px 380px at 120% 120%, rgba(0,184,107,.18), transparent 60%),
    #0b1f15;
  color: #e7ffe9;
  padding: 18px 18px 16px;
  display: grid;
  grid-template-rows: auto 1fr auto;
  gap: 10px;
}
.flip-back h4{
  margin: 2px 0 0;
  font-family: 'Poppins', system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
  font-weight: 800;
  letter-spacing: .3px;
  color: #d9ffd8;
}
.kicker{
  font-size: 12px;
  letter-spacing: 1.2px;
  color: #b8f7c9;
  text-transform: uppercase;
}
.desc{
  font-size: 14.5px;
  line-height: 1.45;
  color: #defbe7;
}
.sol{
  margin-top: 2px;
  font-size: 14.5px;
  line-height: 1.45;
  color: #fffde0;
}
.cta{
  align-self: end;
  display: inline-flex;
  gap: 10px;
  margin-top: 6px;
}
.btn-ghost, .btn-solid{
  font-weight: 700;
  padding: 8px 12px;
  border-radius: 10px;
  text-decoration: none;
  border: 1px solid rgba(233,255,166,.5);
  transition: all .2s ease;
}
.btn-ghost{
  color: #eaff87;
  background: rgba(233,255,166,.06);
}
.btn-ghost:hover{
  background: rgba(233,255,166,.14);
}
.btn-solid{
  color: #09321f;
  background: linear-gradient(135deg, var(--grad1), var(--grad2));
  box-shadow: 0 8px 18px rgba(0,184,107,.35), 0 0 0 4px rgba(233,255,166,.12);
}
.btn-solid:hover{
  filter: brightness(1.05);
}

/* Sub section heading */
.subhead{
  margin: 26px 0 6px;
  color: var(--text);
  font-weight: 800;
  letter-spacing: .3px;
  text-align: center;
  font-family: 'Poppins', system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<span class="neon-title">🌿 Citrus Leaf Disease — Knowledge Cards</span>', unsafe_allow_html=True)

# ---- Data for cards (edit text freely) ----
cards = [
  {
    "title": "Black spot",
    "img": "black_spot.jpg",
    "about": "Black spot causes dark circular lesions on citrus leaves and fruits; prolonged infection reduces yield.",
    "solution": "Prune infected twigs, dispose fallen debris. Use copper-based fungicide after rainy spells; ensure good airflow."
  },
  {
    "title": "Melanose",
    "img": "melanose.jpg",   # file name as per your repo
    "about": "Small brown raised lesions giving a sandpaper feel; common on younger leaves and fruit peels.",
    "solution": "Remove dead wood (main source of spores). Apply copper sprays pre- and post-bloom; avoid overhead irrigation."
  },
  {
    "title": "Canker",
    "img": "canker.jpg",
    "about": "Bacterial lesions with raised corky centers and yellow halos; spreads fast via wind + rain.",
    "solution": "Rogue heavily infected plants; copper-based bactericides; install windbreaks; sanitize tools regularly."
  },
  {
    "title": "Greening (HLB)",
    "img": "greening.jpg",
    "about": "Blotchy leaf mottling, misshapen bitter fruit. Spread by psyllids—no cure, only management.",
    "solution": "Remove infected trees, control psyllids, plant certified disease-free stock, feed with micronutrients."
  },
  {
    "title": "Healthy",
    "img": "healthy.jpg",
    "about": "Glossy deep-green leaves, uniform canopy and normal sized, flavorful fruits—signs of good health.",
    "solution": "Keep balanced NPK + micronutrients, irrigate evenly, mulch, and monitor for early symptoms."
  },
]

# ---- Render Grid ----
st.markdown('<h3 class="subhead">Tap / hover to flip & read details</h3>', unsafe_allow_html=True)
st.markdown('<div class="cards-grid">', unsafe_allow_html=True)

for c in cards:
    img_path = str(Path(c["img"]))
    card_html = f"""
    <div class="flip-card">
      <div class="flip-card-inner">
        <div class="flip-face flip-front">
          <img src="{img_path}" alt="{c['title']} example"/>
          <div class="badge">{c['title']}</div>
        </div>
        <div class="flip-face flip-back">
          <span class="kicker">About</span>
          <h4>{c['title']}</h4>
          <p class="desc">{c['about']}</p>
          <span class="kicker" style="margin-top:6px;">Solution</span>
          <p class="sol">{c['solution']}</p>
          <div class="cta">
            <a class="btn-ghost" href="#predict">Predict</a>
            <a class="btn-solid" href="#predict">Try on your leaf</a>
          </div>
        </div>
      </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
