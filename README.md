# WeChatAssistant
微信助手，有GUI图形界面、扫码登陆、关键词监控、自动回复、关键词及回复内容展示、群发消息等功能

开发python版本python 3.7.0
# 一、功能介绍
- 有GUI界面
- 关键词监听并回复指定内容（可监听个人对话和群消息）
- 展示关键词
- 可以多选群，并群发消息
- 可选择是否开启监听

# 二、界面展示
![image](https://github.com/LvDunn/WeChatAssistant/blob/master/image/%E7%95%8C%E9%9D%A21.PNG)
![image](https://github.com/LvDunn/WeChatAssistant/blob/master/image/%E7%95%8C%E9%9D%A22.PNG)
![image](https://github.com/LvDunn/WeChatAssistant/blob/master/image/%E7%95%8C%E9%9D%A23.PNG)

# 三、说明

## ！为了方便修改，本项目的配置信息存放在excel里面，当你下载exe可执行文件的同时，也要同时下载 “自动回复.xlsx” excel文件，并确保在执行的时候，两者在同一个目录下面。
![image](https://github.com/LvDunn/WeChatAssistant/blob/master/image/exce%E9%85%8D%E7%BD%AE%E5%9B%BE%E7%89%87.PNG)

“自动回复.xlsx”的第一列是你要监听的关键字。
本项目会监听个人和群内发的文字消息，你需要确保没有把群设置为免打扰，否则不会监听到消息。

第二列是当监听到关键字的时候，要回复的内容。第一列和第二列都是两两对应的。

第三列是你要监听的群的名称，也是你要向多个群发送消息的时候可以选择的群列表。

# 四、下载
你需要下载两个文件。第一个是WeChatAssistant.exe文件。[软件下载地址](https://github.com/LvDunn/WeChatAssistant/blob/master/exe/WeChatAssistant.exe)

第二个是自动回复.xlsx文件。[excel下载地址](https://github.com/LvDunn/WeChatAssistant/blob/master/src/%E8%87%AA%E5%8A%A8%E5%9B%9E%E5%A4%8D.xlsx)

进入下载网页后，点击右下角Download就可下载。

![image](https://github.com/LvDunn/WeChatAssistant/blob/master/image/%E4%B8%8B%E8%BD%BD.PNG)

# 四、编译
如果你想自己编译打包，可以按以下步骤操作

## 1.下载源代码

## 2.pip install itchat 

## 3.pip install openpyxl

## 4.下载pyinstaller  使用pyinstaller进行打包
