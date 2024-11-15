from src.module.mlforkidsimages import MLforKidsImageProject
import src.module.key as moduleKey
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from playsound import playsound

Imagekey = moduleKey.myImageKey

# how to deal with voice inputs...

# this will train your model and might take a little while
myproject = MLforKidsImageProject(Imagekey)
myproject.train_model()

# example for data you want to input

# label = img1["class_name"]
# confidence = img1["confidence"]

# print ("result: '%s' with %d%% confidence" % (label, confidence))

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
    canvas.itemconfig(normal_face,state="hidden")
    # canvas.itemconfig(happy_face,state="hidden")
    # canvas.itemconfig(sad_face,state="hidden")
    # canvas.itemconfig(angry_face,state="hidden")
    # canvas.itemconfig(anxious_face,state="hidden")
    
main=tk.Tk()
main.title("나만의 로봇 친구")
main.geometry("700x700")
main.resizable(False, False)
main.attributes("-fullscreen", False)

canvas=tk.Canvas(main,width=700,height=700)

normal_face=genImage("C:\\codes\\ProblemSolving\\Introduction-to-AI-projects\\src\\images\\normal_face.webp",(600,600))
# happy_face=genImage("")
# sad_face=genImage("")
# angry_face=genImage("")
# anxious_face=genImage("")
canvas.create_image(50,0,anchor="nw",image=normal_face)

greetStr="안녕! 지금 기분이 어때?"
happyStr="너가 기뻐하니까 나도 기뻐!"
sadStr="많이 슬펐구나.. 힘든 일이 있으면 알려줘!"
angryStr="잠시 명상을 하면서 화를 가라 앉혀보자"
anxiousStr=""



canvas.create_text(350,650,text=greetStr,font=("Noto Sans KR",20))



# if button pressed then image's prediction saved to variable inputImage
btn_open_image=tk.Button(main,text="감정 표현하기",command=open_image)




# install classes
btn_open_image.pack()
canvas.pack()

main.mainloop()