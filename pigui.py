from tkinter import *
import tkinter.font
from gpiozero import LED
import RPi.GPIO
import os
import glob

RPi.GPIO.setmode(RPi.GPIO.BCM)
import picamera
import time

class Menu:
    def __init__(self, win):
        self.camera = picamera.PiCamera()
        self.camera.vflip = True
        self.camera.hflip = True
        self.count = 0
        self.win = win
        self.status = Label(self.win, text="Camera ready", bg='green', height=1, width=24)
        self.status.grid(row=0, column=1)

        self.cam_button = Button(self.win, text="Take photo", command=self.cam_func, bg='bisque2', height=1, width=24)
        self.cam_button.grid(row=1, column=1)

        self.exit_button = Button(self.win, text="Exit", command=self.close, bg='red', height=1, width=24)
        self.exit_button.grid(row=2, column=1)

        self.restart_button = Button(self.win, text="Restart", command=self.restart_program, bg='yellow', height=1, width=24)
        self.restart_button.grid(row=3, column=1)

    # event functions
    def cam_func(self):
        filename = "raw" + str(self.count) + ".jpg"
        self.count += 1
        self.camera.capture(filename)
        self.status["text"] = "photo captured"

    def close(self):
        RPi.GPIO.cleanup()
        self.win.destroy()

    def restart_program(self):
        for i in glob.glob("*.jpg"):
            os.remove(i)
        python = sys.executable
        os.execl(python, python, *sys.argv)

if __name__=="__main__":
    win = tkinter.Tk()
    win.title("Image Capturer")
    menu = Menu(win)
    win.mainloop()