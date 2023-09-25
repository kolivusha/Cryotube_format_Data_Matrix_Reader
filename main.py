from pylibdmtx.pylibdmtx import decode
from PIL import Image,ImageDraw,ImageFont
import cv2
import time
import re
import numpy as np
from itertools import product
t=time.perf_counter()
path=r'C:\Users\...\600.png'
listCellnames = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12', 'B1', 'B2', 'B3', 'B4',
                 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11', 'B12', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8',
                 'C9', 'C10', 'C11', 'C12', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D11',
                 'D12', 'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10', 'E11', 'E12', 'F1', 'F2', 'F3',
                 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7',
                 'G8', 'G9', 'G10', 'G11', 'G12', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10',
                 'H11', 'H12']
Letters=list('ABCDEFGH')
def gammaCorrection(src, gamma):
    invGamma = 1 / gamma

    table = [((i / 255) ** invGamma) * 255 for i in range(256)]
    table = np.array(table, np.uint8)

    return cv2.LUT(src, table)

resultsls=[]
original=cv2.imread(path)
copy=original
img = cv2.cvtColor(original, cv2.COLOR_RGB2GRAY)

img=~img
img=gammaCorrection(img,1.4)
kernel = np.ones((3, 3), np.uint8)
img = cv2.medianBlur(img,3)
img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
w, h = img.shape
print(f"{w=},{h=}")
s=h//12
c=20
color = (0, 0, 255)
count=0
for i in range(12):
    for j in range(8):
        out=img[j*s+c: j*s + s-c, i*s+c:i*s+s-c]
        colorout=original[j*s+c: j*s + s-c, i*s+c:i*s+s-c]
        result=''
        a=decode(out,max_count=1)
        print(f"{a=}")
        if len(set(a))==1:
            result = (re.search("data=b'(.*)'", str(a))).group(1)
            resultsls.append(result)
        scale_percent = 200  # percent of original size
        width = int(colorout.shape[1] * scale_percent / 100)
        height = int(colorout.shape[0] * scale_percent / 100)
        dim = (width, height)
        scaledown = cv2.resize(out, dim, interpolation=cv2.INTER_AREA)
        cv2.imshow('scaledown', scaledown)
        color = (153,255,0)
        c=0
        cv2.putText(copy, str(result), (i * s + c+25, j * s + c + s), cv2.FONT_HERSHEY_SIMPLEX, .8, (0, 0, 0), 3, cv2.LINE_AA)
        cv2.putText(copy,str(result), (i*s+c+25, j*s+c+s), cv2.FONT_HERSHEY_SIMPLEX, .8, color, 2, cv2.LINE_AA)
        cellname=f'{i=}_{j=}'
        cellname=f'{Letters[j]}{i+1}'
        color = (15,100,250)
        cv2.putText(copy, cellname, (i * s + c+25, j * s + c + s-30), cv2.FONT_HERSHEY_SIMPLEX, .8, (0, 0, 0), 3, cv2.LINE_AA)
        cv2.putText(copy,cellname, (i*s+c+25, j*s+c+s-30), cv2.FONT_HERSHEY_SIMPLEX, .8, color, 2, cv2.LINE_AA)

        if result==[]:
            cv2.waitKey(50)
        cv2.waitKey(50)
        count+=1
def checkConsecutive(l):
    try:
        l=[int(x) for x in l]
        return sorted(l) == list(range(min(l), max(l)+1))
    except:
        return False

print(f"{len(resultsls)=}")
print(f"{len(set(resultsls))=}")
print(f"{(resultsls)=}")
print(f"{sorted(set(resultsls))=}")
elapsed_time = round(time.perf_counter() - t, 2)
print(f"{elapsed_time=}")
numonly=[x[0:8] for x in resultsls]
print(f"{checkConsecutive(numonly)=}")
print(f"duplicates {set([x for x in resultsls if resultsls.count(x) > 1])=}")

filename = path[:-4] + f'individually read {len(set(resultsls))}.png'
cv2.imwrite(filename, copy)
