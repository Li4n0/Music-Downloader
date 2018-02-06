import json
import time
import os
import random
import requests
import tkinter.filedialog
from bs4 import BeautifulSoup
from tkinter import *

api = (
    'https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg',
    'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?&p=2&n=',
    'https://c.y.qq.com/qzone/fcg-bin/fcg_ucc_getcdinfo_byids_cp.fcg?type=1&disstid='
)


def download_qq_music(song_data, storage_path, list_name=None):  # 下载QQ音乐
    songmid = song_data['songmid']
    filename = 'C400' + songmid + '.m4a'
    guid = int(random.random() * 2147483647) * int(time.time() * 1000) % 10000000000
    params = {
        'format': 'json',
        'cid': 205361747,
        'uin': 0,
        'songmid': songmid,
        'filename': filename,
        'guid': guid,
    }
    r = requests.get(api[0], params=params)
    try:
        vkey = json.loads(r.content)['data']['items'][0]['vkey']
    except json.decoder.JSONDecodeError:
        r = requests.get(api[0], params=params)
        vkey = json.loads(r.content)['data']['items'][0]['vkey']
    audio_url = 'http://dl.stream.qqmusic.qq.com/%s?vkey=%s&guid=%s&uin=0&fromtag=66' % (filename, vkey, guid)  # 获取直链
    song = requests.get(audio_url)
    if list_name is not None:
        if os.path.exists(storage_path + list_name) is False:
            os.mkdir(storage_path + list_name)
        filename = ("%s/%s %s.mp3" % (
            list_name, song_data['songname'].replace('/', ''), song_data['singer'][0]['name'].replace('/', '')))
    else:
        filename = (
                "%s %s.mp3" % (song_data['songname'].replace('/', ''), song_data['singer'][0]['name'].replace('/', '')))
        # 过滤不合法文件名 (非常想知道歌手们为什么都这么有创造力，想出了这么多奇怪的歌名和艺名(╯‵□′)╯︵┻━┻)
    filename = filename.replace('|', ':').replace('\"', '').replace('\\', '').replace('“', '').replace('”', '').replace(
        ':', '：').replace('*', '').replace('?','？')
    with open(storage_path + filename.replace('|', '：'), 'wb') as file:
        file.write(song.content)
        return (filename + '' * (30 - len(filename)) + '下载完成')


def qq_song(name, window, n='20'):  # 在QQ音乐乐库中搜索
    search_url = api[1] + n + '&w=' + name
    songs = requests.get(search_url).text[9:-1]
    songs = json.loads(songs)
    songs_id = 1
    songs_list = songs['data']['song']['list']
    for i in songs_list:
        window.list.insert(END, "     %-10s%s%s" % (
            songs_id, i['songname'].rjust(-20), i['singer'][0]['name'].rjust(40 - len(i['songname'] * 2))))
        songs_id += 1
    window.list2 = Listbox(window.root, font=('', '10', ''))
    window.list2.place(relx='0.04', rely='0.865', relwidth='0.9', relheight='0.035')

    def download(event):  # 下载选中歌曲
        try:
            songs_id = window.list.curselection()[0]
            song_data = songs_list[songs_id]
            window.list2.insert(0, download_qq_music(song_data, window.storage_path))
        except IndexError:
            pass

    window.list.bind("<<ListboxSelect>>", download)


def qq_song_list(url, window):  # 下载QQ音乐歌单内歌曲
    root = window.root
    list = window.list
    storage_path = window.storage_path
    dissit_id = re.findall('\d+', url)[0]
    url_l = api[2] + dissit_id
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
        'Referer': url  # 无聊的判断来源
    }
    data_r = requests.get(url_l, headers=headers).text[13:-1]
    cdlist = json.loads(data_r)['cdlist']
    list_name = cdlist[0]['dissname'].replace('|', '：')
    songlist = cdlist[0]['songlist']
    # for song in songlist:
    i = 0
    while i < len(songlist):
        song = songlist[i]
        try:
            list.insert(0, download_qq_music(song, storage_path, list_name))
            root.update()
            i += 1
        except Exception as message:
            # print(message)
            list.insert(0, '该歌曲下载失败，(若一直出错请检查网络或联系作者)错误信息：' + str(message))
            root.update()
    list.insert(0, '      ---------------全部下载完成,共计%s首歌曲--------------' % (len(songlist)))


def qm_song(url, window):  # 下载全民音乐单曲
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    singer = soup.select('.singer_user__name')[0]
    music_name = soup.select('.play_name')[0].text.strip()
    r_data = soup.select('script')[2].text[18:-2]
    singer_name = singer.text.strip()
    audio_url = json.loads(r_data)['detail']['playurl']
    if len(audio_url) < 5:  # 忽略诡异的纯MV作品
        return
    music = requests.get(audio_url)
    filename = music_name + '-' + singer_name + '.mp3'
    filename = filename.replace('|', ':').replace('\"', '').replace('\\', '').replace('/', '')

    with open(window.storage_path + filename, 'wb') as file:
        file.write(music.content)
        window.list.insert(0, '             ' + filename + ' ' * (30 - len(filename)) + '下载完成')


def qm_singer(url, window):  # 下载全民K歌歌手所有公开作品
    singer_index = requests.get(url)
    soup = BeautifulSoup(singer_index.text, 'lxml')
    songlist = soup.select('.mod_playlist__cover')
    for song in songlist:
        qm_song(song.get('href'), window)
        window.root.update_idletasks()
    window.list.insert(0, '      ---------------全部下载完成,共计%s首歌曲--------------' % (len(songlist)))


def help(root):  # 帮助面板
    help_window = Toplevel()
    help_window.title("帮助")
    help_window.geometry(
        '450x400+%d+%d' % ((root.winfo_screenwidth() - 270) / 2, (root.winfo_screenheight() - 400) / 2))
    help_message = """
        Music Downloader
    Music Downloader 是一款用来下载试听音乐的工具
    \n——————————————————————————————————————
目前支持功能:
        1、根据歌名或歌手在QQ音乐乐库中搜索并下载歌曲
        2、根据歌单链接，下载QQ音乐歌单内全部歌曲
        3、根据链接下载全民K歌好友单曲或全部公开作品
    \n———————————————————————————————————————
使用方法：
        1、在输入框中输入对应的歌曲/歌单(仅支持qq音乐)/全
            民K歌作品分享/好友主页链接 即可下载音乐
        2、在输入框中输入 歌曲名/歌手名 即可在乐库中搜索歌曲，
            在关键字后+‘|’+数字 可以控制搜索歌曲的数目，
            默认为20条)如 输入‘周杰伦|30’ 将显示‘周杰伦’相关
            的30首歌曲。在搜索结果列表 单击 想要下载的乐曲即可下载。
        3、歌曲默认下载到本工具目录下的/output文件夹下,可另行修改
        ——————————————————————————————————————— 
        项目地址：https://github.com/Li4n0/Music-Downloader/
                        @Author：Li4n0            
                    """
    Label(help_window, text=help_message).pack()


def setting(window):
    directory = tkinter.filedialog.askdirectory() + '/'
    if len(directory) != 1:
        window.storage_path = directory
        with open('.setting/setting.ini', 'w') as setting_file:
            setting_file.write(directory)
