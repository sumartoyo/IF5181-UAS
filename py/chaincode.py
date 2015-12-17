import sys

import gambar

# chaincode:
# 5 6 7
# 4   0
# 3 2 1

# kodebelok:
# kan +
# kir -

def get_chaincode(kopong):
    codes = []
    for y in range(0, kopong.shape[0]):
        for x in range(0, kopong.shape[1]):
            if kopong[y, x]:
                code = iterate_chaincode(kopong, y, x)
                if len(code) > 0:
                    codes.append(code)
    return codes

def iterate_chaincode(kopong, y, x):
    result = []
    stop = False
    while not stop:
        stop = True
        kopong[y, x] = False
        for dir in range(0, 8):
            y_next, x_next = move(kopong, y, x, dir)
            if y_next is not None and kopong[y_next, x_next]:
                stop = False
                result.append(dir)
                y, x = y_next, x_next
                break
    return result

def move(kopong, y, x, dir):
    y += 1 if 1 <= dir <= 3 else 0
    y -= 1 if 5 <= dir <= 7 else 0
    
    x -= 1 if 3 <= dir <= 5 else 0
    x += 1 if 0 <= dir <= 1 or dir == 7 else 0
    
    if y >= 0 and y < kopong.shape[0] and x >= 0 and x < kopong.shape[1]:
        return (y, x)
    else:
        return (None, None)

def get_kodebelok(codes):
    beloks = []
    for code in codes:
        belok = []
        dir_last = None
        for dir in code:
            if dir_last is not None:
                arah = get_arah(dir_last, dir)
                if arah is not None:
                    belok.append(arah)
            dir_last = dir
        beloks.append(belok)
    return beloks

def get_arah(dir_last, dir):
    if dir_last >= 5:
        dir = 8 if dir == 0 else dir
    if dir_last >= 6:
        dir = 9 if dir == 1 else dir
    if dir_last >= 7:
        dir = 10 if dir == 2 else dir
    
    if dir_last <= 2:
        dir = -1 if dir == 7 else dir
    if dir_last <= 1:
        dir = -2 if dir == 6 else dir
    if dir_last <= 0:
        dir = -3 if dir == 5 else dir
    
    if dir > dir_last:
        return '+'
    elif dir < dir_last:
        return '-'
    else:
        return None

if __name__ == ('__main__'):
    img = gambar.read(sys.argv[1])
    gray = gambar.to_gray(img)
    bw = gambar.to_bw(gray)
    kopong = gambar.koponging(bw)
    
    chaincode = get_chaincode(kopong)
    kodebelok = get_kodebelok(chaincode)