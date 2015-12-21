import numpy as np

import nph
import gambar

def convolve(gray, kernel):
    mid = (len(kernel)-1)/2
    rolls = create_rolls(gray, kernel)
    result = np.zeros(gray.shape, dtype=np.float)
    for y in range(0, len(kernel)):
        for x in range(0, len(kernel)):
            result += rolls[y][x] * kernel[y][x]
    return result

def create_rolls(gray, kernel):
    mid = (len(kernel)-1)/2
    
    rolls = []
    for y in kernel:
        roll = []
        for x in y:
            roll.append(gray.copy().astype(np.float))
        rolls.append(roll)
    
    for i in range(0, mid):
        for j in range(0, i+1):
            for k in range(0, len(rolls)):
                rolls[j][k][:] = nph.roll_down(rolls[j][k], rolls[mid][j][0].copy())
    
    for i in range(len(rolls)-1, mid, -1):
        for j in range(len(rolls)-1, i-1, -1):
            for k in range(0, len(rolls)):
                rolls[j][k][:] = nph.roll_up(rolls[j][k], rolls[mid][j][-1].copy())
    
    for i in range(0, mid):
        for j in range(0, i+1):
            for k in range(0, len(rolls)):
                rolls[k][j][:] = nph.roll_right(rolls[k][j], rolls[k][mid][:, 0].copy())
    
    for i in range(len(rolls)-1, mid, -1):
        for j in range(len(rolls)-1, i-1, -1):
            for k in range(0, len(rolls)):
                rolls[k][j][:] = nph.roll_left(rolls[k][j], rolls[k][mid][:, -1].copy())
    
    return rolls

def derajat0(gray, type):
    result = np.zeros(gray.shape, dtype=np.float)
    
    if type == 'average':
        kernel = [
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1],
        ]
        result[:] = convolve(gray, kernel)
        result /= 9
    
    elif type == 'homogen':
        rolls = create_rolls(gray, [
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1],
        ])
        subs = []
        for row in rolls:
            for roll in row:
                subs.append(np.abs(roll-gray))
        for sub in subs:
            result[:] = np.maximum(result, sub)
        result[:] = normalize(result)
    
    elif type == 'difference':
        rolls = create_rolls(gray, [
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1],
        ])
        subs = [
            np.abs(rolls[0][0]-rolls[2][2]),
            np.abs(rolls[0][1]-rolls[2][1]),
            np.abs(rolls[0][2]-rolls[2][0]),
            np.abs(rolls[1][0]-rolls[1][2]),
        ]
        for sub in subs:
            result[:] = np.maximum(result, sub)
        result[:] = normalize(result)
    
    return result.round().astype(np.uint8)

def derajat1(gray, type):
    result = np.zeros(gray.shape, dtype=np.float)
    
    if type == 'sobel':
        kernel1 = [
            [-1, 0, 1],
            [-2, 0, 2],
            [-1, 0, 1],
        ]
        kernel2 = [
            [1, 2, 1],
            [0, 0, 0],
            [-1, -2, -1],
        ]
    elif type == 'prewitt':
        kernel1 = [
            [-1, -1, -1],
            [0, 0, 0],
            [1, 1, 1],
        ]
        kernel2 = [
            [-1, 0, 1],
            [-1, 0, 1],
            [-1, 0, 1],
        ]
    
    result[:] = convolve(gray, kernel1)
    result += convolve(gray, kernel2)
    result[:] = np.abs(result)
    result[:] = normalize(result)
    
    return result.round().astype(np.uint8)

def derajat2(gray, type):
    result = np.zeros(gray.shape, dtype=np.float)
    
    if type == 'kirsch':
        kernel = [
            [5, 5, 5],
            [-3, 0, -3],
            [-3, -3, -3],
        ]
    
    elif type == 'prewitt':
        kernel = [
            [-1, 0, 1],
            [-1, 0, 1],
            [-1, 0, 1],
        ]
    
    results = []
    for i in range(0, 8):
        results.append(convolve(gray, kernel))
        kernel[:] = nph.rot45(np.array(kernel))
    
    for i in range(0, 8):
        result[:] = np.maximum(result, results[i])
    
    result[:] = normalize(result)
    return result.round().astype(np.uint8)

def sobel(gray):
    operator_baris = [[1, 2, 1],
                      [0, 0, 0],
                      [-1, -2, -1]]
    operator_kolom = [[1, 0, -1],
                      [2, 0, -2],
                      [1, 0, -1]]
    
    result = operate(gray, operator_baris, operator_kolom)
    return normalize(result).round().astype(np.uint8)

def gaussian(img):
    # kernel = [1, 3, 5, 3, 1]
    kernel = [1, 4, 7, 9, 7, 4, 1]
    
    kernel_count = len(kernel)
    kernel_half = (kernel_count-1)/2
    rolls = range(0, len(kernel))
    result = np.zeros(img.shape, dtype=np.float)
    
    rolls[kernel_half] = img.astype(np.float)
    for i in range(1, kernel_half+1):
        rolls[kernel_half+i] = nph.roll_left(rolls[kernel_half+i-1], img[:,-1].copy())
        rolls[kernel_half-i] = nph.roll_right(rolls[kernel_half-i+1], img[:,0].copy())
    for i in range(0, kernel_count):
        result += rolls[i] * kernel[i]
    result /= sum(kernel)
    
    rolls[kernel_half] = result.copy()
    result = 0
    for i in range(1, kernel_half+1):
        rolls[kernel_half+i] = nph.roll_up(rolls[kernel_half+i-1], img[-1].copy())
        rolls[kernel_half-i] = nph.roll_down(rolls[kernel_half-i+1], img[0].copy())
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
    result = (0. + matrix - min) * 255 / (max - min)
    return result

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
    
    return normalize(result).round().astype(np.uint8)

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
    
    # img = gambar.read('D:\\Kuliah\\pola\\527C868C9284958A22F9E4D448BDDA12.JPG')
    img = gambar.read('C:\\Users\\user all\\Downloads\\532fd38d-1.jpg')
    gray = gambar.to_gray(img)
    # gambar.show(gray)
    result = derajat1(gray, 'prewitt')
    gambar.show(result)
    
    # kernel = [
        # [1, 2, 1],
        # [2, 4, 2],
        # [1, 2, 1],
    # ]
    # gray = np.array(kernel)
    # convolve(gray, kernel)