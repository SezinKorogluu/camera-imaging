## Demosaicing Evaluation

The synthetic Bayer RAW image was reconstructed using two demosaicing methods provided by OpenCV:

- Basic demosaicing
- Edge-aware demosaicing

The reconstructed images were compared with the original RGB image using PSNR (Peak Signal-to-Noise Ratio).

### Results

| Method | PSNR |
|---|---:|
| Basic Demosaicing | 40.2877 dB |
| Edge-Aware Demosaicing | 40.3005 dB |

Both methods produced a reconstruction close to the original image. The edge-aware method achieved a slightly higher PSNR.

During evaluation, an RGB/BGR channel-order mismatch was also identified. Before correcting the channel order, the measured PSNR was approximately 16.77 dB. After correcting the channel alignment, the PSNR increased to approximately 40.29 dB.

This highlighted the importance of consistent color-channel ordering when working with OpenCV image-processing pipelines.