from src.module.mlforkidsimages import MLforKidsImageProject
import src.module.key as moduleKey
# treat this key like a password and keep it secret!
Imagekey = moduleKey.myImageKey

# this will train your model and might take a little while
myproject = MLforKidsImageProject(Imagekey)
myproject.train_model()

# # CHANGE THIS to the image file you want to recognize
# img1 = myproject.prediction("C:\codes\ProblemSolving\Introduction-to-AI-projects\src\images\img1.jpg")

# label = img1["class_name"]
# confidence = img1["confidence"]

# # CHANGE THIS to do something different with the result
# print ("result: '%s' with %d%% confidence" % (label, confidence))

import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from playsound import playsound

global inputImage

def genImage(path,size):
    tmp_img=Image.open(path)
    tmp_img=tmp_img.resize(size)
    return ImageTk.PhotoImage(tmp_img)

def open_image():
    path = filedialog.askopenfilename(
        title="감정을 고르세요!",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")]
    )
    if path:
        inputImage=myproject.prediction(path)


main=tk.Tk()
main.title("나만의 로봇 친구")
main.geometry("700x700")

canvas=tk.Canvas(main,width=700,height=700)

normal_face=genImage("C:\\codes\\ProblemSolving\\Introduction-to-AI-projects\\src\\images\\normal_face.webp",(600,600))

canvas.create_image(50,0,anchor="nw",image=normal_face)

greet="안녕! 오늘 하루는 어땠어?"
canvas.create_text(350,650,text=greet,font=("Noto Sans KR",20))

# if button pressed then image's prediction saved to variable inputImage
btn_open_image=tk.Button(main,text="감정 표현하기",command=open_image)




canvas.pack()

main.mainloop()