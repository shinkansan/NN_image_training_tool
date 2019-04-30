# 이미지 정규화 하는 코드
# 그레이스케일, 리사이징, 정규화 (/255.0) 하고 npy에 stack
# 사진들이 분류 되어있는 폴더의 상위 디렉토리에 넣고 돌리기...

# script for preparing datasets, loading fer data and generating scaled images
import numpy as np
import cv2
from PIL import Image
import sys
import os

emotions = {0:'anger', 1:'disgust', 2:'fear',3:'happiness',4:'sadness',5:'surprise',6:'neutral'}
global outfile, data, data0, label, label0, desired_size

def _cls():
    os.system("cls" if os.name == "nt" else "clear")
def run(data, label, desired_size):
    data0 = data[:]
    label0 = label[:]
    for root, dirs, files in os.walk(os.getcwd(), topdown=False):

        for name in files:
            try:


                filename = os.path.join(root, name)
                im = Image.open(filename)
                cvim = cv2.imread(filename)
                grayCv = cv2.cvtColor(cvim, cv2.COLOR_BGR2GRAY)
                grayCv = cv2.resize(grayCv, desired_size)
                pdata = np.array(grayCv.reshape(-1)).astype('float64')
                pdata = [np.divide(d, 255.0) for d in pdata]
                data = np.concatenate((data, [pdata]))
                emotios_k = list(emotions.keys())
                for key in emotios_k:
                    if emotions[key] in filename:
                        label = np.concatenate((label, [key]))
                        _cls()
                        print(f'add img2pix {name}:{emotions[key]}')

            except Exception as rex:
                print('Image OpenError!', rex)
    print(f"All done! \n{data.shape[0] - dataO.shape[0]:} files are coverted and added ")
    name = "Scaled_" + str(data.shape[0]) + ".npy"
    name_lab = "labeld_" + str(label.shape[0]) + ".npy"
    np.save(name, data)
    np.save(name_lab, label)



# load previous npy file if exist
try:
    global outfile, data, data0, label, label0, desired_size
    var1, var2, desired_size = '', '', (48, 48)
    var1 = sys.argv[2] #pixel
    var2 = sys.argv[3] #label
    data = np.load(var1)
    dataO = data[:]
    label = np.load(var2)
    labelO = label[:]
    desired_size = eval(sys.argv[1])

    run(data, label, desired_size)
except Exception as ex:
    tuto = '''
    image2pixel by shinkansan
    =Manual=
    e.g) python img2pixel.py '(48, 48)' data.npy label.npy
    argv[1] = img resize..tuple
    argv[2] = merging existing data npy file
    argv[3] = merging existing label npy file
    '''
    print(tuto)
    print(ex)
