import streamlit as st
import base64
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image

# Load model and labels
model = load_model("citrus_model.keras")
with open("class_labels.txt") as f:
    labels = [line.strip() for line in f]

# Function to set background
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
        background: linear-gradient(180deg, #001a00, #002200);
        padding: 20px;
    }}

    [data-testid="stSidebar"] h2 {{
        color: #ffff33; /* Yellow Glow */
        font-size: 24px !important;
        text-shadow: 0px 0px 15px #ffff66;
        font-weight: bold;
    }}

    /* Sidebar labels - white with glow */
    [data-testid="stSidebar"] label {{
        color: white !important;   
        font-size: 18px !important;  
        font-weight: bold !important;
        text-shadow: 0px 0px 6px #39ff14;
    }}

    [data-testid="stSidebar"] label:hover {{
        color: #ffff66 !important;  
        text-shadow: 0px 0px 10px yellow, 0px 0px 20px #39ff14;
        transform: scale(1.05);
    }}

    /* Caption under images */
    .caption {{
        color: white;
        font-weight: bold;
        font-size: 16px;
        text-align: center;
        text-shadow: 0px 0px 5px black;
   
