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
from tkinter import *
from tkinter import ttk
import tkinter.scrolledtext as tst
import threading
import queue
import time
from basedata import jsonManage

Listen_Flag = False
js = jsonManage()
keyword_dict = {}
group_list = []
frind_dict = {}
q = queue.Queue()


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
        self.root.resizable(False,False)
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
        self.tabControl.add(self.tab3, text='多群发送')
        self.tabControl.pack(expand=1, fill=BOTH)
        self.tab4 = ttk.Frame(self.tabControl)
        self.tab4.columnconfigure(0, weight=1)
        self.tab4.rowconfigure(0, weight=1)
        self.tabControl.add(self.tab4, text='群发')
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
        self.b_listbox1 = Listbox(self.b_mighty, width=33, height=10)
        self.b_listbox2 = Listbox(self.b_mighty, width=33, height=10)
        self.b_listbox1.pack(padx=5,side=LEFT,  anchor=NW,fill=BOTH)
        self.b_listbox2.pack(padx=5,side=LEFT,  anchor=NW,fill=BOTH)
        
        self.b_lable1 = Label(self.tab2, text="关键字")
        self.b_lable1.pack( padx=0, pady=5, side=LEFT)
        self.b_key_input = tst.ScrolledText(self.tab2, width=22, height=2)
        self.b_key_input.pack( padx=0, pady=5, side=LEFT)
        self.b_lable2 = Label(self.tab2, text="回复内容")
        self.b_lable2.pack( padx=0, pady=0, side=LEFT)
        self.b_value_input = tst.ScrolledText(self.tab2, width=22, height=2)
        self.b_value_input.pack( padx=0, pady=0, side=LEFT, anchor=S)
        self.button_add_keyword = Button(
            self.tab2, text='增加', command=self.AddKeyword)
        self.button_add_keyword.pack(padx=0, pady=0, side=TOP, anchor=NW)
        self.button_delete_keyword = Button(
            self.tab2, text='删除', command=self.DeleteKeyword)
        self.button_delete_keyword.pack(padx=0, pady=0, side=LEFT, anchor=S)
        # tab3
        self.c_mighty = ttk.LabelFrame(self.tab3, text='多群发送')
        self.c_mighty.pack(fill=BOTH, expand=1)

        self.c_Listname = Listbox(self.c_mighty, selectmode=MULTIPLE)
        self.c_Listname.pack(padx=10)
        self.c_lable = Label(self.tab3, text="只能检测到未免打扰的群，如果还有未检测到的群，请点击添加到通讯录")
        self.c_lable.pack( padx=0, pady=5, side=LEFT)

        self.c_input = tst.ScrolledText(self.c_mighty, width=65, height=7)
        self.c_input.pack(padx=0, pady=0, side=BOTTOM, anchor=NW)
        self.button_send = Button(
            self.tab3, text='发送', command=self.SendMessage_thread)
        self.button_send.pack(padx=10, pady=0, side=RIGHT, anchor=NW)
        # tab4
        self.d_mighty = ttk.LabelFrame(self.tab4, text='群发')
        self.d_mighty.pack(fill=BOTH, expand=1)

        self.d_Listname = Listbox(self.d_mighty, selectmode=MULTIPLE)
        self.d_Listname.pack(padx=10)

        self.d_input = tst.ScrolledText(self.d_mighty, width=65, height=7)
        self.d_input.pack(padx=0, pady=0, side=BOTTOM, anchor=NW)
        self.d_button_send = Button(
            self.tab4, text='发送', command=self.SendFriend)
        self.d_button_send.pack(padx=10, pady=0, side=RIGHT, anchor=NW)

    def Login_in(self):
        self.thread1 = threading.Thread(target=self.wechat_login)
        self.thread1.setDaemon(True)
        self.thread1.start()
        self.button_login.config(text='退出', command=self.Login_out)
        self.button_login['bg'] = 'green'
        self.ShowKeyWord()
        
    def Login_out(self):
        self.thread = threading.Thread(target=self.wechat_logout)
        self.thread.setDaemon(True)
        self.thread.start()
        self.button_login.config(text='登陆', command=self.Login_in)
        self.button_login['bg'] = 'white'

    def wechat_login(self):
        itchat.auto_login(hotReload=True)
        chatroomsList =itchat.get_chatrooms()
        for chatroom in chatroomsList:
            group_list.append(chatroom["NickName"])
        js.writejson('groupdata.json',group_list)
        self.ShowGroup()
        self.ShowFriends()
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
        global keyword_dict
        keyword_dict = js.readjson('keyword.json')
        self.b_listbox1.delete(0,'end')
        self.b_listbox2.delete(0,'end')
        for key, value in keyword_dict.items():
            self.b_listbox1.insert(END, key)
            self.b_listbox2.insert(END, value)
    
    def AddKeyword(self):
        global keyword_dict
        key = None
        value = None
        key = self.b_key_input.get(1.0, END)
        value = self.b_value_input.get(1.0, END)
        if(key.isspace() == True or value.isspace() == True):
            key = None
            value = None
            return
        keyword_dict[key] = value
        js.writejson('keyword.json',keyword_dict)
        self.b_key_input.delete(1.0, END)
        self.b_value_input.delete(1.0, END)
        self.ShowKeyWord()
    
    def DeleteKeyword(self):
        global keyword_dict
        for i in range(len(keyword_dict)):
            if(self.b_listbox1.selection_includes(i) == True):
                key = self.b_listbox1.get(i)
                keyword_dict.pop(key)
        js.writejson('keyword.json',keyword_dict)
        self.ShowKeyWord()

    def ShowGroup(self):
        self.c_Listname.delete(0,'end')
        for group in group_list:
            self.c_Listname.insert(END, group)
    
    def ShowFriends(self):
        friendslist = itchat.get_friends(update=True)[1:]
        global frind_dict
        for frind in friendslist:
            if (frind['RemarkName'] == ''):
                frind_dict[frind['NickName']] = frind['NickName']
                self.d_Listname.insert(END, frind['NickName'])
            else:
                frind_dict[frind['RemarkName']] = frind['NickName']
                self.d_Listname.insert(END, frind['RemarkName'])
        print(frind_dict)

    def SendFriend(self):
        global frind_dict
        for i in range(len(frind_dict)):
            if(self.d_Listname.selection_includes(i) == True):
                key = self.d_Listname.get(i)
                value = frind_dict[key]
                str = self.d_input.get(1.0, END)
                self.d_input.delete(1.0, END)
                frind = itchat.search_friends(nickName=value)[0]['UserName']
                itchat.send(str,toUserName=frind)

    def SendMessage(self):
        for i, group in enumerate(group_list):
            if(self.c_Listname.selection_includes(i) == True):
                groups = itchat.search_chatrooms(name=group)
                groupname = groups[0]['UserName']
                str = self.c_input.get(1.0, END)
                self.c_input.delete(1.0, END)
                itchat.send(str, toUserName=groupname)

    def SendMessage_thread(self):
        self.thread = threading.Thread(target=self.SendMessage)
        self.thread.setDaemon(True)
        self.thread.start()

    def remove_emoji(self, string):
        emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
        return emoji_pattern.sub(r'', string)

if __name__ == "__main__":
    root = Tk()
    tool = App(root)
    root.mainloop()
