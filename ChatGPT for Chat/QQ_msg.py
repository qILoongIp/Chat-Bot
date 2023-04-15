import win32con,win32gui,win32api
import uiautomation as ui
import win32clipboard as w
from Openai_model import AI
import time
import threading
import tkinter as tk
import ctypes
class QQ_Chat():
    def __init__(self,name,api_key,find_str = '@ChatGPT',temperature = 0):
        self.msg = ''#消息内容
        self.Got_Messages = [None]#用于记录已接收的消息
        self.Replied_Messages = [None]#用于记录已回复的消息
        self.Messages = dict()#用于储存历史记录，这个历史记录要发给ai，这样才能使得ai能够联系上下文
        self.name = name#用户的QQ昵称
        self.temperature = temperature#用于控制ai回答的随机性0~1
        self.find_str = find_str#根据此字符串寻找对方的消息是否是需要用ai回答的
        self.ai = AI(api_key,self.temperature)
        self.lock = threading.Lock()#创建锁对象
        self.root = tk.Tk()#创建Tk对象用于获取当前电脑的分辨率
        #获取分辨率
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        #获取缩放倍率
        self.user32 = ctypes.windll.user32
        self.scale_factor = self.user32.GetDpiForSystem() / 96
    #获取对方的消息
    def get_msg(self):
        while True:
            #获取消息
            try:
                #刷新消息
                hwnd = win32gui.FindWindow(None, "消息管理器")
                left, top, right, bottom = win32gui.GetWindowRect(hwnd)
                #print("窗口位置：左={}, 上={}, 右={}, 下={}".format(left, top, right, bottom))
                #做一个处理，防止用户分辨率改变导致程序运行不了
                num1 = int(((((69+17)/2560)*self.width)/1.5)*self.scale_factor)
                num2 = int(((((130+17)/1440)*self.height)/1.5)*self.scale_factor)
                long_position = win32api.MAKELONG(right-left-num1,num2)#810, 130
                win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position)
                win32api.SendMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position)
                with self.lock:
                    with ui.UIAutomationInitializerInThread():#多线程用uiautomation库的方法时必须加这个
                        list_window = ui.ListControl(Name='IEMsgView')
                        return_msg = list_window.GetLastChildControl().Name
            except:
                try:#防止用户一直关闭消息管理器导致错误
                    #点击显示消息记录
                    hwnd = win32gui.FindWindow(None, self.name)
                    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
                    #print("窗口位置：左={}, 上={}, 右={}, 下={}".format(left, top, right, bottom))
                    #做一个处理，防止用户分辨率改变导致程序运行不了
                    num1 = int(((((19+21)/2560)*self.width)/1.5)*self.scale_factor)
                    num2 = int(((((177+21)/1440)*self.height)/1.5)*self.scale_factor)
                    long_position = win32api.MAKELONG(right-left-num1,bottom-top-num2)
                    win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position)
                    win32api.SendMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position)
                    #点击显示消息管理
                    hwnd = win32gui.FindWindow(None,self.name)
                    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
                    #print("窗口位置：左={}, 上={}, 右={}, 下={}".format(left, top, right, bottom))
                    #做一个处理，防止用户分辨率改变导致程序运行不了
                    num1 = int(((((34+58)/2560)*self.width)/1.5)*self.scale_factor)
                    num2 = int(((((13+15)/1440)*self.height)/1.5)*self.scale_factor)
                    long_position = win32api.MAKELONG(right-left-num1,bottom-top-num2)
                    win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position)
                    win32api.SendMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position)
                    #刷新消息
                    hwnd = win32gui.FindWindow(None, "消息管理器")
                    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
                    #print("窗口位置：左={}, 上={}, 右={}, 下={}".format(left, top, right, bottom))
                    #做一个处理，防止用户分辨率改变导致程序运行不了
                    num1 = int(((((69+17)/2560)*self.width)/1.5)*self.scale_factor)
                    num2 = int(((((130+17)/1440)*self.height)/1.5)*self.scale_factor)
                    long_position = win32api.MAKELONG(right-left-69-17,130+17)#810, 130
                    win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position)
                    win32api.SendMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position)
                    with self.lock:#关键操作锁一下防止出错
                        with ui.UIAutomationInitializerInThread():#多线程用uiautomation库的方法时必须加这个
                            list_window = ui.ListControl(Name='IEMsgView')
                            return_msg = list_window.GetLastChildControl().Name
                except:
                    pass
            #找到最后一次@ChatGPT的内容
            try:
                return_msg_index = return_msg.rfind(self.find_str)
                if return_msg_index != -1:
                    return_msg = return_msg[return_msg_index:]#获取对方的消息
                    return_msg = return_msg.replace(' ','')#清除对方消息中所有的空格
                    return_msg = return_msg.replace('\r','')#清除对方消息中所有的回车
                    return_msg = return_msg.replace('\n','')#清除对方消息中所有的回车
                    return_msg = return_msg.replace(self.find_str,'')#清除对方消息中的“@ChatGPT”字样
                    #确保不重复捕捉同样的消息
                    if return_msg not in self.Got_Messages:
                        #因为两个函数同时访问Got_Messages会产生冲突，所以有函数访问的时候要锁住,with代码块运行时自动获取锁，运行完毕自动释放锁
                        with self.lock:
                            self.Got_Messages.append(return_msg)
                            print('对方'+':'+return_msg+'\n')
                            print(self.Got_Messages)
                            self.Messages['User:'+return_msg] = 0#做了一个处理，防止一开始没有历史消息导致ai发生错误
                            #return return_msg
                    else:
                        print('捕捉到重复消息！')
                        #return None
                else:
                    print('未捕捉到关键字！')
            except:
                pass
            #await asyncio.sleep(0.1)#每0.1秒读取一次新消息
    # 输出字符串
    def send_msg(self):
        while True:
            #print('节点1')
            try:
                #print('节点2')
                #因为两个函数同时访问Got_Messages会产生冲突，所以有函数访问的时候要锁住,with代码块运行时自动获取锁，运行完毕自动释放锁
                with self.lock:
                    #print('节点3')
                    reply_list = list(set(self.Got_Messages) - set(self.Replied_Messages))#获取一个需要回复的列表
                if len(reply_list) > 0:
                    #print('节点4')
                    #对待回复列表中的消息依次回复
                    for return_msg in reply_list:
                        response =self.ai.Chat_AI(return_msg,self.Messages)#获取AI的消息，此时可以让另一个函数运作
                        if 'AI:' in response['choices'][0]['message']['content']:
                            response['choices'][0]['message']['content'] = response['choices'][0]['message']['content'].replace('AI:','')#把ChatGPT回复的话里面的可能出现的“AI:”字样删除
                        print('对于"{return_msg}"消息的自动回复:\n\n'.format(return_msg = return_msg) + response['choices'][0]['message']['content'])
                        self.msg = '对于"{return_msg}"消息的自动回复:\n\n'.format(return_msg = return_msg) + response['choices'][0]['message']['content']
                        self.Replied_Messages.append(return_msg)#将已回复的消息放进列表中
                        with open(file = 'QQ_msg_data.txt',mode = 'a+',encoding='utf-8') as file:
                            file.write('User:'+return_msg+'\n')
                            file.write('AI:'+response['choices'][0]['message']['content']+'\n\n')
                        self.Messages['User:'+return_msg] = 'AI:'+response['choices'][0]['message']['content']#将本次回复写入字典
                        #将测试消息放到剪贴板
                        w.OpenClipboard()
                        w.EmptyClipboard()
                        w.SetClipboardData(win32con.CF_UNICODETEXT,self.msg)
                        w.CloseClipboard()
                        '''
                        #发送消息(微信似乎不能用这个方法？)，这个方法能够实现后台发送消息，但是有一定几率出bug，因此此处采用微信模块中的方法来发送消息
                        handle = win32gui.FindWindow(None,self.name)
                        win32api.SendMessage(handle,win32con.WM_PASTE,0,0)
                        win32api.SendMessage(handle,win32con.WM_KEYDOWN,win32con.VK_RETURN,0)
                        '''
                        with self.lock:
                            with ui.UIAutomationInitializerInThread():#多线程用uiautomation库的方法时必须加这个
                                #发送消息
                                qq_window = ui.WindowControl(Name = self.name)
                                qq_window.SwitchToThisWindow(waitTime=0.5)
                                if not qq_window.IsTopmost():
                                    qq_window.SetTopmost()#先将qq窗口置顶
                                edit = ui.EditControl(Name = '输入')
                                #await asyncio.sleep(0.5)#防止消息输入不全
                                #time.sleep(0.5)
                                edit.SendKeys('{Ctrl}v',waitTime=0)
                                edit.SendKeys('{Enter}',waitTime=0)
                else:
                    pass
                    #await asyncio.sleep(1)
            except:
                pass
    #创建一个异步函数，返回一个同时运行两个函数的协程
    '''async def interaction(self):
        await asyncio.gather(self.get_msg(), self.send_msg())'''
    #启动协程
    def running(self):
        try:
            '''loop = asyncio.get_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.interaction())'''
            #直接开两个线程让两个函数同时跑
            thread1 = threading.Thread(target=self.get_msg)
            thread2 = threading.Thread(target=self.send_msg)
            #开始两个线程
            thread1.start()
            thread2.start()
            #等待两个线程结束
            thread1.join()
            thread2.join()
        except:
            print('quite')