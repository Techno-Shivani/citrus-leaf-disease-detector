from PIL import Image
import streamlit as st

# Background image set
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("https://raw.githubusercontent.com/Techno-Shivani/citrus-leaf-disease-detector/main/bg.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Example disease image load
black_spot_img = Image.open("black_spot.jpg")
st.image(black_spot_img, caption="Black Spot Example", use_column_width=True)
