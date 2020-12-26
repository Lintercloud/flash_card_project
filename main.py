from pandas import *
from tkinter import *
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
words_to_learn = {}
#load_data
try:
    word_data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    origin_data = pandas.read_csv("data/english_words1000-2000.csv", encoding = "ISO-8859-1")   #原本的資料不要去動到
    words_to_learn = origin_data.to_dict(orient="records")
else:
    words_to_learn = word_data.to_dict(orient="records")


#data
def get_word():
    global current_card, timmer
    window.after_cancel(timmer)     #在執行此程式先將之前的翻牌停掉
    current_card = random.choice(words_to_learn)     #隨機選牌
    canves.itemconfigure(language_card, text="English", fill="black")
    canves.itemconfigure(word_card, text=current_card["English"], fill="black")
    canves.itemconfigure(card_bg_img, image=card_front_image)
    timmer = window.after(300000, answer_word)  #再執行3秒後翻牌

def answer_word():
    canves.itemconfigure(language_card, text="chinese", fill="white")
    canves.itemconfigure(word_card, text=current_card["chinese"], fill="white")
    canves.itemconfigure(card_bg_img, image = card_back_image)


def is_known():
    words_to_learn.remove(current_card)   #將牌中的card抽掉
    print(len(words_to_learn))
    new_data = pandas.DataFrame(words_to_learn)
    new_data.to_csv("data/words_to_learn.csv", index=False) #每次執行都會增加index,因此index=False是每次不再增加
    get_word()

# #windows

window = Tk()
window.title("Flash Card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
timmer = window.after(3000, answer_word)  #先執行一次

#Canvas

canves = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_image =PhotoImage(file="images/card_front.png")
card_back_image = PhotoImage(file="images/card_back.png")
card_bg_img =canves.create_image(400, 263, image=card_front_image)
canves.grid(column=0, row=0, columnspan=2)

language_card = canves.create_text(400, 150, text="language", font=("Arial", 40, "italic"))
word_card = canves.create_text(400, 263, text="word", font=("Arial", 60, "bold"))

#button
good_image = PhotoImage(file="images/right.png")
bad_image = PhotoImage(file="images/wrong.png")

yes_button = Button(image=good_image, highlightthickness=0, command=is_known)
yes_button.grid(column=1, row=2, columnspan=1)
no_button = Button(image=bad_image, highlightthickness=0, command=get_word)
no_button.grid(column=0, row=2, columnspan=1)


get_word()


window.mainloop()