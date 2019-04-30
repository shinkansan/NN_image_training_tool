import os
from PIL import Image

yourpath = os.getcwd()
for root, dirs, files in os.walk(yourpath, topdown=False):
    for name in files:
        print(os.path.join(root, name))
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
