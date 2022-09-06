import sys
import os
import base64
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilenames
from tkinter.font import Font

window = Tk()
window.geometry('600x300')
window.title(" ")

custom_font = Font(
    family="Britannic Bold",
    size=30,
    weight="bold"
)


def resource_path(relative):
    return os.path.join(
        os.environ.get(
            "_MEIPASS2",
            os.path.abspath(".")
        ),
        relative
    )


def resource_path2(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


bg_path = resource_path2("images/background_image.png")
bg = PhotoImage(file=bg_path)
icon_path = resource_path2("images/64.ico")

background_label = Label(image=bg)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
window.iconbitmap(icon_path)
Label(window, text="BASE64 ENCODER",
      font=custom_font).pack(pady=10)
file_path = ""


def select_file():
    global file_path
    file_path = askopenfilenames(initialdir="/")


def b64_encode():
    if file_path:
        for file in file_path:
            with open(file, "rb") as input_file:
                encoded_string = base64.b64encode(input_file.read())
            with open(f"{file.split('/')[-1]}_base64.txt", "w") as output_file:
                encoded_str = str(encoded_string).replace("b", "", 1)
                final_str = encoded_str.replace("'", "")
                output_file.write(final_str)
        return messagebox.showinfo(" ", "Encoding completed!")
    else:
        return messagebox.showinfo(" ", "Please select one or more files!")


frame = Frame()
frame.pack()

Button(window, text="Select file(s)",
       command=select_file,
       bg="green",
       fg="white",
       font="Verdana 13 bold").pack(pady=20, padx=20)

Button(window, text="Encode",
       command=b64_encode,
       bg="brown",
       fg="white",
       font="Verdana 21 bold").pack(pady=20, padx=20)

window.mainloop()