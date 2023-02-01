from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import json
from difflib import get_close_matches
import sqlite3

data = json.load(open("words.json"))

window = Tk()
window.title("Dictionary")
window.geometry("580x400+350+200")
image = Image.open('eiffel.jpg')
bcg = ImageTk.PhotoImage(image)
bcgl = Label(window, image=bcg)
bcgl.place(x=0, y=0)

def search(word):

    if word in data:
        return data[word]
    elif len(get_close_matches(word, data.keys())) > 0:
        yn = messagebox.askyesno(title="Confirmation", message="Did you mean "+get_close_matches(word, data.keys())[0]+" instead?")
        if yn == True:
            return data[get_close_matches(word, data.keys())[0]]
        elif yn == False:
            return "The word doesn't exist."
        else:
            return "Wrong entry."
    else:
        return "The word doesn't exist. Check the word again"

def view():
    conn = sqlite3.connect("words.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM recent")
    rows = cur.fetchall()
    conn.close()
    label2 = Label(text="HISTORY", font=('arial', 10, 'bold','italic'), bg="skyblue").place(x=70, y=250)
    t2 = Text(window, bg="grey",  height=6, width=62)
    t2.place(x=50, y=285)
    t2.delete('1.0', END)
    t2.insert(END, "Recent words are :\n\n")
    t2.insert(END, rows)

word = StringVar()
label1 = Label(text="Enter the word", font=(
    'arial', 10, 'bold', 'italic'), bg="skyblue").place(x=70, y=30)

menu = Menu()
file = Menu()
file.add_command(label='Recent Words', command=view)
menu.add_cascade(label="Options", menu=file)
window.config(menu=menu)

e1 = Entry(window, width=55, textvariable=word, bg="silver").place(
    x=179, y=30)  # .grid(row=0, column=10)

def dictionary():
    conn = sqlite3.connect("words.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO recent VALUES (?)", (word.get(),))
    conn.commit()
    conn.close()
    view()
    meaning = search(word.get())
    count = 0
    if type(meaning) == list:
        t1.delete('1.0', END)
        t1.insert(END, str(len(meaning))+" meanings found.\n")
        for item in meaning:
            count += 1
            t1.insert(END, str(count)+": "+item)
            t1.insert(END, '\n')
    else:
        t1 .delete('1.0', END)
        t1.insert(END, meaning)
        t1.insert(END, '\n')

b1 = Button(window, text="Search", command=dictionary, font=('arial', 13,'italic', 'bold'), bg="Plum3").place(x=250, y=60)

t1 = Text(window, height=8, width=62, bg="silver")
t1.place(x=50, y=105)

window.mainloop()