# 🖼️ Image Steganography using Python

🔒 **Hide secret messages inside images using Steganography**  

## 📌 Overview
This project implements **steganography** to embed **secret messages inside images** by manipulating pixel values in the **RGB color channels**. This enables **secure communication** while keeping the hidden data undetectable to the human eye.

## 🚀 Features
✅ Hide text messages inside images without visual distortion  
✅ Password-protected **encryption & decryption**  
✅ Uses **Python & OpenCV** for image processing  
✅ Supports **JPG, BMP, PNG** formats  
✅ **Simple command-line interface**  

## 🛠️ Technologies Used
- **Python 3.11**  
- **OpenCV (cv2)** – Image processing  
- **NumPy** – Data manipulation  

## 📂 Project Structure
📁 Image-Steganography/ │-- stego.py # Main script for encoding & decoding │-- mypic.bmp # Sample image for testing │-- README.md # Documentation │-- .gitignore # Files to ignore in Git

## 📥 Installation & Setup
1. **Clone the repository**
   git clone https://github.com/yourusername/Image-Steganography.git
   cd Image-Steganography
2. **Run the script**
   python stego.py

## 🖼️ Usage
# 🔑 Encryption (Hiding a Message)
1️⃣ Run stego.py
2️⃣ Enter the secret message
3️⃣ Enter a password
4️⃣ The encrypted image Encryptedmsg.jpg is generated

# 🔓 Decryption (Retrieving the Message)
1️⃣ Open stego.py
2️⃣ Enter the correct password
3️⃣ The hidden message is displayed

 # 🔮 Future Scope
Implement AES encryption for additional security
Develop a GUI-based tool for non-technical users
Extend the project to video & audio steganography

# 📜 License
This project is open-source under the MIT License.

🚀 Contributions & Feedback Welcome!
