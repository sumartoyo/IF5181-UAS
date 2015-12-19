import sys
import shutil
import json
import os
import time

import gambar
import konvolusi
import chaincode
import zhangsuen
import ocr

def main():
    method = sys.argv[1]
    input = sys.argv[2]
    id = sys.argv[3]
    home = os.path.expanduser('~')+'\\.IF5181\\'
    dir = home+id+'\\'

    if not os.path.isdir(dir):
        if os.path.isdir(home):
            shutil.rmtree(home, ignore_errors=True)
        if not os.path.isdir(home):
            os.mkdir(home)
        os.mkdir(dir)

    os.chdir('py')
    
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
        gambar.save(gray, dir+'gray.jpg')
        
        bw = gambar.to_bw(gray)
        gambar.save(bw, dir+'binary.jpg')
    
    elif method == 'derajat0':
        img = gambar.read(input)
        
        gray = gambar.to_gray(img)
        gambar.save(gray, dir+'gray.jpg')
        
        average = konvolusi.derajat0(gray, 'average')
        gambar.save(average, dir+'derajat0-average.jpg')
        
        homogen = konvolusi.derajat0(gray, 'homogen')
        gambar.save(homogen, dir+'derajat0-homogen.jpg')
        
        difference = konvolusi.derajat0(gray, 'difference')
        gambar.save(difference, dir+'derajat0-difference.jpg')
    
    elif method == 'derajat1':
        img = gambar.read(input)
        
        gray = gambar.to_gray(img)
        gambar.save(gray, dir+'gray.jpg')
        
        sobel = konvolusi.derajat1(gray, 'sobel')
        gambar.save(sobel, dir+'derajat1-sobel.jpg')
        
        prewitt = konvolusi.derajat1(gray, 'prewitt')
        gambar.save(prewitt, dir+'derajat1-prewitt.jpg')
    
    elif method == 'derajat2':
        img = gambar.read(input)
        
        gray = gambar.to_gray(img)
        gambar.save(gray, dir+'gray.jpg')
        
        kirsch = konvolusi.derajat2(gray, 'kirsch')
        gambar.save(kirsch, dir+'derajat2-kirsch.jpg')
        
        prewitt = konvolusi.derajat2(gray, 'prewitt')
        gambar.save(prewitt, dir+'derajat2-prewitt.jpg')
    
    elif method == 'gauss':
        img = gambar.read(input)
        gambar.save(konvolusi.gaussian(img), dir+'gauss.jpg')
    
    elif method == 'chaincode':
        img = gambar.read(input)
        gray = gambar.to_gray(img)
        bw = gambar.to_bw(gray)
        gambar.save(bw, dir+'binary.jpg')
        
        kopong = gambar.koponging(bw)
        gambar.save(kopong, dir+'kopong.jpg')
        
        code = chaincode.get_chaincode(kopong)
        belok = chaincode.get_kodebelok(code)
        json_save(code, dir+'chaincode.json')
        json_save(belok, dir+'kodebelok.json')
    
    elif method == 'skeleton':
        img = gambar.read(input)
        gray = gambar.to_gray(img)
        bw = gambar.to_bw(gray)
        gambar.save(bw, dir+'binary.jpg')
        
        tulang = zhangsuen.penulangan(bw)
        gambar.save(tulang, dir+'tulang.jpg')
        
        ujung, simpangan = zhangsuen.get_identity(tulang)
        json_save({
            'ujung': [[int(y), int(x)] for y, x in ujung],
            'simpangan': [[int(y), int(x)] for y, x in simpangan],
        }, dir+'tulang-identity.json')
        
        code = zhangsuen.get_chaincode(tulang)
        belok = chaincode.get_kodebelok(code)
        json_save(code, dir+'tulang-chaincode.json')
        json_save(belok, dir+'tulang-kodebelok.json')
    
    elif method == 'ocr':
        result = ocr.main(input)
        json_save({
            'result': result
        }, dir+'ocr-result.json')

def json_save(obj, path):
    f = open(path, 'w')
    json.dump(obj, f)
    f.close()

if __name__ == ('__main__'):
    main()