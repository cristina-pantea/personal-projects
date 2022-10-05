import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image
from pytube import YouTube
import os
import ffmpy

format_list = []
quality_list = []


def format_mp3():
    if len(format_list) > 1:
        format_list.pop()
    format_list.append(".mp3")


def format_avi():
    if len(format_list) > 1:
        format_list.pop()
    format_list.append(".avi")


def format_mkv():
    if len(format_list) > 1:
        format_list.pop()
    format_list.append(".mkv")


def format_wav():
    if len(format_list) > 1:
        format_list.pop()
    format_list.append(".wav")


def format_mp4():
    if len(format_list) > 1:
        format_list.pop()
    format_list.append(".mp4")


def quality_480():
    if len(quality_list) > 1:
        quality_list.pop()
    quality_list.append("480p")


def quality_audio():
    if len(quality_list) > 1:
        quality_list.pop()
    quality_list.append("audio")


def quality_240():
    if len(quality_list) > 1:
        quality_list.pop()
    quality_list.append("240p")


def quality_360():
    if len(quality_list) > 1:
        quality_list.pop()
    quality_list.append("360p")


def browse():
    folder = filedialog.askdirectory()
    entry_folder.set(folder)


def download():
    link = entry_link.get()
    download_folder = entry_folder.get()
    video_format = format_list[0]
    video_quality = quality_list[0]
    if video_quality == "audio":
        file = YouTube(link).streams.filter(only_audio=True).first().download(download_folder)
    else:
        if video_quality == "480p":
            file = YouTube(link).streams.get_highest_resolution().download(download_folder)
        else:
            if video_quality == "240p":
                file = YouTube(link).streams.get_lowest_resolution().download(download_folder)
            else:
                file = YouTube(link).streams.first().download(download_folder)

    if video_format != ".mp4":
        base, ext = os.path.splitext(file)
        new_file = base + video_format
        # os.rename(file, new_file)
        ff = ffmpy.FFmpeg(inputs={file: None}, outputs={new_file: None})
        ff.run()
        os.remove(file)
    messagebox.showinfo("YouTube Converter", "DESCĂRCAT CU SUCCES ÎN\n" + download_folder)


window = tk.Tk()
window.title("YouTube Converter")
window.geometry("950x650")
window.resizable(False, False)
window.config(background="light sky blue")
img = ImageTk.PhotoImage(Image.open("icon.jpg"))
lbl_image = tk.Label(window, image=img, borderwidth=0)
lbl_image.pack()
lbl_image.place(x=15, y=5)
entry_link = tk.StringVar()
lbl_link = tk.Label(text="LINK", background="light sky blue", font=("Eras Demi ITC", 14))
lbl_link.place(relx=0.5, y=100, anchor=tk.CENTER)
ent_link = tk.Entry(width=80, textvariable=entry_link)
ent_link.place(relx=0.5, y=120, anchor=tk.CENTER)
lbl_format = tk.Label(text="FORMAT", background="light sky blue", font=("Eras Demi ITC", 14))
lbl_format.place(relx=0.5, y=200, anchor=tk.CENTER)
frame1 = tk.Frame(background="light sky blue")
frame1.pack()
frame1.place(relx=0.5, y=250, anchor=tk.CENTER)
btn_mp3 = tk.Button(frame1, text="MP3", background="powder blue", foreground="dodger blue4",
                    font=("Eras Demi ITC", 12), command=format_mp3)
btn_mp3.pack(side=tk.LEFT)
btn_avi = tk.Button(frame1, text="AVI", background="powder blue", foreground="dodger blue4",
                    font=("Eras Demi ITC", 12), command=format_avi)
btn_avi.pack(side=tk.RIGHT)
btn_mkv = tk.Button(frame1, text="MKV", background="powder blue", foreground="dodger blue4",
                    font=("Eras Demi ITC", 12), command=format_mkv)
btn_mkv.pack(side=tk.RIGHT)
btn_wav = tk.Button(frame1, text="WAV", background="powder blue", foreground="dodger blue4",
                    font=("Eras Demi ITC", 12), command=format_wav)
btn_wav.pack(side=tk.RIGHT)
btn_mp4 = tk.Button(frame1, text="MP4", background="powder blue", foreground="dodger blue4",
                    font=("Eras Demi ITC", 12), command=format_mp4)
btn_mp4.pack(side=tk.RIGHT)
lbl_quality = tk.Label(text="CALITATE", background="light sky blue", font=("Eras Demi ITC", 14))
lbl_quality.place(relx=0.5, y=300, anchor=tk.CENTER)
frame2 = tk.Frame(background="light sky blue")
frame2.pack()
frame2.place(relx=0.5, y=350, anchor=tk.CENTER)
btn_480 = tk.Button(frame2, text="480p", background="powder blue", foreground="dodger blue4",
                    font=("Eras Demi ITC", 12), command=quality_480)
btn_480.pack(side=tk.LEFT)
btn_audio = tk.Button(frame2, text="AUDIO", background="powder blue", foreground="dodger blue4",
                      font=("Eras Demi ITC", 12), command=quality_audio)
btn_audio.pack(side=tk.RIGHT)
btn_240 = tk.Button(frame2, text="240p", background="powder blue", foreground="dodger blue4",
                    font=("Eras Demi ITC", 12), command=quality_240)
btn_240.pack(side=tk.RIGHT)
btn_360 = tk.Button(frame2, text="360p", background="powder blue", foreground="dodger blue4",
                    font=("Eras Demi ITC", 12), command=quality_360)
btn_360.pack(side=tk.RIGHT)
lbl_folder = tk.Label(text="FOLDER", background="light sky blue", font=("Eras Demi ITC", 14))
lbl_folder.place(relx=0.5, y=450, anchor=tk.CENTER)
frame3 = tk.Frame(background="light sky blue")
frame3.pack()
frame3.place(relx=0.5, y=480, anchor=tk.CENTER)
entry_folder = tk.StringVar()
ent_folder = tk.Entry(frame3, width=80, textvariable=entry_folder)
ent_folder.pack(side=tk.LEFT)
btn_browse = tk.Button(frame3, text="BROWSE", background="powder blue", foreground="dodger blue4",
                       font=("Eras Demi ITC", 12), command=browse)
btn_browse.pack(side=tk.RIGHT)
btn_download = tk.Button(text="DOWNLOAD", background="powder blue", foreground="red",
                         font=("Eras Demi ITC", 12), height=3, width=20, command=download)
btn_download.place(relx=0.5, y=600, anchor=tk.CENTER)
window.mainloop()
