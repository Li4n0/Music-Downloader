from tkinter import *
from PIL import Image, ImageTk
from api import qq_song_list, qm_song, qm_singer, qq_song, help

"""
    @Name:Music Downloader
    @Function:Download 全民K歌, QQ音乐
    @Author：Li4n0
    @Date：2018-02-04 12:51:57
"""


class Window:
    def __init__(self):  # 初始化窗口及部件
        root = Tk()
        root.title("Music Downloader 1.0")
        root.geometry('550x200+%d+%d' % ((root.winfo_screenwidth() - 550) / 2, (root.winfo_screenheight() - 500) / 2))
        ico = Image.open('icon/main.png')
        ico = ImageTk.PhotoImage(ico)
        root.tk.call('wm', 'iconphoto', root._w, ico)
        root.resizable(width=False, height=False)
        self.root = root
        self.menu = Menu(self.root)
        self.text = StringVar()
        self.entry = Entry(self.root, width=50, font=('', '14', 'italic'), textvariable=self.text, bd=3,
                           fg='gray')
        self.button = Button(self.root, text='开 始', width=14, height=2,
                             command=lambda: deal_input(self.text, self.root),
                             font=('黑体', '12', ''))
        self.label = Label(self.root, text=' @Author:  Li4n0   \n543153648@qq.com\n@Version:1.0', fg='gray',
                           font=('微软等线', '11', ''))

    def initwindow(self):  # 部件摆放
        self.text.set("Ctrl+V 粘贴链接，或输入查询关键词")
        self.menu.add_command(label='帮助', command=lambda: help(self.root))
        self.entry.place(x='24', y='50')
        self.button.place(x='210', y='85')
        self.label.pack(side='bottom')
        self.root.config(menu=self.menu)


def deal_input(var, root):  # 处理输入
    text = var.get()
    root.geometry('550x500')
    list = Listbox(root, font=('', '10', ''))
    list.place(relx='0.04', rely='0.3', relwidth='0.9', relheight='0.58')
    scrolly = Scrollbar(list, orient=VERTICAL)
    scrolly.pack(side=RIGHT, fill='y')
    scrolly.config(command=list.yview)
    root.update()
    if 'http' in text:  # 当输入为链接
        if 'song' in text:
            qq_song(text, list, root)
        elif 'playsquare' in text or 'playlist' in text:
            qq_song_list(text, list, root)
        elif 'node.kg.qq.com/personal' in text:
            qm_singer(text, list, root)
        elif 'node.kg.qq.com/play' in text:
            qm_song(text, list)
            root.update_idletasks()
    else:  # 当输入为关键字
        if '|' in text:
            text = text.split('|')
            qq_song(text[0], list, root, text[1])
        else:
            qq_song(text, list, root)


if __name__ == '__main__':
    Music_downloader = Window()
    Music_downloader.initwindow()
    Music_downloader.root.mainloop()
