import numpy as np

import gambar
from point import Point
from rect import Rect

def get_masker(rgb):
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    
    masker = (r > g) * (r > b) # face is redder
    masker *= g >= b if g[masker].sum() > b[masker].sum() else b >= g
    
    hist = gambar.get_histogram(r)
    threshold = gambar.otsu(hist, r.shape[0]*r.shape[1])
    tmax = max(threshold, r[masker].mean())
    masker *= r >= tmax/2.0
    
    return masker

def get_wajahs(masker):
    wajahs = []
    for y in range(0, masker.shape[0]):
        for x in range(0, masker.shape[1]):
            if masker[y, x]:
                wajah = flood_fill(masker, Point(y=y, x=x))
                wajahs.append(wajah)
    
    # cleaning
    i = 0
    while i < len(wajahs):
        wajah = wajahs[i]
        
        pop = False
        if wajah.d.y-wajah.a.y < 5 or wajah.d.x-wajah.a.x < 5: # minimum wajah size is 5x5
            pop = True
        if wajah.d.y-wajah.a.y < wajah.d.x-wajah.a.x: # must be tall
            pop = True
        
        for compar in wajahs:
            if not (compar.a.x == wajah.a.x and compar.d.x == wajah.d.x and
                    compar.a.y == wajah.a.y and compar.d.y == wajah.d.y):
                if (compar.a.x <= wajah.a.x and wajah.d.x <= compar.d.x and
                    compar.a.y <= wajah.a.y and wajah.d.y <= compar.d.y):
                    pop = True
                    break
        
        if pop:
            wajahs.pop(i)
        else:
            i += 1
    
    return wajahs

def flood_fill(masker, p):
    rect = Rect()
    rect.a.x = p.x
    rect.a.y = p.y
    rect.d.x = p.x
    rect.d.y = p.y
    
    queue = [p]
    while len(queue) > 0:
        dequeue = queue.pop(0)
        if masker[dequeue.y, dequeue.x]:
            masker[dequeue.y, dequeue.x] = False
        
            # get [x|y] [min|max] 
            if dequeue.x < rect.a.x:
                rect.a.x = dequeue.x
            if dequeue.y < rect.a.y:
                rect.a.y = dequeue.y
            if dequeue.x > rect.d.x:
                rect.d.x = dequeue.x
            if dequeue.y > rect.d.y:
                rect.d.y = dequeue.y
            
            for next in [Point(y=dequeue.y-1, x=dequeue.x),
                         Point(y=dequeue.y, x=dequeue.x+1),
                         Point(y=dequeue.y+1, x=dequeue.x),
                         Point(y=dequeue.y, x=dequeue.x-1)]:
                if (next.y < masker.shape[0] and next.x < masker.shape[1] # inside image
                    and masker[next.y, next.x]): # is face
                    queue.append(next)
    
    return rect

def draw_masker(img, masker):
    imgr = img.copy()
    r, g, b = imgr[:, :, 0], imgr[:, :, 1], imgr[:, :, 2]
    r[masker] = 255
    g[masker] = 255
    b[masker] = 255
    return imgr

def draw_kotak(img, wajahs):
    imgr = img.copy()
    for wajah in wajahs:
        # paint x
        imgr[wajah.a.y:wajah.a.y+2, wajah.a.x:wajah.d.x+1] = [255, 0, 0]
        imgr[wajah.d.y-1:wajah.d.y+1, wajah.a.x:wajah.d.x+1] = [255, 0, 0]
        # paint y
        imgr[wajah.a.y:wajah.d.y+1, wajah.a.x:wajah.a.x+2] = [255, 0, 0]
        imgr[wajah.a.y:wajah.d.y+1, wajah.d.x-1:wajah.d.x+1] = [255, 0, 0]
    return imgr

if __name__ == '__main__':
    # rgb = gambar.read('..\\Foto_Kelas_20151116\\kecil\\DSC02275.jpg')
    rgb = gambar.read('..\\..\\Foto_Kelas_20151116\\kecil\\DSC02277.jpg')
    # rgb = gambar.read('..\\Foto_Kelas_20151116\\kecil\\DSC02274.jpg')
    
    masker = get_masker(rgb)
    
    maskered = draw_masker(rgb, masker)
    gambar.show(maskered)
    
    wajahs = get_wajahs(masker)
    kotaked = draw_kotak(rgb, wajahs)
    gambar.show(kotaked)
    
    # r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    
    # masker = get_masker(rgb)
    # # r[masker] = 255
    # # g[masker] = 255
    # # b[masker] = 255
    # # gambar.show(rgb)
    
    # wajahs = get_wajahs(masker)
    
    # for wajah in wajahs:
        # # paint x
        # rgb[wajah.a.y:wajah.a.y+2, wajah.a.x:wajah.d.x+1] = [255, 0, 0]
        # rgb[wajah.d.y-1:wajah.d.y+1, wajah.a.x:wajah.d.x+1] = [255, 0, 0]
        # # paint y
        # rgb[wajah.a.y:wajah.d.y+1, wajah.a.x:wajah.a.x+2] = [255, 0, 0]
        # rgb[wajah.a.y:wajah.d.y+1, wajah.d.x-1:wajah.d.x+1] = [255, 0, 0]
    
    # gambar.show(rgb)