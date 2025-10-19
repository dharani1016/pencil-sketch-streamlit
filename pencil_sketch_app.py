import streamlit as st
import cv2
import numpy as np
from PIL import Image

# App title
st.title("🖌️ Pencil Sketch Generator")
st.write("Upload an image to convert it into a pencil sketch!")

# Upload image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Darkness control
scale_value = st.slider("Adjust Sketch Darkness", min_value=100, max_value=300, value=180, step=10)

if uploaded_file is not None:
    # Read image
    image = Image.open(uploaded_file)
    img = np.array(image)

    # Ensure image has 3 color channels
    if len(img.shape) == 2:  # grayscale
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    elif img.shape[2] == 4:  # RGBA
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # Invert image
    inv = 255 - gray

    # Blur the inverted image
    blur = cv2.GaussianBlur(inv, (21, 21), 0)

    # Invert the blurred image
    inv_blur = 255 - blur

    # Create pencil sketch
    sketch = cv2.divide(gray, inv_blur, scale=scale_value)

    # Show results side by side
    st.subheader("🖼️ Original vs Pencil Sketch")
    col1, col2 = st.columns(2)

    with col1:
        st.image(img, caption="Original Image", use_container_width=True)

    with col2:
        st.image(sketch, caption="Pencil Sketch", use_container_width=True, clamp=True)

    # Option to download the sketch
    result = Image.fromarray(sketch)
    st.download_button(
        label="📥 Download Pencil Sketch",
        data=cv2.imencode('.png', np.array(result))[1].tobytes(),
        file_name="pencil_sketch.png",
        mime="image/png"
    )
else:
    st.info("👆 Upload an image to get started.")
