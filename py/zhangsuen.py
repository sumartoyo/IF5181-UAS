import sys
import numpy as np
import json

import nph
import gambar
import chaincode

def to_tulang(bw, step):
    # http://rosettacode.org/wiki/Zhang-Suen_thinning_algorithm
    # `bw` is already white bordered
    # `step` is 1 or 2 and affects on determining px
    
    the_pixel_is_black = bw # just for the sake of semantics
    
    # Black pixels P1 can have eight neighbours.
    # The neighbours are, in order, arranged as:
    # P9 P2 P3
    # P8 P1 P4
    # P7 P6 P5
    p2, p3, p4, p5, p6, p7, p8, p9 = get_p(bw)
    
    # B(P1) = The number of black pixel neighbours of P1
    b = p2 + p3 + p4 + p5 + p6 + p7 + p8 + p9
    has_between_2_and_6_neighbors = (2 <= b) * (b <= 6)
    
    # A(P1) = the number of transitions from white to black, (0 -> 1) in the sequence P2,P3,P4,P5,P6,P7,P8,P9,P2
    a = (get_is01trans(p2, p3) + get_is01trans(p3, p4) +
         get_is01trans(p4, p5) + get_is01trans(p5, p6) +
         get_is01trans(p6, p7) + get_is01trans(p7, p8) +
         get_is01trans(p8, p9) + get_is01trans(p9, p2))
    has_one_0_to_1_transition = a == 1
    
    has_white_in_p2_p4_px = (p2 * p4 * (p6 if step == 1 else p8)) == False
    has_white_in_px_p6_p8 = ((p4 if step == 1 else p2) * p6 * p8) == False
    
    return bw - (the_pixel_is_black *
                 has_between_2_and_6_neighbors *
                 has_one_0_to_1_transition *
                 has_white_in_p2_p4_px *
                 has_white_in_px_p6_p8)

def get_is01trans(a, b):
    return ((a == False) * b).astype(np.uint8)

def get_p(bw, dtype=np.uint8):
    p1 = bw.astype(dtype)
    p2 = np.roll(p1, 1, 0)
    p3 = np.roll(p2, -1, 1)
    p4 = np.roll(p1, -1, 1)
    p5 = np.roll(p4, -1, 0)
    p6 = np.roll(p1, -1, 0)
    p7 = np.roll(p6, 1, 1)
    p8 = np.roll(p1, 1, 1)
    p9 = np.roll(p8, 1, 0)
    return (p2, p3, p4, p5, p6, p7, p8, p9)

def penulangan(bw):
    # remove non Zhang Suen's tulang
    bwr = np.copy(bw)
    cblack_l = 0
    cblack_c = bwr.nonzero()[0].shape[0]
    while cblack_l != cblack_c:
        cblack_l = bwr.nonzero()[0].shape[0]
        bwr[:] = to_tulang(bwr, 1)
        bwr[:] = to_tulang(bwr, 2)
        cblack_c = bwr.nonzero()[0].shape[0]
    bwr[:] = gambar.koponging(bwr)
    return bwr

def get_identity(tulang):
    rollup, rolldown, rollleft, rollright = nph.roll_all(tulang)
    rollupleft = nph.roll_left(rollup)
    rollupright = nph.roll_right(rollup)
    rolldownleft = nph.roll_left(rolldown)
    rolldownright = nph.roll_right(rolldown)
    
    neighbors = tulang.astype(np.uint8)*(0+rollup+rolldown+rollleft+rollright+rollupleft+rollupright+rolldownleft+rolldownright)
    ujung_nonzero = (neighbors == 1).nonzero()
    simpangan_nonzero = (neighbors > 2).nonzero()
    
    ujung = []
    for i in range(0, ujung_nonzero[0].shape[0]):
        ujung.append((ujung_nonzero[0][i], ujung_nonzero[1][i]))
    
    simpangan = []
    for i in range(0, simpangan_nonzero[0].shape[0]):
        simpangan.append((simpangan_nonzero[0][i], simpangan_nonzero[1][i]))
    
    # remove redundant simpangan
    i = 0
    while i < len(simpangan):
        yi, xi = simpangan[i]
        j = i+1
        while j < len(simpangan):
            yj, xj = simpangan[j]
            if yi-1 <= yj <= yj+1 and xi-1 <= xj <= xi+1:
                simpangan.pop(j)
                j -= 1
            j += 1
        i += 1
    
    return (ujung, simpangan)

def get_chaincode(tulang):
    tulangr = tulang.copy()
    codes = []
    
    ujung, simpangan = get_identity(tulangr)
    while len(ujung) > 0:
        y, x = ujung[0]
        if tulangr[y, x]:
            code = chaincode.iterate_chaincode(tulangr, y, x)
            if len(code) > 0:
                codes.append(code)
        ujung, simpangan = get_identity(tulangr)
    
    codes.extend(chaincode.get_chaincode(tulangr))
    
    return codes

if __name__ == ('__main__'):
    img = gambar.read(sys.argv[1])
    gray = gambar.to_gray(img)
    bw = gambar.to_bw(gray)
    
    tulang = penulangan(bw)
    ujung, simpangan = get_identity(tulang)
    json_data = {
        'ujung': [list((int(y), int(x))) for y, x in ujung],
        'simpangan': [list((int(y), int(x))) for y, x in simpangan],
    }
    print json.dumps(json_data)
    # code = get_chaincode(tulang)
    # belok = chaincode.get_kodebelok(code)
    # print belok