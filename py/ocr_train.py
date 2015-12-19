from os import listdir
from os.path import isfile, join, splitext
import json

import gambar
import ocr

def main():
    features = []
    for type in ['number', 'upper', 'lower']:
        bw = gambar.to_bw(gambar.to_gray(gambar.read('ocr_train_{}.PNG'.format(type))))
        features.extend([array.tolist() for array in ocr.get_features(bw)])
    
    labels = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
             'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
             'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    
    with open('ocr_train.json', 'w') as outfile:
        json.dump({'features': features, 'labels': labels}, outfile)

if __name__ == ('__main__'):
    main()