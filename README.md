# WeChatAssistant
微信助手，有GUI图形界面、扫码登陆、关键词监控、自动回复、关键词及回复内容展示增加删除、群发消息、多群发送等功能

开发python版本python 3.7.0
# 一、功能介绍
- 有GUI界面
- 关键词监听并回复指定内容（可监听个人对话和群消息）
- 展示关键词
- 可以多选群，并多群发消息
- 多选好友，群发消息
- 可选择是否开启监听

# 二、下载
[软件下载地址](https://github.com/LvDunn/WeChatAssistant/blob/master/exe/%E5%BE%AE%E4%BF%A1%E5%8A%A9%E6%89%8Bexe.exe)
点击进入后，点击右下角Download就可下载。

# 三、界面展示

界面一，可以扫码登陆，选择登陆退出、选择是否监听关键词并回复制定内容
![image](https://github.com/LvDunn/WeChatAssistant/blob/master/image/%E7%95%8C%E9%9D%A21.PNG)
---
界面二，可以显示关键词和回复内容，可以增加、删除指定关键词和回复内容
![image](https://github.com/LvDunn/WeChatAssistant/blob/master/image/%E7%95%8C%E9%9D%A22.PNG) 
---
界面三，可以多选群，并多群发送消息。注意：只能检测到未免打扰的群，如果还有未检测到的群，请点击添加到通讯录
![image](https://github.com/LvDunn/WeChatAssistant/blob/master/image/%E7%95%8C%E9%9D%A23.PNG) 
---
界面四，可以多选指定好友，并发送消息   
![image](https://github.com/LvDunn/WeChatAssistant/blob/master/image/%E7%95%8C%E9%9D%A24.png)




# 四、编译
如果你想自己编译打包，可以按以下步骤操作

## 1.下载源代码

## 2.pip install itchat 

## 3.下载pyinstaller  使用pyinstaller进行打包
pyinstaller的spec文件可以参照以下内容:

binaries内是源码附加文件的存放地址，以下是我的存放地址，你可以更改为你的地址。

console=False代表打包后，不会出现控制台窗口
```
# -*- mode: python -*-

block_cipher = None


a = Analysis(['WeChatAssistant.py'],
             pathex=['D:\\Codes\\WeChatProgramCodes'],
             binaries=[('D:\\Codes\WeChatProgramCodes\groupdata.json','.'),('D:\\Codes\WeChatProgramCodes\keyword.json','.'),('D:\\Codes\WeChatProgramCodes\weixin.ico','.')],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='WeChatAssistant',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False )
```
