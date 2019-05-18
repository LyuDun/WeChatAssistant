# -*- coding:utf-8 -*- 
"""
实现功能：
1、自动回复
2、图形界面
3、自定义回复内容
4、
"""
import itchat
import re
from excel import excel
from tkinter import *
from tkinter import ttk
import tkinter.scrolledtext as tst
import threading
import queue
import time


Listen_Flag = False
ON = False
excel = excel()
keyword_dict = excel.get_keyword_dict()
group_list = excel.get_group_list()
q = queue.Queue()
lock = threading.Lock()


@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    if (Listen_Flag == True):
        if msg['Type'] == 'Text':
            reply_content = msg['Text']
            for key, value in keyword_dict.items():
                if re.search(key, reply_content):
                    itchat.send(value, toUserName=msg['FromUserName'])
                    str = '(%s) -> %s\n' % (
                        msg.User['NickName'], reply_content)
                    q.put(str)


@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
def group_chat_reply(msg):
    if (Listen_Flag == True):
        if msg.User["NickName"] in group_list:
            if msg['Type'] == 'Text':
                reply_content = msg['Text']
                for key, value in keyword_dict.items():
                    if re.search(key, reply_content):
                        itchat.send(value, toUserName=msg['FromUserName'])
                        str = '【%s】：(%s) -> %s\n' % (msg.User["NickName"],
                                                     msg.User.Self['NickName'], reply_content)
                        q.put(str)


class App(object):
    def __init__(self, root):
        self.root = root
        self.root.size = '440*440'
        self.root.title('微信助手')
        self.root.geometry('500x500')
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.tabControl = ttk.Notebook(self.root)
        self.tab1 = ttk.Frame(self.tabControl)
        self.tab1.columnconfigure(0, weight=1)
        self.tab1.rowconfigure(0, weight=1)
        self.tabControl.add(self.tab1, text='监控')
        self.tab2 = ttk.Frame(self.tabControl)
        self.tab2.columnconfigure(0, weight=1)
        self.tab2.rowconfigure(0, weight=1)
        self.tabControl.add(self.tab2, text='关键词')
        self.tab3 = ttk.Frame(self.tabControl)
        self.tab3.columnconfigure(0, weight=1)
        self.tab3.rowconfigure(0, weight=1)
        self.tabControl.add(self.tab3, text='群发')
        self.tabControl.pack(expand=1, fill=BOTH)
        # tab1
        self.a_mighty = ttk.LabelFrame(self.tab1, text='监控界面 ')
        self.a_mighty.pack(fill=BOTH, expand=1)
        self.a_listbox1 = tst.ScrolledText(self.a_mighty)
        self.a_listbox1.pack(fill=BOTH, expand=1)
        self.button_login = Button(self.tab1, text='登陆', command=self.Login_in)
        self.button_login.pack(padx=5, pady=0, side=LEFT, anchor=NW)
        self.button_listen = Button(
            self.tab1, text="启动监控", command=self.Listen_ON)
        self.button_listen.pack(padx=5, pady=0, side=LEFT, anchor=NW)
        self.button_clear = Button(
            self.tab1, text='清空', command=self.ClearMeaaage)
        self.button_clear.pack(padx=10, pady=0, side=LEFT, anchor=NW)
        # tab2
        self.b_mighty = ttk.LabelFrame(self.tab2, text='关键词')
        self.b_mighty.pack(fill=BOTH, expand=1)
        self.b_listbox1 = Listbox(self.b_mighty)
        self.b_listbox2 = Listbox(self.b_mighty)
        self.b_listbox1.pack(side=LEFT, fill=BOTH, expand=1)
        self.b_listbox2.pack(side=LEFT, fill=BOTH, expand=1)
        # tab3
        self.c_mighty = ttk.LabelFrame(self.tab3, text='多群发送')
        self.c_mighty.pack(fill=BOTH, expand=1)

        list1 = StringVar(value=group_list)
        self.c_Listname = Listbox(self.c_mighty, height=len(
            group_list), listvariable=list1, selectmode=MULTIPLE)
        self.c_Listname.pack(padx=10)

        self.c_input = tst.ScrolledText(self.c_mighty, width=65, height=7)
        self.c_input.pack(padx=0, pady=0, side=BOTTOM, anchor=NW)
        self.button_send = Button(
            self.tab3, text='发送', command=self.SendMessage_thread)
        self.button_send.pack(padx=10, pady=0, side=RIGHT, anchor=NW)

    def Login_in(self):
        self.thread = threading.Thread(target=self.wechat_login)
        self.thread.setDaemon(True)
        self.thread.start()
        self.button_login.config(text='退出', command=self.Login_out)
        self.button_login['bg'] = 'green'

    def Login_out(self):
        self.thread = threading.Thread(target=self.wechat_logout)
        self.thread.setDaemon(True)
        self.thread.start()
        self.button_login.config(text='登陆', command=self.Login_in)
        self.button_login['bg'] = 'white'

    def wechat_login(self):
        itchat.auto_login(hotReload=True)
        itchat.run()

    def wechat_logout(self):
        itchat.logout()

    def Listen_ON(self):
        global Listen_Flag
        if(Listen_Flag == False):
            self.button_listen['bg'] = 'green'
            self.button_listen.config(text='停止监控', command=self.Listen_OFF)
            self.thread = threading.Thread(target=self.ShowMessage)
            self.thread.setDaemon(True)
            self.thread.start()
            Listen_Flag = True

    def Listen_OFF(self):
        global Listen_Flag
        if(Listen_Flag == True):
            self.button_listen['bg'] = 'white'
            self.button_listen.config(text='启动监控', command=self.Listen_ON)
            Listen_Flag = False

    def ShowMessage(self):
        while(True):
            while not q.empty():
                str = q.get()
                self.a_listbox1.insert(END, str)
                self.a_listbox1.see(END)
            time.sleep(1)

    def ClearMeaaage(self):
        self.a_listbox1.delete(1.0, END)

    def ShowKeyWord(self):
        for key, value in keyword_dict.items():
            self.b_listbox1.insert(END, key)
            self.b_listbox2.insert(END, value)
        return

    def SendMessage(self):
        selected_list = []
        for i, group in enumerate(group_list):
            if(self.c_Listname.selection_includes(i) == True):
                groups = itchat.search_chatrooms(name=group)
                groupname = groups[0]['UserName']
                str = self.c_input.get(1.0, END)
                itchat.send(str, toUserName=groupname)

    def SendMessage_thread(self):
        self.thread = threading.Thread(target=self.SendMessage)
        self.thread.setDaemon(True)
        self.thread.start()


if __name__ == "__main__":
    root = Tk()
    tool = App(root)
    tool.ShowKeyWord()
    root.mainloop()