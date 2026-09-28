import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

from manual_demosaic import demosaic_bilinear

os.makedirs("results", exist_ok=True)

img = cv2.imread("images/kedi.jpg")

if img is None:
    raise FileNotFoundError("Image could not be loaded.")

img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Original image
#plt.imsave("results/original_rgb.png", img_rgb)

# Synthetic Bayer RAW
h, w, _ = img_rgb.shape
raw = np.zeros((h, w), dtype=np.uint8)

for i in range(h):
    for j in range(w):
        if i % 2 == 0 and j % 2 == 0:
            raw[i, j] = img_rgb[i, j, 0]   # R
        elif i % 2 == 1 and j % 2 == 1:
            raw[i, j] = img_rgb[i, j, 2]   # B
        else:
            raw[i, j] = img_rgb[i, j, 1]   # G

# plt.imsave("results/bayer_raw_gray.png", raw, cmap="gray")

# Bayer visual
bayer_visual = np.zeros((h, w, 3), dtype=np.uint8)

for i in range(h):
    for j in range(w):
        if i % 2 == 0 and j % 2 == 0:
            bayer_visual[i, j, 0] = img_rgb[i, j, 0]
        elif i % 2 == 1 and j % 2 == 1:
            bayer_visual[i, j, 2] = img_rgb[i, j, 2]
        else:
            bayer_visual[i, j, 1] = img_rgb[i, j, 1]

# plt.imsave("results/bayer_mosaic_color.png", bayer_visual)

# Demosaicing
demosaiced_basic = cv2.cvtColor(raw, cv2.COLOR_BayerRG2RGB)
demosaiced_basic = demosaiced_basic[:, :, ::-1]

demosaiced_ea = cv2.cvtColor(raw, cv2.COLOR_BayerRG2RGB_EA)
demosaiced_ea = demosaiced_ea[:, :, ::-1]

# plt.imsave("results/demosaiced_basic.png", demosaiced_basic)
# plt.imsave("results/demosaiced_edge_aware.png", demosaiced_ea)

# Comparison figure
plt.figure(figsize=(12, 4))

plt.subplot(1, 3, 1)
plt.imshow(img_rgb)
plt.title("Original RGB")
plt.axis("off")

plt.subplot(1, 3, 2)
plt.imshow(raw, cmap="gray")
plt.title("Synthetic Bayer RAW")
plt.axis("off")

plt.subplot(1, 3, 3)
plt.imshow(demosaiced_basic)
plt.title("Demosaiced (Basic)")
plt.axis("off")

plt.tight_layout()
# plt.savefig("results/pipeline_overview.png", dpi=200, bbox_inches="tight")
# plt.show()

# PSNR
basic_psnr = cv2.PSNR(img_rgb, demosaiced_basic)
ea_psnr = cv2.PSNR(img_rgb, demosaiced_ea)

print("Basic PSNR:", basic_psnr)
print("Edge-aware PSNR:", ea_psnr)

manual_demosaiced = demosaic_bilinear(raw)

manual_demosaiced = np.clip(
    manual_demosaiced,
    0,
    255
).astype(np.uint8)

manual_psnr = cv2.PSNR(img_rgb, manual_demosaiced)

print("Manual PSNR:", manual_psnr)