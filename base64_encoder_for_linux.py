import tkinter as tk
from tkinter import *
from tkinter import messagebox, ttk
from tkinter.filedialog import askopenfilenames
import base64
from time import sleep
import os.path

window = Tk()
window.geometry('600x300')
window.resizable(False, False)
window.title(" ")
window.wm_attributes('-topmost', 'True')

bg = PhotoImage(file="img/background_image.png")
background_label = Label(image=bg)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
file_path = ""
interrupted = False


def stop_encoding():
    global interrupted
    interrupted = True


def base64_encode(file_path):
    global interrupted
    interrupted_message = None
    # Select output directory
    try:
        window.tk.call('tk_getOpenFile', '-')
    except TclError:
        pass
    window.tk.call('set', '::tk::dialog::file::showHiddenVar', '0')
    output_dir = tk.filedialog.askdirectory(initialdir='/home/', title='Save encoded files to:')

    if output_dir:
        # Define Progress bar parameters
        popup = tk.Toplevel()
        tk.Label(popup, text='Processing...', font='10').grid(row=1, column=1)
        popup.wm_attributes('-topmost', 'True')
        progress_var = tk.IntVar()
        progress_bar = ttk.Progressbar(popup, variable=progress_var, length=300, maximum=100, mode='indeterminate')
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
    try:
        window.tk.call('tk_getOpenFile', '-')
    except TclError:
        pass
    window.tk.call('set', '::tk::dialog::file::showHiddenVar', '0')
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
       width=9,
       font='Verdana 13 bold').place(x=225, y=80)

Button(window, text='Encode',
       command=encoding_validation,
       activebackground='light blue',
       bg='green',
       fg='white',
       bd='5px',
       height=1,
       width=9,
       font='Verdana 13 bold').place(x=225, y=160)

window.mainloop()
