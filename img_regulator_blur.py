import os
from PIL import Image
import cv2
import numpy as np
import pyFspecial
import sys
image_size = (224, 224)

yourpath = os.getcwd()

def _cls():
    os.system("cls" if os.name == "nt" else "clear")
def Imsize_Changer(prev=1):
    global filesc
    filesc= prev
    for root, dirs, files in os.walk(os.getcwd(), topdown=False):
        for name in files:
            try:
                im = Image.open(os.path.join(root, name))
                print(im.size == image_size)
                if im.size == image_size:
                    if prev == len(files):
                        _cls()
                        print("All Done!!")
                        return
                    prev += 1
                if im.size[0] / im.size[1] == 1:
                    print("Image is Square::" , os.path.join(root, name))
                    im.thumbnail(image_size)
                    im.save(os.path.join(root, name), "JPEG", quality=100)
                else:
                    print(f'Not Square ... Converting... {name:}')
                    img = cv2.imread(os.path.join(root, name))
                    h, w, c = img.shape
                    if h > w:
                        y = (h-w)//2
                        crop_img = img[y:y+w, 0:w]
                        cv2.imwrite(os.path.join(root, name), crop_img)
                        print('Img Size changed')
                    else:
                        x = (w-h)//2
                        crop_img = img[0:h, x:x+h]
                        cv2.imwrite(os.path.join(root, name), crop_img)
                        print('Img Size changed')
                filesc +=1
            except Exception as rex:
                print(rex)
                pass
            _cls()

    else:
        Imsize_Changer(filesc) #To Change Image if all ratio chaged




def img2jpg_converter():
    for root, dirs, files in os.walk(yourpath, topdown=False):
        for name in files:
            #print(os.path.join(root, name))
            if os.path.splitext(os.path.join(root, name))[1].lower() == ".tiff":
                if os.path.isfile(os.path.splitext(os.path.join(root, name))[0] + ".jpg"):
                    print("A jpeg file already exists for %s" % name)
                    try:
                        os.remove(os.path.splitext(os.path.join(root, name))[0] + ".tiff")
                    except:
                        pass
                else:
                    outfile = os.path.splitext(os.path.join(root, name))[0] + ".jpg"
                    try:
                        im = Image.open(os.path.join(root, name))
                        print("Generating jpeg for %s" % name)
                        im.thumbnail(im.size)
                        im.save(outfile, "JPEG", quality=100)
                        os.remove(os.path.join(root, name))
                    except Exception as e:
                        print(e)
            elif os.path.splitext(os.path.join(root, name))[1].lower() == ".png":
                if os.path.isfile(os.path.splitext(os.path.join(root, name))[0] + ".jpg"):
                    print("jpG File already exist")
                    try:
                        os.remove(os.path.splitext(os.path.join(root, name))[0] + ".png")
                    except:
                        pass
                else:
                    outfile = os.path.splitext(os.path.join(root, name))[0] + ".jpg"
                    try:
                        im = Image.open(os.path.join(root, name))
                        print("Genrating png for %s" % name)
                        im.thumbnail(im.size)
                        im.save(outfile, "JPEG", quality=100)
                        os.remove(os.path.join(root, name))
                    except Exception as e:
                        print(e)

def blur_augmentation():
    count1 = 0
    for root, dirs, files in os.walk(yourpath, topdown=False):

        for name in files:
            try:

                for i in range(0, 360, 45):
                    #_cls()
                    im = cv2.imread(os.path.join(root, name))
                    im = pyFspecial.filterImage(im,'motion', '[21, 21]', 20, i, 1 )
                    outname = os.path.splitext(os.path.join(root, name))[0] + "_" + str(i) + ".jpg"
                    cv2.imwrite(outname,  im)
                    print('Motion Blurring Inetensity={0}, Angle={1}'.format(20, i))
                    print('Now...', name)
                    count1 +=1
            except Exception as rex:
                print("Image load error")
        else:
            print('All Done! {} images are blurred'.format(count1))



if __name__ == '__main__':
    try:
        var1 = sys.argv[1]
        if var1 == 'converter':
            img2jpg_converter()
        elif var1 == 'changer':
            Imsize_Changer()
        elif var1 == 'blur':
            blur_augmentation()
    except:
        print("wrong args ::", var1)
        pass
