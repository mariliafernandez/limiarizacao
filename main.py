
import cv2 as cv
import argparse
import sys
from limiarizacao import *

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
    sys.exit(1)
else: 
    # Converte as cores originais da imagem para tons de cinza e salva a nova imagem em arquivo
    gray = cv.cvtColor(img_file, cv.COLOR_BGR2GRAY)
    
if algoritmo == 'rc':
    segmented = ridler_calvard(gray, politica)
    cv.imwrite('output-rc-'+politica+'.png', segmented)
    cv.imshow('output', segmented/255)
    cv.waitKey(0)
    
elif algoritmo == 'otsu':
    segmented = otsu(gray, politica)
    cv.imwrite('output-otsu-' + politica+'.png', segmented)
    cv.imshow('output', segmented/255)
    cv.waitKey(0)
    
else:
    print('Opção inválida.')
    sys.exit(1)