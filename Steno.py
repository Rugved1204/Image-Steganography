import cv2
import os
import numpy as np

img = cv2.imread("mypic.bmp")

if img is None:
    print("Error: Image not loaded. Check the file path and format.")
    exit()
else:
    print("Image loaded successfully!")

if img is None:
    print("Error: Image not found. Check the filename and path.")
    exit()

msg = input("Enter secret message: ")
password = input("Enter password: ")

d = {chr(i): i for i in range(256)}
c = {i: chr(i) for i in range(256)}

height, width, _ = img.shape
n, m, z = 0, 0, 0

# Ensure message fits in the image
if len(msg) > height * width:
    print("Error: Message is too long for the image!")
    exit()

# Encode message into the image
for char in msg:
    img[n, m, z] = d[char]  # Convert character to int
    m += 1
    if m >= width:
        m = 0
        n += 1
    z = (z + 1) % 3  # Cycle through R, G, B channels

cv2.imwrite("Encryptedmsg.jpg", img)

# Open encrypted image
import platform
if platform.system() == "Windows":
    os.system("start Encryptedmsg.jpg")
else:
    os.system("xdg-open Encryptedmsg.jpg")

# Decryption
message = ""
n, m, z = 0, 0, 0

pas = input("Enter passcode for decryption: ")

if password == pas:
    for _ in range(len(msg)):
        message += c[img[n, m, z]]
        m += 1
        if m >= width:
            m = 0
            n += 1
        z = (z + 1) % 3
    print("Decrypted message:", message)
else:
    print("Invalid password!")