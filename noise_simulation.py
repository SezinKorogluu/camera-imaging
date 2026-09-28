import cv2
import numpy as np
import matplotlib.pyplot as plt


img = cv2.imread("images/kedi.jpg")

if img is None:
    raise FileNotFoundError("Image could not be loaded.")

img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

h, w, _ = img_rgb.shape


# Create synthetic Bayer RAW
raw = np.zeros((h, w), dtype=np.float32)

for i in range(h):
    for j in range(w):

        if i % 2 == 0 and j % 2 == 0:
            raw[i, j] = img_rgb[i, j, 0]   # R

        elif i % 2 == 1 and j % 2 == 1:
            raw[i, j] = img_rgb[i, j, 2]   # B

        else:
            raw[i, j] = img_rgb[i, j, 1]   # G

noise_std = 40

noise = np.random.normal(
    loc=0,
    scale=noise_std,
    size=raw.shape
)

noisy_raw = raw + noise
noisy_raw = np.clip(noisy_raw, 0, 255)
plt.figure(figsize=(10, 4))

plt.subplot(1, 2, 1)
plt.imshow(raw, cmap="gray")
plt.title("Original Bayer RAW")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(noisy_raw, cmap="gray")
plt.title("Bayer RAW + Read Noise")
plt.axis("off")

plt.tight_layout()
plt.show()