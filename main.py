from tkinter import *
from PIL import Image, ImageTk
from api import qq_song_list, qm_song, qm_singer, qq_song, help, setting
from icon import img  # 引入ico
import base64, os

"""
    @Name:Music Downloader
    @Function:Download 全民K歌, QQ音乐
    @Author：Li4n0
    @Version: 1.1.0
    @Date：2018-02-04 12:51:57
"""


class Music_Downloader:
    def __init__(self):  # 初始化窗口及部件
        root = Tk()
        root.title("Music Downloader 1.0")
        root.geometry('550x200+%d+%d' % ((root.winfo_screenwidth() - 550) / 2, (root.winfo_screenheight() - 500) / 2))
        with open("tmp.ico", "wb+") as tmp:  # 加载ico
            tmp.write(base64.b64decode(img[1:]))
        ico = Image.open('tmp.ico')
        ico = ImageTk.PhotoImage(ico)
        os.remove("tmp.ico")
        root.tk.call('wm', 'iconphoto', root._w, ico)
        root.resizable(width=False, height=False)
        self.root = root
        self.menu = Menu(self.root)
        self.text = StringVar()
        self.entry = Entry(self.root, width=50, font=('', '15', 'italic'), textvariable=self.text, bd=4,
                           fg='gray')
        self.button = Button(self.root, text='开 始', width=14, height=2,
                             command=lambda: start(self),
                             font=('黑体', '12', ''))
        self.label = Label(self.root, text=' @Author:  Li4n0   \n543153648@qq.com\n@Version:1.10', fg='gray',
                           font=('微软等线', '11', ''))
        self.list = Listbox(root, font=('', '10', ''))
        self.scrolly = Scrollbar(self.list, orient=VERTICAL)
        self.storage_path = get_storage_path()

    def init(self):  # 部件摆放
        self.text.set("Ctrl+V粘贴链接或输入查询关键词")
        self.childmenu = Menu(self.menu, tearoff=0)
        self.childmenu.add_command(label='设置储存路径', command=lambda: setting(self))
        self.childmenu.add_command(label='帮助', command=lambda: help(self.root))
        self.menu.add_cascade(label='菜单', menu=self.childmenu)
        self.entry.place(x='24', y='40')
        self.button.place(x='210', y='85')
        self.label.pack(side='bottom')
        self.root.config(menu=self.menu)
        self.scrolly.config(command=self.list.yview)


def get_storage_path():
    if os.path.exists('.setting'):
        with open('.setting/setting.ini', 'r') as setting_file:
            return setting_file.read()
    else:
        os.mkdir('.setting')
        with open('.setting/setting.ini', 'w') as setting_file:
            if os.path.exists('output/') is False:
                os.mkdir('output/')
            setting_file.write('output/')
            return 'output/'


def start(window):
    text = window.text.get()
    root = window.root
    root.geometry('550x500')
    window.list.place(relx='0.04', rely='0.3', relwidth='0.9', relheight='0.58')
    window.list.delete(0, END)
    window.scrolly.pack(side=RIGHT, fill='y')
    if hasattr(window, 'list2'):
        window.list2.destroy()
    root.update()
    if 'http' in text:  # 当输入为链接
        if 'playsquare' in text or 'playlist' in text:  # QQ音乐歌单
            qq_song_list(text, window)
        elif 'kg.qq.com/node/personal?uid' in text or 'kg.qq.com/personal?uid' in text:  # 全民K歌歌手公开作品
            qm_singer(text, window)
        elif 'node.kg.qq.com/play?s' in text or 'kg2.qq.com/node/play?s' in text:  # 全民K歌单曲
            qm_song(text, window)
            root.update_idletasks()
    else:  # 当输入为关键字
        if '|' in text:
            text = text.split('|')
            qq_song(text[0], window, text[1])
        else:
            qq_song(text, window)


if __name__ == '__main__':
    Music_downloader = Music_Downloader()
    Music_downloader.init()
    Music_downloader.root.mainloop()
