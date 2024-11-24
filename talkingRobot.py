# program should be executed on folder that contains this "talkingRobot.py" file.
# programmed with relative path

from src.module.mlforkidsimages import MLforKidsImageProject
from src.module.voiceML import getPrediction
import src.module.key as moduleKey
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from playsound import playsound
import random as rd

mlk_key = moduleKey.key

# this will train your model and might take a little while
myproject = MLforKidsImageProject(mlk_key)
myproject.train_model()

def genImage(path,size):
    tmp_img=Image.open(path)
    tmp_img=tmp_img.resize(size)
    return ImageTk.PhotoImage(tmp_img)

def renew(emotion):
    canvas.itemconfig(imageId,image=displayImage[emotion])
    idx=rd.randint(0,4)
    canvas.itemconfig(textId,text=displayText[emotion][idx])
    main.after(1500,lambda:playsound(textAudios[emotion][idx]))

def open_image():
    path = filedialog.askopenfilename(
        title="감정을 고르세요!",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")]
    )
    if path:
        inputImage=myproject.prediction(path)
        renew(inputImage["class_name"])
    else:
        print("path is inavailable.\nplease open file again")

def open_audio():
    path = filedialog.askopenfilename(
        title="감정을 고르세요!",
        filetypes=[("Audio files", "*.wav *.mp3")]
    )
    if path:
        renew(getPrediction(path))
    else:
        print("path is inavailable.\nplease open file again")

main=tk.Tk()
main.title("나만의 로봇 친구")
main.geometry("800x750")

# disable fullscreen
main.resizable(False, False)
main.attributes("-fullscreen", False)

canvas=tk.Canvas(main,width=800,height=700)

displayImage={
              "greet":genImage("src\\images\\greet.webp",(600,600)),
              "happy":genImage("src\\images\\happy.webp",(600,600)),
              "sad":genImage("src\\images\\sad.webp",(600,600)),
              "angry":genImage("src\\images\\angry.webp",(600,600)),
              "anxious":genImage("src\\images\\anxious.webp",(600,600))
}

displayText={
            "greet":["안녕하세요! 지금 기분이 어떠신가요?"],
            "happy":["정말 행복한 하루를 보내고 계신 것 같아요!\n더 듣고 싶어요. 어떤 일이 있었나요?",
                     "웃는 얼굴을 보니 저도 덩달아 행복해져요.\n오늘 더 즐겁게 지내세요!",
                     "기쁘다는 건 정말 좋은 일이죠!\n이런 순간이 많아지면 좋겠어요.",
                     "오늘 정말 멋진 하루네요.\n혹시 다른 재미있는 일도 있었나요?",
                     "와, 정말 멋진 이야기네요!\n이런 기쁜 일이 더 많이 생기길 바래요."
            ],
            "sad":[
                "마음이 많이 무거우신 것 같아요.\n제가 옆에서 이야기 들어드릴게요.",
                "힘드신 일이 있으셨던 것 같아요.\n저에게 말씀해주시면 마음이 조금 나아지실 수도 있어요.",
                "언제나 힘든 시간 뒤엔 좋은 날이 오니까,\n제가 곁에서 응원할게요.",
                "많이 속상하셨겠어요.\n괜찮으시다면 더 이야기 나눠봐요.",
                "지금 느끼는 감정도 소중해요.\n제가 함께 있어드릴게요."
            ],
            "angry":[
                "무엇 때문에 속상하신지 말씀해주시면\n제가 도와드릴게요.",
                "화가 나셨을 땐 깊게 숨을 들이마시고\n내쉬는 것도 도움이 될 수 있어요. 한번 같이 해볼까요?",
                "화가 날 땐 누구나 힘들죠.\n제가 옆에서 차분히 들어드릴게요.",
                "속상한 일은 저에게 이야기하시면\n조금이라도 마음이 풀리실 거예요.",
                "화난 기분을 풀 수 있는 좋은 방법이 있을까요?\n함께 찾아봐요."
            ],
            "anxious":[
                "걱정이 많으신 것 같아요.\n무슨 일이 있으셨나요?",
                "불안한 마음은 자연스러운 거예요.\n제가 곁에서 함께 해드릴게요.",
                "혹시 마음을 차분히 할 수 있는\n이야기를 나눠볼까요?",
                "어떤 걱정이든 혼자 느끼지 않으셔도 돼요.\n제가 여기 있어요.",
                "지금은 조금 불안하셔도,\n제가 있으면 안심이 될 거예요."
            ]
}

textAudios={
            "greet":["src\\voices\\greet\\0.wav"],
            "happy":["src\\voices\\happy\\1.wav",
                     "src\\voices\\happy\\2.wav",
                     "src\\voices\\happy\\3.wav",
                     "src\\voices\\happy\\4.wav",
                     "src\\voices\\happy\\5.wav"
            ],
            "sad":[
                "src\\voices\\sad\\6.wav",
                "src\\voices\\sad\\7.wav",
                "src\\voices\\sad\\8.wav",
                "src\\voices\\sad\\9.wav",
                "src\\voices\\sad\\10.wav"
            ],
            "angry":[
                "src\\voices\\angry\\11.wav",
                "src\\voices\\angry\\12.wav",
                "src\\voices\\angry\\13.wav",
                "src\\voices\\angry\\14.wav",
                "src\\voices\\angry\\15.wav"
            ],
            "anxious":[
                "src\\voices\\anxious\\16.wav",
                "src\\voices\\anxious\\17.wav",
                "src\\voices\\anxious\\18.wav",
                "src\\voices\\anxious\\19.wav",
                "src\\voices\\anxious\\20.wav"
            ]
}

# if button pressed then image's prediction saved to variable inputImage
btn_open_image=tk.Button(main,text="감정 표현하기(이미지)",command=open_image,font=("Noto Sans KR",15))
btn_open_audio=tk.Button(main,text="감정 표현하기(음성)",command=open_audio,font=("Noto Sans KR",15))

# create image on canvas
imageId=canvas.create_image(75,0,anchor="nw",image=displayImage["greet"])
canvas.itemconfig(imageId,state="normal")

# create text on canvas       
textId=canvas.create_text(375,635,text=displayText["greet"][0],font=("Noto Sans KR",20))
canvas.itemconfig(textId,state="normal")

# install widget

canvas.pack(side="top")
btn_open_image.pack(side="left")
btn_open_audio.pack(side="right")

main.after(3500,lambda:playsound(textAudios["greet"][0]))

main.mainloop()