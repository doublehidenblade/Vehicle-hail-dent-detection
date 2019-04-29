from tkinter import *
from PIL import ImageTk,Image
import tkinter
import cv2
import numpy as np
from skimage import io
import skimage.morphology as morp
from skimage.filters import rank
from skimage.transform import AffineTransform, warp
from skimage import data
from skimage.segmentation import clear_border
from skimage.filters import threshold_otsu
from skimage.measure import label, regionprops
from skimage.morphology import closing, square
from skimage.color import label2rgb
from skimage.filters import gaussian
import skimage
import time

root = Tk()
root.title("Dent Detector")
upper = Canvas(root, width = 1000, height = 1000)
upper.grid(row=0, column=0)
canvas = Canvas(upper, width = 1000, height = 1000)
canvas.grid(row=0, column=0)
control = Canvas(upper, width = 200, height = 1000)
control.grid(row=0, column=1)
lower = Canvas(root, width = 1000, height = 50)
lower.grid(row=1, column=0)


result = Label(lower, text="Click the buttons from top down, like what a normal human would do.")
result.grid(row=0, column=0)
background = np.ones([1080, 1920], dtype=np.uint8)
cv2.imwrite("background.jpg",background)
origin = Image.open("background.jpg")
origin = origin.resize((800, 800), Image.ANTIALIAS)
origin = ImageTk.PhotoImage(origin)
panel = tkinter.Label(canvas, image=origin)
panel.grid(row=0, column=0)

class RawImage:
    def __init__(self,rawinput = None):
        self.rawinput = rawinput
        self.norm = None
        self.denoised = None
        self.extracted = None
        self.shifted = None
        self.clustered = None
        self.result = None
        self.detectNumber = None
        self.detectarr = []
    def normalize(self, ds1 = 50,ds2 = 20,t_norm = None):#ds1 equalize disk size;ds2 enhance contrast disk size
        self.rawinput = cv2.imread('stitch.jpg',cv2.COLOR_BGR2GRAY)
        # img = raw.rawinput
        # kernel = morp.disk(ds1)
        # kernel2 = morp.disk(ds2)
        # norm_image = rank.equalize(img, selem=kernel)
        # norm_image = rank.enhance_contrast(norm_image, selem=kernel2)
        img= cv2.imread('Best.jpg')
        mask = cv2.imread("mask.jpg")
        mask = cv2.resize(mask, (img.shape[1], img.shape[0]))
        masked = cv2.bitwise_and(img, mask)
        cv2.imwrite("norm.jpg", masked)
        self.norm = cv2.imread('norm.jpg')
        # show
        imgshow = Image.open("norm.jpg")
        imgshow = imgshow.resize((800, 800), Image.ANTIALIAS)
        imgshow = ImageTk.PhotoImage(imgshow)
        panel.configure(image=imgshow)
        panel.image = imgshow
        # update text
        t_norm.destroy()
        done = Label(control, text="Normalizing done", foreground="green")
        done.grid(row=2, column=2)
        return


    def extract(self,save = False, t_extract = None,param = 1):
        # process
        bw = self.norm
        horizontal = np.copy(bw)
        # Create structure element for extracting horizontal lines through morphology operations
        cols = horizontal.shape[1]
        horizontal_size = int(cols / param)
        horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontal_size, 1))
        horizontal = cv2.erode(horizontal, horizontalStructure)
        horizontal = cv2.dilate(horizontal, horizontalStructure)
        subtracted = cv2.subtract(bw, horizontal)
        self.extracted = subtracted
        cv2.imwrite("extracted.jpg", subtracted)
        # show
        imgshow = Image.open("extracted.jpg")
        imgshow = imgshow.resize((800, 800), Image.ANTIALIAS)
        imgshow = ImageTk.PhotoImage(imgshow)
        panel.configure(image=imgshow)
        panel.image = imgshow
        # update text
        t_extract.destroy()
        done = Label(control, text="Extracting done", foreground="green")
        done.grid(row=3, column=2)

    def Shift(self, vector = (0,3),t_shift = None):
        # process
        img = self.extracted
        transform = AffineTransform(translation=vector)
        shifted = warp(img, transform, mode='wrap', preserve_range=True)
        shifted = shifted.astype(img.dtype)
        anded = cv2.bitwise_and(img, shifted)
        self.shifted = anded
        cv2.imwrite("shifted.jpg", anded)
        # show
        imgshow = Image.open("shifted.jpg")
        imgshow = imgshow.resize((800, 800), Image.ANTIALIAS)
        imgshow = ImageTk.PhotoImage(imgshow)
        panel.configure(image=imgshow)
        panel.image = imgshow
        # update text
        t_shift.destroy()
        done = Label(control, text="Shifting done", foreground="green")
        done.grid(row=4, column=2)
    def Cluster(self,t_cluster = None, param=10):
        img = self.shifted
        skgaussian = gaussian(img, sigma=param)
        _, threshed = cv2.threshold(skgaussian, 0.1, 255, cv2.THRESH_BINARY)
        skgaussian2 = gaussian(threshed, sigma=0)
        mykernel = np.array([[-1, -1, -1], [-1, 10, -1], [-1, -1, -1]])
        sharpen = cv2.filter2D(skgaussian2, -1, mykernel)
        self.clustered = sharpen
        cv2.imwrite("clustered.jpg", sharpen)
        # show
        imgshow = Image.open("clustered.jpg")
        imgshow = imgshow.resize((800, 800), Image.ANTIALIAS)
        imgshow = ImageTk.PhotoImage(imgshow)
        panel.configure(image=imgshow)
        panel.image = imgshow
        # update text
        t_cluster.destroy()
        done = Label(control, text="Clustering done", foreground="green")
        done.grid(row=5, column=2)
        return

    def Detection(self,t_detect = None,result = None):
        # process
        origin = self.rawinput
        image =skimage.color.rgb2gray(self.clustered)
        thresh = threshold_otsu(image)
        bw = closing(image > thresh, square(1))
        bw = clear_border(bw)
        label_image = label(bw)
        quarter, nickel, dime = 0, 0, 0
        for region in regionprops(label_image):
            # take regions with large enough areas
            if 80000 > region.area >= 1000:
                # print("region area: %d" %region.area)
                if region.area > 50000:
                    quarter += 1
                elif region.area > 20000:
                    nickel += 1
                elif region.area >= 5000:
                    dime += 1
                # draw rectangle around segmented area
                minr, minc, maxr, maxc = region.bbox
                if float(maxc - minc) / float(maxr - minr) > 0.667 and float(maxc - minc) / float(maxr - minr) < 1.5:
                    cv2.rectangle(origin, (minc, minr + (maxr - minr)), (minc + (maxc - minc), minr), (255, 255, 255), 10)
        self.result = origin
        cv2.imwrite("detected.jpg", origin)
        # show
        imgshow = Image.open("detected.jpg")
        imgshow = imgshow.resize((800, 800), Image.ANTIALIAS)
        imgshow = ImageTk.PhotoImage(imgshow)
        panel.configure(image=imgshow)
        panel.image = imgshow

        # update text
        t_detect.destroy()
        done = Label(control, text="Detecting done", foreground="green")
        done.grid(row=6, column=2)
        # show result
        if quarter + nickel + dime <= 5:
            value = dime * 65 + nickel * 75 + quarter * 100
            condition = "very light"
        elif quarter + nickel + dime <= 15:
            value = dime * 100 + nickel * 125 + quarter * 150
            condition = "light"
        elif quarter + nickel + dime <= 30:
            value = dime * 150 + nickel * 200 + quarter * 225
            condition = "moderate"
        else:
            value = dime * 200 + nickel * 225 + quarter * 225
            condition = "severe"
        result.destroy()
        result = Label(lower,
                       text="{} quarter size dents, {} nickel size dents, {} dime size dents. Damage condition is {}.".format(
                           quarter, nickel, dime, condition), foreground="purple")
        result.grid()
raw = RawImage()


def normalizeforStitch(img, ds1=50, ds2=20, t_norm=None):  # ds1 equalize disk size;ds2 enhance contrast disk size
    kernel = morp.disk(ds1)
    kernel2 = morp.disk(ds2)
    norm_image = rank.equalize(img, selem=kernel)
    norm_image = rank.enhance_contrast(norm_image, selem=kernel2)
    # show
    return norm_image

def stitch(num = 23,mode = 'auto',arr = []):
    # process
    background = np.ones([int(num*1080/4.5),1920],dtype=np.uint8)
    background.fill(255)
    length = len(background)
    image = []
    for i in range(1,num+1):
        image.append(cv2.imread("raw" + str(i)+'.jpg',0))
    sec = int(1080/4.5)
    mid = int(1080/2)
    file = open('shift.txt', 'r')
    for line in file.readlines():
        arr.append(int(line))
    file.close()
    start = 0
    if mode == 'auto':
        k = 180
        for i in range(0,num):
                start = i*sec
                temp = int(1080*5/12 + 190 - i*(12+i/9))
                obj = image[i][temp:temp+sec][0:1920]
                background[start:start+sec]= obj
    if mode == 'manual':
        count = 0
        for i in arr:
            start += i
            if start < length:
                if start + sec < length:
                    for j in range(0, sec):
                        background[start + j] = image[count][mid - int(sec / 2) + j][0:1920]
                else:
                    for j in range(0, length - start):
                        background[start + j] = image[count][mid - int(sec / 2) + j][0:1920]
            else:
                break
            count+=1



    img = cv2.imwrite('stitch.jpg', background)
    # show
    imgshow = Image.open("stitch.jpg")
    imgshow = imgshow.resize((800, 800), Image.ANTIALIAS)
    imgshow = ImageTk.PhotoImage(imgshow)
    panel.configure(image=imgshow)
    panel.image = imgshow
    # update text
    done = Label(control, text="Stitching done", foreground="green")
    done.grid(row=1, column=2)
