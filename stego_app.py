import streamlit as st
import cv2
import numpy as np
import tempfile
import os

import streamlit as st

# Set sky-blue gradient background
def set_skyblue_gradient_background():
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(to bottom, #87CEEB, #00BFFF);
            background-attachment: fixed;
        }
        .title-container {
            text-align: center;
            font-size: 2em;
            font-weight: bold;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }
        .description {
            text-align: center;
            font-size: 1.1em;
            margin-top: 10px;
            color: #333;
        }
        .footer {
            text-align: center;
            font-size: 1em;
            margin-top: 20px;
            color: #444;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
set_skyblue_gradient_background()

st.markdown(
    """
    <style>
    .decrypted-text {
        color: white;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

decrypted_message = "heyy"  # Example decrypted text
st.markdown(f'<p class="decrypted-text">Decrypted Message: {decrypted_message}</p>', unsafe_allow_html=True)


# Title with emoji and keeping it on one line
st.markdown('<div class="title-container">🖼️ Secure Image Steganography Web App 🔒</div>', unsafe_allow_html=True)

# Description with instructions
st.markdown(
    """
    <div class="description">
    Hide and retrieve secret messages from images using Steganography!<br>
    📌 <b>How to use:</b><br>
    1️⃣ Upload an image 📤 <br>
    2️⃣ Enter your secret message 📝 <br>
    3️⃣ Encrypt & Download the modified image 🔐<br>
    4️⃣ Upload the modified image to decrypt the message! 🔍
    </div>
    """, 
    unsafe_allow_html=True
)

# Footer
st.markdown('<div class="footer">Made with ❤️ by Rugved</div>', unsafe_allow_html=True)



# Function to hide a message in an image with password
def hide_message(image_path, message, password):
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)  # Read image correctly
    if img is None:
        return None, "Error: Invalid image file!"

    # Combine password with message
    full_message = password + "|" + message  # Store password with message
    d = {chr(i): i for i in range(256)}

    n, m, z = 1, 0, 0  # Start from (1,0) to avoid modifying metadata

    # Encode message length in the first two pixels (R and G channels)
    msg_length = len(full_message)
    max_length = (img.shape[0] * img.shape[1] * 3) - 2  # Max capacity (excluding length storage)
    if msg_length > max_length:
        return None, "Error: Message too long for this image!"

    img[0, 0, 0] = np.uint8(msg_length % 256)  # Store lower byte of length
    img[0, 0, 1] = np.uint8((msg_length // 256) % 256)  # Store upper byte of length

    # Encode message in image
    for i in range(msg_length):
        img[n, m, z] = np.uint8(d[full_message[i]])  # Convert char to int
        m += 1
        if m >= img.shape[1]:  # Move to next row if end of column
            m = 0
            n += 1
        z = (z + 1) % 3  # Cycle through RGB

    encrypted_image_path = "encrypted_image.png"
    cv2.imwrite(encrypted_image_path, img)
    return encrypted_image_path, "Message hidden successfully!"

# Function to reveal message from an image using password
def reveal_message(image_path, password):
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)  # Read image correctly
    if img is None:
        return "Error: Invalid image file!"

    d = {i: chr(i) for i in range(256)}

    # Retrieve message length from the first two pixels (R and G channels)
    msg_length = int(img[0, 0, 0]) + (int(img[0, 0, 1]) * 256)  # Read length from two channels

    message = ""
    n, m, z = 1, 0, 0  # Start reading from (1,0)

    for i in range(msg_length):  # Read only the exact number of characters
        if n >= img.shape[0]:
            break
        message += d[int(img[n, m, z])]  # Convert int back to char
        m += 1
        if m >= img.shape[1]:  # Move to next row if end of column
            m = 0
            n += 1
        z = (z + 1) % 3  # Cycle through RGB

    # Ensure message contains the password separator "|"
    if "|" not in message:
        return "Error: Decryption failed. Message format is incorrect!"

    # Split password and message
    stored_password, secret_message = message.split("|", 1)

    if stored_password == password:
        return f"Decrypted Message: {secret_message}"
    else:
        return "Error: Incorrect password!"

# Define `temp_image_path` outside to prevent NameError
temp_image_path = None  

# Upload an image
uploaded_file = st.file_uploader("Choose an image", type=["png", "jpg", "bmp"])

if uploaded_file is not None:
    # Save uploaded image to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_image_path = temp_file.name  # Define temp_image_path here
    
    st.image(temp_image_path, caption="Uploaded Image", use_container_width=True)

    # Hide Message
    st.subheader("🔑 Hide a Secret Message")
    message = st.text_area("Enter your secret message")
    password = st.text_input("Enter a password", type="password")  # Password field

    if st.button("Encrypt and Save"):
        if temp_image_path and password:
            encrypted_image_path, result = hide_message(temp_image_path, message, password)
            if encrypted_image_path:
                st.image(encrypted_image_path, caption="Encrypted Image", use_container_width=True)
                with open(encrypted_image_path, "rb") as file:
                    st.download_button(label="Download Encrypted Image", data=file, file_name="encrypted_image.png", mime="image/png")
            st.success(result)
        else:
            st.error("Please upload an image and enter a password!")

    # Reveal Message
    st.subheader("🔓 Reveal a Secret Message")
    decrypt_password = st.text_input("Enter the password to decrypt", type="password")

    if st.button("Decrypt Message"):
        if temp_image_path and decrypt_password:
            decrypted_message = reveal_message(temp_image_path, decrypt_password)
            st.info(decrypted_message)
        else:
            st.error("Please upload an encrypted image and enter the correct password!")

# Cleanup temp files (Only if `temp_image_path` exists)
if temp_image_path and os.path.exists(temp_image_path):
    os.remove(temp_image_path)
