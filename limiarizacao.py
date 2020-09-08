import numpy as np
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
        # print(i, t-t0)
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

def plot_variances(f, limiar):
    plt.plot(f)
    plt.axvline(x=limiar, color='red', linestyle='--')
    plt.show()

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
    # plot_variances(variances, t)

    return segment(img, t, r1, r2, politica)