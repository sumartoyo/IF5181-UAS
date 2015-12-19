import sys
import json
import numpy as np

import gambar
import chaincode
import zhangsuen

def main(path):
    img = gambar.read(path)
    gray = gambar.to_gray(img)
    bw = gambar.to_bw(gray)
    tulang = zhangsuen.penulangan(bw)
    
    with open('ocr_train.json') as infile:
        train = json.load(infile)
    
    results = []
    objects = get_objects(bw)
    for object in objects:
        feature = get_feature(tulang[object[0]-1:object[1]+2, object[2]-1:object[3]+2])
        results.append(classify(train, feature))
    return ''.join(results)

def get_objects(bw):
    objects = []
    yf, yl, xf, xl = -1, -1, -1, -1
    
    any_row = bw.any(1)
    for y in range(0, any_row.shape[0]):
        if any_row[y]:
            yf = y if yf == -1 else yf
            yl = y if yf > -1 else yl
        else:
            if yf > -1:
                any_col = bw[yf:yl+1, 0:bw.shape[1]].any(0)
                for x in range(0, any_col.shape[0]):
                    if any_col[x]:
                        xf = x if xf == -1 else xf
                        xl = x if xf > -1 else xl
                    else:
                        if xf > -1:
                            objects.append((yf, yl, xf, xl))
                            xf, xl = -1, -1
                yf, yl = -1, -1
    
    return objects

def get_feature(bw):
    feature = np.zeros((4, 8)) # 1st axis is kuadran, 2nd axis is code of chain code
    
    pixels = chaincode.get_pixels(bw)
    center = chaincode.get_center(pixels)
    for i in range(0, pixels.shape[1]): # for every pixel
        if pixels[0, i] >= center[0]:
            kuadran = 0 if pixels[1, i] >= center[1] else 1
        else:
            kuadran = 2 if pixels[1, i] < center[1] else 3
        
        for dir in range(0, 8): # for every direction
            ynei, xnei = chaincode.move(bw, pixels[1, i], pixels[0, i], dir) # neighbor pixel
            if ynei is not None and bw[ynei, xnei]: # if neighbor is black
                feature[kuadran, dir] += 1
    
    return feature * (100.0 / pixels.shape[1])

def get_features(bw):
    features = []
    objects = get_objects(bw)
    tulang = zhangsuen.penulangan(bw)
    for object in objects:
        feature = get_feature(tulang[object[0]-1:object[1]+2, object[2]-1:object[3]+2])
        features.append(feature)
    return features

def classify(train, feattest):
    data = np.array(train['features']) # array of character (array of kuadran (array of chaincode))
    tests = feattest.reshape((1,) + feattest.shape).repeat(data.shape[0], axis=0) # reshape-repeat to data shape
    min = ((tests - data) ** 2).sum(-1).sum(-1).argmin() # index of minimum square error
    return train['labels'][min]

if __name__ == ('__main__'):
    main(sys.argv[1])