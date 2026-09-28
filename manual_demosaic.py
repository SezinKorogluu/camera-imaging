import numpy as np


def demosaic_bilinear(raw):

    raw = raw.astype(np.float32)

    h, w = raw.shape

    # Görüntünün etrafına 1 piksellik padding ekle
    padded = np.pad(raw, 1, mode="edge")

    rgb = np.zeros((h, w, 3), dtype=np.float32)

    for i in range(h):
        for j in range(w):

            # padded matristaki karşılığı
            pi = i + 1
            pj = j + 1

            # -------------------------
            # R position
            # -------------------------
            if i % 2 == 0 and j % 2 == 0:

                r = padded[pi, pj]

                g = (
                    padded[pi - 1, pj]
                    + padded[pi + 1, pj]
                    + padded[pi, pj - 1]
                    + padded[pi, pj + 1]
                ) / 4

                b = (
                    padded[pi - 1, pj - 1]
                    + padded[pi - 1, pj + 1]
                    + padded[pi + 1, pj - 1]
                    + padded[pi + 1, pj + 1]
                ) / 4

                rgb[i, j] = [r, g, b]

            # -------------------------
            # B position
            # -------------------------
            elif i % 2 == 1 and j % 2 == 1:

                b = padded[pi, pj]

                g = (
                    padded[pi - 1, pj]
                    + padded[pi + 1, pj]
                    + padded[pi, pj - 1]
                    + padded[pi, pj + 1]
                ) / 4

                r = (
                    padded[pi - 1, pj - 1]
                    + padded[pi - 1, pj + 1]
                    + padded[pi + 1, pj - 1]
                    + padded[pi + 1, pj + 1]
                ) / 4

                rgb[i, j] = [r, g, b]

            # -------------------------
            # G position on R row
            # R G R
            #   ↑
            # -------------------------
            elif i % 2 == 0 and j % 2 == 1:

                g = padded[pi, pj]

                # R sağ ve solda
                r = (
                    padded[pi, pj - 1]
                    + padded[pi, pj + 1]
                ) / 2

                # B üst ve altta
                b = (
                    padded[pi - 1, pj]
                    + padded[pi + 1, pj]
                ) / 2

                rgb[i, j] = [r, g, b]

            # -------------------------
            # G position on B row
            #   G
            # B G B
            # -------------------------
            else:

                g = padded[pi, pj]

                # R üst ve altta
                r = (
                    padded[pi - 1, pj]
                    + padded[pi + 1, pj]
                ) / 2

                # B sağ ve solda
                b = (
                    padded[pi, pj - 1]
                    + padded[pi, pj + 1]
                ) / 2

                rgb[i, j] = [r, g, b]

    return rgb