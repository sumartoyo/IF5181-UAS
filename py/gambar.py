import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import sys

import nph

def read(path):
    img = mpimg.imread(path)
    if img.dtype == 'float32':
        return (img*255).astype(np.uint8)
    if len(img.shape) < 3:
        return to_img(img)
    return img

def to_gray(img):
    return img.mean(-1).round().astype(np.uint8)

def to_bw(gray):
    hist = get_histogram(gray)
    threshold = otsu(hist, gray.shape[0]*gray.shape[1])
    return gray <= threshold

def to_img(matrix):
    if len(matrix.shape) == 3:
        return matrix
    matrixr = (matrix-1)*-255 if matrix.dtype == 'bool' else np.asarray(matrix)
    return (matrixr.reshape(matrixr.shape + (1,))
                   .repeat(3, -1)
                   .astype(np.uint8))

def contrasting(gray):
    min = gray.min()
    max = gray.max()
    result = (gray - min) * 255.0 / (max - min)
    return result.astype(np.uint8)

def equalize(gray, hist):
    cdf = np.cumsum(hist)
    pixels = gray.shape[0]*gray.shape[1]
    nonzero = np.nonzero(cdf)
    min = 0 if nonzero[0].shape[0] == 0 else cdf[nonzero][0]
    min += 0.
    h = ((cdf-min)/(pixels-min)*255).round().astype(np.uint8)
    result = h[gray.flatten()].reshape(gray.shape)
    result_hist = get_histogram(result)
    return (result, result_hist)

def show(img):
    plt.imshow(to_img(img), interpolation='nearest')
    plt.show()

def save(img, path):
    mpimg.imsave(path, to_img(img))

def koponging(bw):
    bwr = bw.copy()
    
    # remove filler
    rollup, rolldown, rollleft, rollright = nph.roll_all(bwr)
    bwr -= bwr * rolldown * rollup * rollright * rollleft
    
    # remove zigzag
    rollup, rollright = nph.roll_up(bwr), nph.roll_right(bwr)
    rolldownleft = nph.roll_left(nph.roll_down(bwr))
    bwr -= bwr * rollup * rollright * (rolldownleft == False)
    
    rollright, rolldown = nph.roll_right(bwr), nph.roll_down(bwr)
    rollupleft = nph.roll_left(nph.roll_up(bwr))
    bwr -= bwr * rollright * rolldown * (rollupleft == False)
    
    rolldown, rollleft = nph.roll_down(bwr), nph.roll_left(bwr)
    rollupright = nph.roll_right(nph.roll_up(bwr))
    bwr -= bwr * rolldown * rollleft * (rollupright == False)
    
    rollleft, rollup = nph.roll_left(bwr), nph.roll_up(bwr)
    rolldownright = nph.roll_right(nph.roll_down(bwr))
    bwr -= bwr * rollleft * rollup * (rolldownright == False)
    
    return bwr

def get_histogram(channel):
    return np.histogram(channel, range=(0, 256), bins=256)[0]

def otsu(hist, pixels):
    sum = (hist*range(0, 256)).sum()
    sumb = wb = wf = varmax = threshold = 0.
    for t in range(0, 256):
        wb += hist[t]
        if wb == 0:
            continue
        wf = pixels-wb
        if wf == 0:
            break
        sumb += t*hist[t]
        mb = sumb/wb
        mf = (sum-sumb)/wf
        varbetween = wb*wf*(mb-mf)*(mb-mf)
        if varbetween > varmax:
            varmax = varbetween
            threshold = t
    return threshold

if __name__ == ('__main__'):
    img = read('c:\\users\\user all\\Downloads\\otsu-pre.jpg')
    gray = to_gray(img)
    hist = get_histogram(gray)
    threshold = otsu(hist, gray.shape[0]*gray.shape[1])
    show(gray <= threshold)