# Matlab fspecial function port python
# 2019.05.02 14:24
import numpy as np
import math
from scipy.misc import imrotate
import scipy
import sys
from scipy.ndimage import convolve
from skimage.measure import compare_ssim as ssim
import cv2


def fspecial(_, filtertype, sze=[3, 3], len = 9, angle = 0, sigma=0.5):
    sze = eval(str(sze))
    len = int(len)
    angle = int(angle)
    sigma = float(sigma)
    if filtertype == 'motion': #By etal. Peter 2005 m file
        f = np.zeros(sze)
        f[math.floor(len/2)-1][:len] = 1

        f = imrotate(f,  angle, interp='bilinear')
        f = np.divide(f, f.sum())
        return f
    elif filtertype == 'gaussian':
        m,n = [(ss-1.)/2. for ss in sze]
        y,x = np.ogrid[-m:m+1,-n:n+1]
        h = np.exp( -(x*x + y*y) / (2.*sigma*sigma) )
        h[ h < np.finfo(h.dtype).eps*h.max() ] = 0
        sumh = h.sum()
        if sumh != 0:
            h /= sumh
        return h
import time
def filterImage(im, type, sze, len, angle, sigma):
    h = fspecial(0,type, sze, len, angle, sigma )
    try:
        im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    except:
        pass
    out = convolve(im, h)
    return out

def img_qualityCheck():
    sobelX = [[-1, 0, 1], [-2, 0, 2],[-1,0,1]]
    img = cv2.imread('pic.jpg')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    f = fspecial(0, 'motion', [20, 20], 20 ,45 ,1)
    k2 = convolve(img, f)
    k = convolve(k2, sobelX)
    k3 = convolve(img, sobelX)

    cv2.imshow('test2', np.hstack([k2, k, k3]))
    cv2.waitKey(0)


if __name__ == '__main__':
    print(*sys.argv[2:])
    h = fspecial(0, 'motion', *sys.argv[2:])
    g = fspecial(0, 'gaussian', *sys.argv[2:])
    print(h, g, sep='\n')

    img2 = cv2.imread('pic2.tiff')
    img = cv2.imread('pic.jpg')
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    h1 = convolve(img, h, mode='nearest')
    g1 = convolve(img, g, mode='nearest')
    h2 = convolve(img2, h, mode='nearest')
    g2 = convolve(img2, g, mode='nearest')

    hssim_const = ssim(h1, img, data_range=img.max() - img.min())
    gssim_const = ssim(g1, img, data_range=img.max() - img.min())
    issim_const = ssim(img, img, data_range=img.max() - img.min())

    print(issim_const, hssim_const, gssim_const, sep=' | ')

    cv2.imshow('test', np.hstack([img, h1, g1]))

    cv2.waitKey(10000)
    cv2.destroyAllWindows()

    img_qualityCheck()
