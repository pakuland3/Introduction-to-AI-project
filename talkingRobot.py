from src.module.mlforkidsimages import MLforKidsImageProject
from src.module.voiceML import voiceML
import src.module.key as moduleKey
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from playsound import playsound

Imagekey = moduleKey.myImageKey # my key got changed

# how to deal with voice inputs...

# this will train your model and might take a little while
myproject = MLforKidsImageProject(Imagekey)
myproject.train_model()

# example for data you want to input

# label = img1["class_name"]
# confidence = img1["confidence"]

# print ("result: '%s' with %d%% confidence" % (label, confidence))

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
    else:
        print("path is inavailable")
        main.quit()
    for name in displayImage.keys():
        canvas.itemconfig(displayImageId[name],state="hidden")
    canvas.itemconfig(displayImageId[inputImage["class_name"]],state="normal")
    for name in displayText.keys():
        canvas.itemconfig(displayTextId[name],state="hidden")
    canvas.itemconfig(displayTextId[inputImage["class_name"]],state="normal")
    
main=tk.Tk()
main.title("나만의 로봇 친구")
main.geometry("700x700")

# disable fullscreen
main.resizable(False, False)
main.attributes("-fullscreen", False)

canvas=tk.Canvas(main,width=700,height=700)

displayImage={"normal":genImage("C:\\codes\\ProblemSolving\\Introduction-to-AI-project\\src\\images\\normal.webp",(600,600)),
              "happy":genImage("C:\\codes\\ProblemSolving\\Introduction-to-AI-project\\src\\images\\happy.webp",(600,600)),
              "sad":genImage("C:\\codes\\ProblemSolving\\Introduction-to-AI-project\\src\\images\\sad.webp",(600,600)),
              "angry":genImage("C:\\codes\\ProblemSolving\\Introduction-to-AI-project\\src\\images\\angry.webp",(600,600)),
              "anxious":genImage("C:\\codes\\ProblemSolving\\Introduction-to-AI-project\\src\\images\\anxious.webp",(600,600))
            }

displayImageId={"normal":0,
              "happy":0,
              "sad":0,
              "angry":0,
              "anxious":0
            }

displayText={"greet":"안녕! 지금 기분이 어때?",
            "happy":"너가 기뻐하니까 나도 기뻐!",
            "sad":"많이 슬펐구나.. 힘든 일이 있으면 알려줘!",
            "angry":"잠시 호흡을 하면서 화를 가라 앉혀보자",
            "anxious":"많이 힘들구나? 우리 같이 힘내자!"
            }

displayTextId={"greet":"안녕! 지금 기분이 어때?",
            "happy":"너가 기뻐하니까 나도 기뻐!",
            "sad":"많이 슬펐구나.. 힘든 일이 있으면 알려줘!",
            "angry":"잠시 호흡을 하면서 화를 가라 앉혀보자",
            "anxious":"많이 힘드세요? 우리 같이 힘내봐요!"
            }



# if button pressed then image's prediction saved to variable inputImage
btn_open_image=tk.Button(main,text="감정 표현하기",command=open_image)


# create image on canvas
for name in displayImage.keys():
    displayImageId[name]=canvas.create_image(50,0,anchor="nw",image=displayImage[name])
    canvas.itemconfig(displayImage[name],state="hidden")

canvas.itemconfig(displayImage["normal"],state="normal")


# create text on canvas
for name in displayText.keys():
    displayTextId[name]=canvas.create_text(350,650,text=displayText[name],font=("Noto Sans KR",20))
    canvas.itemconfig(displayTextId[name],state="hidden")

canvas.itemconfig(displayTextId["greet"],state="normal")

# install classes
btn_open_image.pack()
canvas.pack()

main.mainloop()