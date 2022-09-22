import tkinter as tk
from tkinter import *
from tkinter import messagebox, ttk
from tkinter.filedialog import askopenfilenames
import base64
from time import sleep
import os.path

window = Tk()
window.geometry('600x350-500+250')
window.resizable(False, False)
window.title(" ")
window.wm_attributes('-topmost', 'True')


def resource_path(relative):
    # 1. Function for creating a path for the images(for Windows app only)
    return os.path.join(
        os.environ.get(
            "_MEIPASS2",
            os.path.abspath(".")
        ),
        relative
    )


def resource_path2(relative_path):
    # 2. Function for creating a path for the images(for Windows app only)
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


bg_path = resource_path2("img/background_image.png")
bg = PhotoImage(file=bg_path)
icon_path = resource_path2("img/64.ico")
background_label = Label(image=bg)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
window.iconbitmap(icon_path)
file_path = ""
interrupted = False


def stop_encoding():
    global interrupted
    interrupted = True


def base64_encode(file_path):
    global interrupted
    interrupted_message = None

    # Select output directory
    output_dir = tk.filedialog.askdirectory(initialdir='/home/', title='Save encoded files to:')

    if output_dir:
        # Define Progress bar parameters
        popup = tk.Toplevel()
        tk.Label(popup, text='Processing...', font='15').grid(row=1, column=1)
        win_x = window.winfo_rootx()
        win_y = window.winfo_rooty()
        position_x = win_x + 150
        position_y = win_y + 150
        popup.geometry(f'+{position_x}+{position_y}')
        popup.wm_attributes('-topmost', 'True')
        popup.iconbitmap(icon_path)
        progress_var = tk.IntVar()
        progress_bar = ttk.Progressbar(popup, variable=progress_var, length=300, mode='indeterminate')
        progress_bar.grid(row=2, column=1)
        popup.pack_slaves()
        progress = 0
        progress_step = 10
        popup.protocol("WM_DELETE_WINDOW", stop_encoding)

        # Start encoding
        list_of_files = list(file_path)
        for file in list_of_files:
            if interrupted:
                popup.destroy()
                interrupted_message = messagebox.showinfo(' ', 'Encoding interrupted by user!')
                interrupted = False
                break
            with open(file, 'rb') as input_file:
                encoded_string = base64.b64encode(input_file.read())
                file_name = f"{file.split('/')[-1]}_base64.txt"
                encoded_str = str(encoded_string).replace("b", "", 1)
                base64_str = encoded_str.replace("'", "")
                complete_file_path = os.path.join(output_dir, file_name)
            with open(complete_file_path, 'w') as output_file:
                output_file.write(base64_str)

                popup.update()
                sleep(0.05)
                progress += progress_step
                progress_var.set(progress)

        # Close the progress bar when encoding is finished
        sleep(0.5)
        popup.destroy()
        if not interrupted_message:
            return messagebox.showinfo(' ', 'Encoding completed!')


def select_file():
    # Select files from local directory (1000 files max)
    global file_path
    file_path = askopenfilenames(initialdir='/home/',
                                 title='Select files to encode',
                                 filetypes=(('Images', '.jpeg .jpg .png .svg .bmp .gif .tiff .tif .ico'),
                                            ('PDF files', '.pdf'), ('All files', '*.*')))
    if len(list(file_path)) > 1000:
        file_path = None
        return messagebox.showinfo(' ', 'Please select up to 1000 files!')


def encoding_validation():
    if not file_path:
        return messagebox.showinfo(' ', 'Please select at least one file to encode!')
    else:
        base64_encode(file_path)


Button(window, text='Select files',
       command=select_file,
       activebackground='light blue',
       bg='OrangeRed3',
       fg='white',
       bd='5px',
       height=1,
       width=10,
       font='Verdana 13 bold').place(x=230, y=110)

Button(window, text='Encode',
       command=encoding_validation,
       activebackground='light blue',
       bg='green',
       fg='white',
       bd='5px',
       height=1,
       width=10,
       font='Verdana 13 bold').place(x=230, y=190)

window.mainloop()
