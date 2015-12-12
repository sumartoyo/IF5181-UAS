import sys
import shutil
import json
import os
import time

import gambar

def main():
    method = sys.argv[1]
    input = sys.argv[2]
    id = sys.argv[3]
    home = os.path.expanduser('~')+'\\.IF5181-dimas\\'
    dir = home+id+'\\'

    if not os.path.isdir(dir):
        if os.path.isdir(home):
            shutil.rmtree(home, ignore_errors=True)
        if not os.path.isdir(home):
            os.mkdir(home)
        os.mkdir(dir)

    if method == 'histogram':
        img = gambar.read(input)
        hist = gambar.get_histogram(img)
        json_save({
            'r': list(gambar.get_histogram(img[:, :, 0])),
            'g': list(gambar.get_histogram(img[:, :, 1])),
            'b': list(gambar.get_histogram(img[:, :, 2])),
        }, dir+'histogram.json')

    elif method == 'equalize':
        img = gambar.read(input)
        gray = gambar.to_gray(img)
        hist_gray = gambar.get_histogram(gray)
        result, hist_result = gambar.equalize(gray, hist_gray)
        
        gambar.save(gray, dir+'gray.jpg')
        json_save(list(hist_gray), dir+'histogram_gray.json')
        
        gambar.save(result, dir+'equalized.jpg')
        json_save(list(hist_result), dir+'histogram_equalized.json')
    
    elif method == 'otsu':
        img = gambar.read(input)
        gray = gambar.to_gray(img)
        hist = gambar.get_histogram(gray)
        threshold = gambar.otsu(hist, gray.shape[0]*gray.shape[1])
        gambar.save(gray, dir+'gray.jpg')
        gambar.save(gray <= threshold, dir+'binary.jpg')

def json_save(obj, path):
    f = open(path, 'w')
    json.dump(obj, f)
    f.close()

if __name__ == ('__main__'):
    main()