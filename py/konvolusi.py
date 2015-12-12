import numpy as np

import nph
import gambar

def sobel(gray):
    operator_baris = [[1, 2, 1],
                      [0, 0, 0],
                      [-1, -2, -1]]
    operator_kolom = [[1, 0, -1],
                      [2, 0, -2],
                      [1, 0, -1]]
    
    result = operate(gray, operator_baris, operator_kolom)
    return normalize(result)

def gaussian(img):
    # kernel = [1, 3, 5, 3, 1]
    kernel = [1, 4, 7, 9, 7, 4, 1]
    
    kernel_count = len(kernel)
    kernel_half = (kernel_count-1)/2
    rolls = range(0, len(kernel))
    result = np.zeros(img.shape, dtype=np.float)
    
    rolls[kernel_half] = img.astype(np.float)
    for i in range(1, kernel_half+1):
        rolls[kernel_half+i] = nph.roll_left(rolls[kernel_half+i-1])
        rolls[kernel_half-i] = nph.roll_right(rolls[kernel_half-i+1])
    for i in range(0, kernel_count):
        result += rolls[i] * kernel[i]
    result /= sum(kernel)
    
    rolls[kernel_half] = result.copy()
    result = 0
    for i in range(1, kernel_half+1):
        rolls[kernel_half+i] = nph.roll_up(rolls[kernel_half+i-1])
        rolls[kernel_half-i] = nph.roll_down(rolls[kernel_half-i+1])
    for i in range(0, kernel_count):
        result += rolls[i] * kernel[i]
    result /= sum(kernel)
    
    return result.round().astype(np.uint8)

def operate(gray, operator_baris, operator_kolom):
    result = np.zeros(gray.shape, dtype=np.int32)
    rolled = nph.roll_down(gray)
    
    for y in range(0, 3):
        for x in range(0, 3):
            result = result + mulsum(gray, operator_baris, operator_kolom, y, x)
    
    return np.absolute(result)

# comparator
def o_naive(gray, operator_baris, operator_kolom):
    result = np.zeros(gray.shape, dtype=np.int32)
    for y in range(1, gray.shape[0] - 1):
        for x in range(1, gray.shape[1] - 1):
            sum = 0
            for m in range(-1, 2):
                for n in range(-1, 2):
                    sum += operator_baris[m+1][n+1] * gray[y+m][x+n]
                    sum += operator_kolom[m+1][n+1] * gray[y+m][x+n]
            result[y, x] = sum
    return result

def mulsum(gray, operator_baris, operator_kolom, y, x):
    rolled = np.array(gray, dtype=np.int32)
    
    if y == 0:
        rolled[:] = nph.roll_down(rolled)
    elif y == 2:
        rolled[:] = nph.roll_up(rolled)
    
    if x == 0:
        rolled[:] = nph.roll_right(rolled)
    elif x == 2:
        rolled[:] = nph.roll_left(rolled)
    
    return rolled * (operator_baris[y][x] + operator_kolom[y][x])

def normalize(matrix):
    min = matrix.min()
    max = matrix.max()
    result = (matrix - min) * 255.0 / (max - min)
    return result.astype(np.uint8)

def kirsch(gray):
    dummy = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    kernel = np.array([[5, 5, 5,],
                       [-3, 0, -3],
                       [-3, -3, -3]])
    
    results = []
    for i in range(0, 8):
        results.append(operate(gray, kernel, dummy))
        kernel[:] = nph.rot45(kernel)
    
    result = results[0]
    for i in range(1, 8):
        result[:] = np.maximum(result, results[i])
    
    return normalize(result)

if __name__ == '__main__':
    # test = np.asarray([[255, 255, 255, 255, 255, 255, 255, 255],
                       # [255, 255, 255, 255, 255, 255, 255, 255],
                       # [255, 255, 0, 0, 0, 0, 255, 255],
                       # [255, 255, 0, 0, 0, 0, 255, 255],
                       # [255, 255, 0, 0, 0, 0, 255, 255],
                       # [255, 255, 0, 0, 0, 0, 255, 255],
                       # [255, 255, 255, 255, 255, 255, 255, 255],
                       # [255, 255, 255, 255, 255, 255, 255, 255]])
    # sobel(test)
    
    img = gambar.read('D:\\Kuliah\\pola\\527C868C9284958A22F9E4D448BDDA12.JPG')
    gauss = gaussian(img)
    gambar.show(gauss)