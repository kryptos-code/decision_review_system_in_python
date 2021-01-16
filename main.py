import tkinter
import cv2  # install using pip
import PIL.Image, PIL.ImageTk # install using pip
from functools import partial # used to take argument in function in command arg of button
import threading # creating a different loop for pending function
import imutils # framing the images and resizing
import time

stream = cv2.VideoCapture("clip.mp4")
flag = True
def play(speed):
    global flag
    print(f"You clicked on play. speed is {speed}")
    
    frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES, frame1 + speed)

    grabbed, frame = stream.read()
    if not grabbed:
        exit()
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image=frame, anchor=tkinter.NW)
    if flag:
        canvas.create_text(135, 26, fill="yellow", font="Times 26 bold", text="Decision Pending")
    flag = not flag

def pending(decision):
#1. Display decision pending image
    frame = cv2.cvtColor(cv2.imread("pending.png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image= frame, anchor=tkinter.NW)
#2. Wait for 1 second
    time.sleep(1)
#3. Display sponson image
    frame = cv2.cvtColor(cv2.imread("sponsor.png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image= frame, anchor=tkinter.NW)
#4. Wait for 1.5 sec.
    time.sleep(1.5)
#5. Display Decision image
    if decision == 'out':
        decisionImg = 'out.png'
    else:
        decisionImg = 'not_out.png'
    frame = cv2.cvtColor(cv2.imread(decisionImg), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image= frame, anchor=tkinter.NW)
#6. Wait for 1.5 sec.
    

def out():
    thread = threading.Thread(target=pending, args=("out",))
    thread.daemon = 1
    thread.start()
    print("Player is out")

def not_out():
    thread = threading.Thread(target=pending, args=("not out",))
    thread.daemon = 1
    thread.start()
    print("Player is not out")

# setting width and height of the main screen
SET_WIDTH = 640
SET_HEIGHT = 480

# Initializing gui
window = tkinter.Tk()
window.title("Third Umpire Decision Review Kit by Shoaib Rehman")
cv_img = cv2.cvtColor(cv2.imread("welcome.png"), cv2.COLOR_BGR2RGB)
canvas = tkinter.Canvas(window, width = SET_WIDTH, height = SET_HEIGHT) 
photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(cv_img))
image_on_canvas = canvas.create_image(0, 0, ancho=tkinter.NW, image=photo)
canvas.pack()

# Playback Controller Buttons
btn = tkinter.Button(window, text= "<< Previous (fast)",width = 50,\
    command=partial(play, -25))
btn.pack()

btn = tkinter.Button(window, text= "<< Previous (slow)",width = 50,\
    command=partial(play, -2))
btn.pack()

btn = tkinter.Button(window, text= "Next (slow) >>",width = 50,\
    command=partial(play, 2))
btn.pack()

btn = tkinter.Button(window, text= "Next (fast) >>",width = 50,\
    command=partial(play, 25))
btn.pack()

btn = tkinter.Button(window, text= "Give OUT",width = 50, command=out)
btn.pack()

btn = tkinter.Button(window, text= "Give Not OUT",width = 50, command=not_out)
btn.pack()

window.mainloop()

