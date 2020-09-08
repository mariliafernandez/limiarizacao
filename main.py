import numpy as np
import cv2 as cv
import argparse
import sys
import matplotlib.pyplot as plt

def segment(img, t, r1, r2, opt):
    img_seg = img.copy()
    
    if opt == 'bin':
        img_seg[r1] = 0
        img_seg[r2] = 255
    elif opt == 'trunc':
        img_seg[r2] = t
    elif opt == 'zero':
        img_seg[r1] = 0
    return img_seg

def ridler_calvard(img, politica):
    t0 = np.mean(img)
    t = t0
    
    for i in range(100):
        r1 = img < t
        r2 = img > t
        u1 = np.mean(img[r1])
        u2 = np.mean(img[r2])
        t0 = t
        t = (u1+u2)/2
        print(i, t-t0)
        if abs(t-t0) < 0.001 : break
    return segment(img, t, r1, r2, politica)

def histograma(img):
    hist = np.zeros(256)
    for i in range(256):
        hist[i] = np.sum(img == i)
    return hist
        
def var_intraclasse(hist, L):
    med1 = np.zeros(L)
    arr1 = np.array(range(L))
    h1 = hist[:L]
    soma1 = sum(h1)
    if soma1 != 0:
        avg1 = sum(arr1 * h1) / soma1
        var1 = sum( pow(arr1 - avg1, 2) * h1) / soma1
    else: 
        var1 = 0
    w1 = np.mean(h1) * var1
    
    med2 = np.zeros(256-L)
    arr2 = np.array(range(L, 256))
    h2 = hist[L:]
    soma2 = np.sum(h2)
    if soma2 != 0:
        avg2 = sum(arr2 * h2) / soma2
        var2 = sum( pow(arr2 - avg2, 2) * h2) / soma2
    else:
        var2 = 0
    w2 = np.mean(h2) * var2
    
    return w1*var1 + w2*var2

def otsu(img, politica):
    variances = []
    hist = histograma(img)
    min_ = np.min(img)
    max_ = np.max(img)
    
    for i in range( min_, max_+1):
        var = var_intraclasse(hist, i)
        variances.append( var )
        
    t = variances.index(min(variances))
    r1 = img < t
    r2 = img > t
    
    f = plt.figure()
    plt.plot(variances)
    plt.axvline(x=t, color='red', linestyle='--')
    plt.show()
    return segment(img, t, r1, r2, politica)

# Interpreta os argumentos passados via terminal
parser = argparse.ArgumentParser()
parser.add_argument('-b', help='política de limiarização [bin, trunc, zero]')
parser.add_argument('-t', help='algoritmo de limiarização [rc, otsu]')
parser.add_argument('-i', help='imagem de entrada em formato png')

args = parser.parse_args()
politica = args.b
algoritmo = args.t
image = args.i

# Abre a imagem em escala de cinza
img_file = cv.imread(image)
if img_file is None : 
    print('Não foi possível ler a imagem.')
    sys.exit(0)
else: 
    # Converte as cores originais da imagem para tons de cinza e salva a nova imagem em arquivo
    gray = cv.cvtColor(img_file, cv.COLOR_BGR2GRAY)
    
if algoritmo == 'ridler_calvard':
    segmented = ridler_calvard(gray, politica)
    cv.imwrite('output-rc-'+politica+'.png', segmented)
    cv.imshow('output', segmented/255)
    cv.waitKey(0)
    
elif algoritmo == 'otsu':
    segmented = otsu(gray, politica)
    cv.imwrite('output-otsu-' + politica+'.png', segmented)
    cv.imshow('output', segmented/255)
    cv.waitKey(0)